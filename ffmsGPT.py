import sys
import time
import random
import os
import glob
import argparse

def read_instance(file_path):
    """Lee la instancia del problema desde el archivo dado"""
    with open(file_path, 'r') as file:
        strings = [line.strip() for line in file.readlines()]
    return strings

def hamming_distance(s1, s2, threshold):
    """Calcula la distancia entre dos strings como el número de posiciones con caracteres distintos"""
    hd = sum(c1 != c2 for c1, c2 in zip(s1, s2))
    if hd/len(s1) >= threshold:
        return 1
    else:
        return 0 

def evaluate_solution(solution, strings, threshold):
    """Evalúa una solución para el problema Far From Most String"""
    score = 0
    for s in strings:
        score += hamming_distance(solution, s, threshold)
    return score

def greedy_ffmsp(strings, threshold, drate):
    """Heurística greedy para el problema Far From Most String"""
    num_strings = len(strings)
    string_length = len(strings[0]) # m
    
    # Inicializar la cadena greedy como una lista de caracteres
    greedy_string = []
    
    for i in range(string_length):
        # random value between 0 and 1
        chance = random.random() < drate
        
        if chance:
            # Contar la frecuencia de cada carácter en la posición i
            counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0} # Pendiente randomizar el orden
            for s in strings:
                counts[s[i]] += 1
            
            # Ordenar caracteres por frecuencia (menos frecuente primero)
            sorted_chars = sorted(counts.items(), key=lambda x: x[1])
        
            # Escoger el carácter más distante posible (mas frecuente)
            greedy_string.append(sorted_chars[0][0])
        else:
            greedy_string.append(random.choice(['A', 'C', 'G', 'T']))
            
    return ''.join(greedy_string)

def average(score,n):
    return sum(score) / n

def standar_deviation(score,media,n):
    return (sum((x-media)**2 for x in score)/n)**0.5

def main():
    parser = argparse.ArgumentParser(description="Greedy heuristic for FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Path to the problem instance file")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Threshold percentage (e.g., 0.75, 0.80, 0.85)")
    parser.add_argument('-dr', '--drate', type=float, required=True, help="D-rate percentage (e.g., 0.05, 0.10, 0.15)")
    
    args = parser.parse_args()

    threshold = args.threshold
    drate = args.drate
    instance = args.instance
    
    
    strings = read_instance(instance)
    solution = greedy_ffmsp(strings, threshold, drate)
    score = evaluate_solution(solution, strings, threshold)
    print(f"Solution: {solution}")
    print(f"Score: {score}")
    

    '''
    # Leer la instancias del problema
    score = []    
    
    path = 'datasets/'
    
    archivos_aux = glob.glob(os.path.join(path, "*.txt"))
    archivos_filtrados = [archivo for archivo in archivos_aux if not archivo.endswith("readme.txt")]
    
    archivos_matrix = [ # (1,2)
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-300")],"100-300"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-600")],"100-600"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-800")],"100-800"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-300")],"200-300"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-600")],"200-600"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-800")],"200-800"),
    ]
    cont = 0
    for archivos,nombre in archivos_matrix:
        cont += 1
        for archivo in archivos:
            strings = read_instance(archivo)
            solution = greedy_ffmsp(strings, threshold, drate)
            score.append(evaluate_solution(solution, strings, threshold))
        media = average(score,len(strings[0]))
        print('-'*50)
        print(f"dataset: {nombre}")
        print(f"average: {media}")
        print(f"standar deviation: {standar_deviation(score,average(score,len(strings[0])),len(strings[0]))}")
        print('-'*50)
    '''
if __name__ == "__main__":
    main()
