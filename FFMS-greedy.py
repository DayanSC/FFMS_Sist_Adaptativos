import time
import random
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
    """Evalúa una solución"""
    score = 0
    for s in strings:
        score += hamming_distance(solution, s, threshold)
    return score

def greedy_ffmsp(strings, threshold, drate):
    """Heurística greedy"""
    num_strings = len(strings)
    string_length = len(strings[0]) # m
    
    # Inicializar la cadena greedy como una lista de caracteres
    greedy_string = []
    
    for i in range(string_length):
        # Valor aleatorio entre 0 y 1
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
    
    start_time = time.time()
    solution = greedy_ffmsp(strings, threshold, drate)
    end_time = time.time()
    
    score = evaluate_solution(solution, strings, threshold)
    
    #print(f"Solution: {solution}")
    print(f"Score: {score}")
    print(f"Time: {end_time - start_time:.12f}")

if __name__ == "__main__":
    main()
