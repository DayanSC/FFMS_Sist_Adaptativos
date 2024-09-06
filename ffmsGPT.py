import sys
import time

def read_instance(file_path):
    """Lee la instancia del problema desde el archivo dado"""
    with open(file_path, 'r') as file:
        strings = [line.strip() for line in file.readlines()]
    return strings

def hamming_distance(s1, s2):
    """Calcula la distancia entre dos strings como el número de posiciones con caracteres distintos"""
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def evaluate_solution(solution, strings):
    return min(hamming_distance(solution, s) for s in strings)

def greedy_ffmsp(strings, threshold):
    """Heurística greedy para el problema Far From Most String"""
    num_strings = len(strings)
    string_length = len(strings[0])
    
    # Inicializar la cadena greedy como una lista de caracteres
    greedy_string = []
    
    for i in range(string_length):
        # Contar la frecuencia de cada carácter en la posición i
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
        for s in strings:
            counts[s[i]] += 1
        
        # Ordenar caracteres por frecuencia (menos frecuente primero)
        sorted_chars = sorted(counts.keys(), key=lambda x: counts[x])
        
        # Escoger el carácter más distante posible (menos frecuente)
        for char in sorted_chars:
            # Contar cuántas veces este carácter sería distinto en el umbral
            num_diff = sum(1 for s in strings if s[i] != char) / num_strings
            if num_diff >= threshold:
                greedy_string.append(char)
                break
    
    return ''.join(greedy_string)

def main():
    # Leer los argumentos de la línea de comandos
    args = sys.argv
    if len(args) != 5 or args[1] != "-i" or args[3] != "-th":
        print("Uso: python ffmsGPT.py -i <instancia-problema> -th <threshold>")
        return
    
    instance_file = args[2]
    threshold = float(args[4])
    
    # Leer la instancia del problema
    strings = read_instance(instance_file)
    
    # Medir el tiempo de inicio
    #start_time = time.time()
    
    # Ejecutar la heurística greedy
    solution = greedy_ffmsp(strings, threshold)
    score = evaluate_solution(solution, strings)
    
    # Medir el tiempo final
    #end_time = time.time()
    
    # Mostrar el resultado (solución y tiempo de ejecución)
    print(f"Solución greedy: {solution}")
    print(f"Score (minimum distance): {score}")
    #print(f"Tiempo de ejecución: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    main()
