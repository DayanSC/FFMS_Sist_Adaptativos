#python script.py -i <ruta-al-archivo-de-instancia> -th 0.80

import random
import argparse

def read_instance(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def ffmsp_randomized_greedy_heuristic(strings, m, threshold):
    alphabet = ['C', 'G', 'T', 'A']
    result = []
    
    for j in range(m):
        occurrences = {char: 0 for char in alphabet}
        for string in strings:
            occurrences[string[j]] += 1
        
        # Ordenar caracteres por frecuencia ascendente
        sorted_chars = sorted(occurrences.items(), key=lambda x: x[1])
        
        # Seleccionar caracteres hasta alcanzar el umbral
        total_occurrences = sum(occurrences.values())
        cumulative_occurrences = 0
        candidates = []
        
        for char, count in sorted_chars:
            candidates.append(char)
            cumulative_occurrences += count
            if cumulative_occurrences / total_occurrences >= threshold:
                break
        
        # Elegir aleatoriamente entre los candidatos
        chosen_char = random.choice(candidates)
        result.append(chosen_char)
    
    return ''.join(result)

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def evaluate_solution(solution, strings):
    return min(hamming_distance(solution, s) for s in strings)

def main():
    parser = argparse.ArgumentParser(description="Greedy heuristic for FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Path to the problem instance file")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Threshold percentage (e.g., 0.75, 0.80, 0.85)")
    
    args = parser.parse_args()
    
    strings = read_instance(args.instance)
    m = len(strings[0])  # Assuming all strings have the same length
    
    solution = ffmsp_randomized_greedy_heuristic(strings, m, args.threshold)
    score = evaluate_solution(solution, strings)
    
    #print(f"Input strings: {strings}")
    print(f"Solution found: {solution}")
    print(f"Score (minimum distance): {score}")

if __name__ == "__main__":
    main()
