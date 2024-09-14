import sys
import time
import random
import argparse
import os
import glob
from multiprocessing import Pool

def read_input(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def hamming_distance_partial_cached(S, s, cached_distance, j):
    """
    Recalcula la distancia parcial solo para la posición j.
    """
    if S[j] == '' or S[j] == s[j]:
        return cached_distance
    else:
        return cached_distance + 1 if S[j] != s[j] else cached_distance - 1

def count_occurrences(strings, position):  # occ(i,a)
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

def average(score, n):
    return sum(score) / n

def standar_deviation(score, media, n):
    return (sum((x - media) ** 2 for x in score) / n) ** 0.5

def f_partial_optimized(S, strings, threshold, cached_distances, j):
    """
    Calcula el score total, pero actualizando solo la distancia en la posición j.
    """
    score = 0
    for i, s in enumerate(strings):
        cached_distances[i] = hamming_distance_partial_cached(S, s, cached_distances[i], j)
        if cached_distances[i] / len(S) >= threshold:
            score += 1
    return score

def exists_a(S, alphabet, j, strings, threshold, cached_distances):
    current_f_partial = f_partial_optimized(S, strings, threshold, cached_distances, j)  # f_partial
    for a in alphabet:
        new_S = S[:]  
        new_S[j] = a  # Asignar el nuevo carácter en la posición j
        new_f_partial = f_partial_optimized(new_S, strings, threshold, cached_distances, j)
        if new_f_partial > current_f_partial:
            return True, a
    return False, None

def count_occurrencesB(strings, position):
    return {
        'A': sum(1 for s in strings if s[position] == 'A'),
        'C': sum(1 for s in strings if s[position] == 'C'),
        'G': sum(1 for s in strings if s[position] == 'G'),
        'T': sum(1 for s in strings if s[position] == 'T')
    }

def select_min_occurrence_char(strings, j):
    occurrences = count_occurrencesB(strings, j)
    min_occ = min(occurrences.values())
    for char in ['A', 'C', 'G', 'T']:
        if occurrences[char] == min_occ:
            return char

def randomized_ffmsp_optimized(strings, threshold, drate, random_start_position):
    m = len(strings[0])
    alphabet = ['A', 'C', 'G', 'T']
    S = [None] * m  # Initialize S as a list of empty strings
    j = DetermineStartingPosition(strings, random_start_position)
    k = 0
    cached_distances = [0] * len(strings)  # Cache de distancias
    while k < m:
        r = random.random()
        if r <= drate:
            exists, a = exists_a(S, alphabet, j, strings, threshold, cached_distances)
            if exists:
                S[j] = a
            else:
                b = select_min_occurrence_char(strings, j)
                S[j] = b
        else:
            a = random.choice(alphabet)
            S[j] = a
        f_partial_optimized(S, strings, threshold, cached_distances, j)  # Actualizar caché
        j += 1
        if j >= m:
            j = 0
        k += 1
    return S

def calculate_quality(result, strings, threshold):
    score = 0
    for s in strings:
        score += hamming_distance_partial(result, s, threshold)
    return score

def hamming_distance_partial(s1, s2, threshold):
    """
    Calcula la distancia de Hamming parcial para dos strings.
    """
    hd = sum(c1 != c2 for c1, c2 in zip(s1, s2) if c1 != '')  # Comparar solo posiciones donde S tiene letras
    return 1 if hd / len(s1) >= threshold else 0

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
    
    strings = read_input(args.instance)
    
    start_time = time.time()
    result = randomized_ffmsp_optimized(strings, threshold, drate, random_start_position)
    end_time = time.time()

    # Calcular la calidad de la solución
    quality = calculate_quality(result, strings, int(threshold * len(strings[0])))

    for char in result:
        print(char, end='')
    print()
    print(f"Quality score: {quality}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    
if __name__ == "__main__":
    main()