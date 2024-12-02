import time
import random
import argparse
import numpy as np

alphabet = ['A', 'C', 'G', 'T']

def read_instance(file_path):
    """Reads the problem instance from the given file"""
    with open(file_path, 'r') as file:
        strings = [line.strip() for line in file.readlines()]
    return strings

def hamming_distance(s1, s2, threshold):
    """Calculates if the Hamming distance between two strings meets the threshold"""
    hd = sum(c1 != c2 for c1, c2 in zip(s1, s2))
    if hd / len(s1) >= threshold:
        return 1
    else:
        return 0

def evaluate_solution(solution, strings, threshold):
    """Evaluates a solution"""
    score = 0
    for s in strings:
        score += hamming_distance(solution, s, threshold)
    return score

def aco_algorithm(strings, threshold, max_time, num_ants, num_iterations, alpha=1.0, beta=2.0, evaporation_rate=0.5):

    start_time = time.time()
    string_length = len(strings[0])

    # Initialize pheromone levels
    pheromone = np.ones((string_length, len(alphabet)))

    heuristic = compute_heuristic(strings, string_length)
    best_solution = None
    best_score = -1
    best_time = 0

    iteration = 0
    while time.time() - start_time < max_time and iteration < num_iterations:
        solutions = []
        scores = []

        for ant in range(num_ants):
            solution = construct_solution(pheromone, heuristic, alpha, beta, string_length)

            score = evaluate_solution(solution, strings, threshold)
            solutions.append(solution)
            scores.append(score)

            if score > best_score:
                best_solution = solution
                best_score = score
                best_time = time.time() - start_time

        pheromone = update_pheromone(pheromone, solutions, scores, evaporation_rate)

        iteration += 1

    print(f"Best score: {best_score}")
    return best_solution, best_score, best_time

def compute_heuristic(strings, string_length):
    """Compute heuristic values based on character frequencies."""
    heuristic = np.zeros((string_length, 4))
    for i in range(string_length):
        # Count frequencies at this position
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
        for s in strings:
            counts[s[i]] += 1
        
        # Convert dictionary values to array in correct order
        freq_array = np.array([counts['A'], counts['C'], counts['G'], counts['T']])
        # Calculate heuristic values
        heuristic[i] = 1.0 / (freq_array + 1e-6)
    
    return heuristic

def construct_solution(pheromone, heuristic, alpha, beta, string_length):
    solution = []
    for pos in range(string_length):
        probs = (pheromone[pos] ** alpha) * (heuristic[pos] ** beta)
        probs /= probs.sum()
        letter = random.choices(alphabet, weights=probs)[0]
        solution.append(letter)
    return solution

def update_pheromone(pheromone, solutions, scores, evaporation_rate):
    char_to_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    pheromone *= (1 - evaporation_rate)
    for solution, score in zip(solutions, scores):
        for pos, char in enumerate(solution):
            idx = char_to_idx[char]
            pheromone[pos][idx] += score
    return pheromone

def main():
    parser = argparse.ArgumentParser(description="Genetic Algorithm for FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Path to the problem instance file")
    parser.add_argument('-t', '--time', type=int, required=True, help="Maximum execution time in seconds")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Threshold percentage (e.g., 0.75, 0.80, 0.85)")

    args = parser.parse_args()
    
    strings = read_instance(args.instance)
    
    solution, score, time_found = aco_algorithm(
        strings, 
        args.threshold, 
        args.time,
        num_ants=100,
        num_iterations=100
    )
    
    print("\nBest solution found:")
    print(f"Score: {score}")
    print(f"Time found: {time_found:.4f}")
    print(f"Solution: {solution}")
    
    # print(score) This line only for tuning purposes

if __name__ == "__main__":
    main()
