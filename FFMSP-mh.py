import time
import random
import argparse

def read_instance(file_path):
    """Reads the problem instance from the given file"""
    with open(file_path, 'r') as file:
        strings = [line.strip() for line in file.readlines()]
    return strings

def hamming_distance(s1, s2, threshold):
    """Calculates the distance between two strings as the number of positions with different characters"""
    hd = sum(c1 != c2 for c1, c2 in zip(s1, s2))
    if hd/len(s1) >= threshold:
        return 1
    else:
        return 0 

def evaluate_solution(solution, strings, threshold):
    """Evaluates a solution"""
    score = 0
    for s in strings:
        score += hamming_distance(solution, s, threshold)
    return score

def construct_greedy_randomized_solution(strings, drate):
    """Greedy randomized construction for FFMSP"""
    num_strings = len(strings)
    string_length = len(strings[0]) # m
    
    # Initialize the greedy string as a list of characters
    greedy_string = []
    
    for i in range(string_length):
        # Random value between 0 and 1
        chance = random.random() < drate
        
        if chance:
            # Count the frequency of each character at position i
            counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
            for s in strings:
                counts[s[i]] += 1
            # Choose the least frequent character
            min_char = min(counts, key=counts.get)
            greedy_string.append(min_char)
        else:
            greedy_string.append(random.choice(['A', 'C', 'G', 'T']))
            
    return ''.join(greedy_string)

def local_search(solution, strings, threshold):
    """Local search for FFMSP""" 
    improved = True
    best_solution = solution
    best_score = evaluate_solution(solution, strings, threshold)

    while improved:
        improved = False
        for i in range(len(solution)):
            for new_char in ['A', 'C', 'G', 'T']:
                if new_char != solution[i]:
                    new_solution = solution[:i] + new_char + solution[i+1:]
                    new_score = evaluate_solution(new_solution, strings, threshold)
                    if new_score > best_score:
                        best_solution = new_solution
                        best_score = new_score
                        improved = True

        solution = best_solution

    return best_solution, best_score

def grasp(strings, threshold, drate, max_time):
    """GRASP for FFMSP with Any-Time behavior"""
    start_time = time.time()
    best_solution = None
    best_score = 0
    best_time = 0

    print(f"Score: {best_score}, Time: {best_time:.12f}")

    while time.time() - start_time < max_time:
        # Construction phase
        solution = construct_greedy_randomized_solution(strings, drate)
        
        # Local search phase
        solution, score = local_search(solution, strings, threshold)
        
        if score > best_score:
            best_solution = solution
            best_score = score
            best_time = time.time() - start_time
            print("New solution found")
            print(f"Score: {best_score}, Time: {best_time:.12f}")

    return best_solution, best_score, best_time

def main():
    parser = argparse.ArgumentParser(description="GRASP for FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Path to the problem instance file")
    parser.add_argument('-t', '--time', type=int, required=True, help="Maximum execution time in seconds")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Threshold percentage (e.g., 0.75, 0.80, 0.85)")
    parser.add_argument('-dr', '--drate', type=float, default=0.9, help="drate parameter for GRASP (default: 0.9)")
    
    args = parser.parse_args()

    threshold = args.threshold
    max_time = args.time
    instance = args.instance
    drate = args.drate
    
    strings = read_instance(instance)
    
    solution, score, time_found = grasp(strings, threshold, drate, max_time)
    
    print("Best solution found")
    print(f"Score: {score}, Time: {time_found:.12f}")
    print(f"Solution: {solution}")
if __name__ == "__main__":
    main()