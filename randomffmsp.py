#python script.py -i <ruta-al-archivo-de-instancia> -th 0.80 -dr 0.05
import sys
import time
import random
import argparse
import os
import glob

def read_input(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def hamming_distance(s1, s2, threshold):
    hd = sum(c1 != c2 for c1, c2 in zip(s1, s2))
    if hd/len(s1) >= threshold:
        return 1
    else:
        return 0 
    #return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def count_occurrences(strings, position): #occ(i,a)
    occurrences = {a: sum(1 for s in strings if s[position] == a) for a in 'ACGT'}
    return occurrences

def min_occurrences(strings, position):
    occurrences = count_occurrences(strings, position)
    return min(occurrences.values())

def DetermineStartingPosition(strings, condition):
    m = len(strings[0])
    min_occs = [min_occurrences(strings, i) for i in range(m)]
    min_value = min(min_occs)
    candidates = [i for i, v in enumerate(min_occs) if v == min_value]
    if condition:
        return random.choice(candidates)
    else:
        return candidates[0]

def average(score,n):
    return sum(score) / n

def standar_deviation(score,media,n):
    return (sum((x-media)**2 for x in score)/n)**0.5

def calculate_quality(result, strings, threshold):
    score = 0
    for s in strings:
        score += hamming_distance(result, s, threshold)
    return score
    #return sum(1 for s in strings if hamming_distance(result, s) >= threshold)

def hamming_distance_partial(s1, s2, threshold):
    """
    Calcula la distancia entre dos strings, pero solo en las posiciones donde s1 (S) tiene una letra.
    """
    # Inicializar la distancia Hamming
    hd = 0
    # Recorrer ambas cadenas posición por posición
    for c1, c2 in zip(s1, s2):
        # Comparar solo cuando c1 (posición de S) no es un carácter vacío
        if c1 != '':  # Aquí asumimos que las posiciones vacías en S son cadenas vacías ('')
            if c1 != c2:
                hd += 1
    
    # Comprobar si la distancia relativa supera el umbral
    if hd / len(s1) >= threshold:
        return 1
    else:
        return 0

def f_partial(S, strings, threshold):
    """
    Calcula el score total comparando la cadena S con una lista de cadenas.
    Solo se comparan las posiciones donde S tenga una letra definida.
    """
    # Inicializar el puntaje total
    score = 0
    
    # Recorrer todas las cadenas en 'strings'
    for s in strings:
        # Acumular el puntaje usando la distancia parcial
        score += hamming_distance_partial(S, s, threshold)
    
    return score

def exists_a(S, alphabet, j, strings, threshold):
    current_f_partial = f_partial(S, strings, threshold)  # f_partial
    for a in alphabet:
        new_S = S[:]  
        new_S[j] = a  # Asignar el nuevo carácter en la posición j
        new_f_partial = f_partial(new_S, strings, threshold)
        if new_f_partial > current_f_partial:
            return True, a
    return False, None

def count_occurrencesB(strings, position):
    """
    Cuenta las ocurrencias de cada carácter en una posición específica
    para todos los strings de entrada.
    """
    return {
        'A': sum(1 for s in strings if s[position] == 'A'),
        'C': sum(1 for s in strings if s[position] == 'C'),
        'G': sum(1 for s in strings if s[position] == 'G'),
        'T': sum(1 for s in strings if s[position] == 'T')
    }

def select_min_occurrence_char(strings, j):
    """
    Selecciona el carácter con la mínima ocurrencia en la posición j.
    Si hay múltiples caracteres con la misma ocurrencia mínima, 
    selecciona el primero alfabéticamente.
    """
    occurrences = count_occurrencesB(strings, j)
    min_occ = min(occurrences.values())
    for char in ['A', 'C', 'G', 'T']:  # Orden alfabético
        if occurrences[char] == min_occ:
            return char
        
def randomized_ffmsp(strings, threshold, drate, random_start_position):
    m = len(strings[0])
    alphabet = ['A', 'C', 'G', 'T']
    S = [None] * m  # Initialize S as a list of empty strings
    j = DetermineStartingPosition(strings, random_start_position)
    k = 0
    while k < m:
        r = random.random()
        if r <= drate:
            a, exists = exists_a(S, alphabet, j, strings, threshold)
            if exists:
                S[j] = a
            else: # Letra con menor ocurrencia en la columna
                b = select_min_occurrence_char(strings, j)
                S[j] = b
        else: 
            a = random.choice(['A', 'C', 'G', 'T'])
            S[j] = a
        j += 1
        if j >= m:
            j = 0
        k += 1
    return S

def main():
    parser = argparse.ArgumentParser(description="Greedy heuristic for FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Path to the problem instance file")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Threshold percentage (e.g., 0.75, 0.80, 0.85)")
    parser.add_argument('-dr', '--drate', type=float, required=True, help="D-rate percentage (e.g., 0.05, 0.10, 0.15)")
    parser.add_argument('-rsp', '--randomstartposition', action='store_true', help="Random start position")
    
    args = parser.parse_args()

    threshold = args.threshold
    drate = args.drate
    random_start_position = args.randomstartposition
    
    '''
    score = []
    path = 'datasets/'
    
    archivos_aux = glob.glob(os.path.join(path, "*.txt"))
    archivos_filtrados = [archivo for archivo in archivos_aux if not archivo.endswith("readme.txt")]
    
    archivos_matrix = [
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-300")],"100-300"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-600")],"100-600"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-800")],"100-800"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-300")],"200-300"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-600")],"200-600"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-800")],"200-800"),
    ]

    for archivos,nombre in archivos_matrix:
        for archivo in archivos:
            strings = read_input(archivo)
            solution = randomized_ffmsp(strings, threshold, drate, random_start_position)
            score.append(calculate_quality(solution, strings, threshold))
        media = average(score,len(strings[0]))
        print('-'*50)
        print(f"dataset: {nombre}")
        print(f"average: {media}")
        print(f"standar deviation: {standar_deviation(score,average(score,len(strings[0])),len(strings[0]))}")
        print('-'*50)
    '''
    
    strings = read_input(args.instance)
    
    start_time = time.time()
    result = randomized_ffmsp(strings, threshold, drate, random_start_position)
    end_time = time.time()

    # Calcular la calidad de la solución
    quality = calculate_quality(result, strings, threshold)

    for char in result:
        print(char, end='')
    print()
    print(f"{quality}")
    
if __name__ == "__main__":
    main()