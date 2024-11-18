import random
import argparse
import time
from typing import List, Tuple
from collections import Counter

################# Util #####################
def read_instance(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def hamming_distance(s1: str, s2: str) -> int:
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def evaluate_solution(solution: str, strings: List[str], threshold: float) -> int:
    return sum(1 for s in strings if hamming_distance(solution, s) / len(s) >= threshold)

################# Advanced Construction #####################
def get_position_weights(strings: List[str]) -> List[dict]:
    """Calculate character frequency weights for each position"""
    string_length = len(strings[0])
    position_weights = []
    
    for i in range(string_length):
        counter = Counter(s[i] for s in strings)
        total = sum(counter.values())
        # Convert to probability distribution
        weights = {char: count/total for char, count in counter.items()}
        position_weights.append(weights)
    
    return position_weights

def smart_random_solution(strings: List[str], position_weights: List[dict]) -> str:
    """Generate a solution using position-specific probabilities"""
    solution = []
    for pos_weight in position_weights:
        # Invert probabilities to favor less common characters
        total = sum(pos_weight.values())
        inv_weights = {char: (total - weight)/total for char, weight in pos_weight.items()}
        # Normalize inverted weights
        total_inv = sum(inv_weights.values())
        norm_weights = {char: weight/total_inv for char, weight in inv_weights.items()}
        
        chars, weights = zip(*norm_weights.items())
        solution.append(random.choices(chars, weights=weights)[0])
    
    return ''.join(solution)

################# Population Management #####################
def initialize_population(population_size: int, strings: List[str]) -> List[str]:
    position_weights = get_position_weights(strings)
    return [smart_random_solution(strings, position_weights) for _ in range(population_size)]

def adaptive_tournament_selection(population: List[str], scores: List[int], generation: int, 
                               max_generations: int) -> str:
    """Tournament selection with adaptive pressure"""
    # Increase selection pressure as generations progress
    k = max(3, min(15, int(3 + (12 * generation / max_generations))))
    selected = random.sample(list(zip(population, scores)), k)
    return max(selected, key=lambda x: x[1])[0]

################# Genetic Operators #####################
def intelligent_crossover(parent1: str, parent2: str, strings: List[str], threshold: float) -> str:
    """Intelligent crossover that evaluates potential crossing points"""
    best_child = parent1
    best_score = evaluate_solution(parent1, strings, threshold)
    
    # Try different crossover points and keep the best result
    for i in range(1, len(parent1) - 1):
        child1 = parent1[:i] + parent2[i:]
        score1 = evaluate_solution(child1, strings, threshold)
        
        if score1 > best_score:
            best_child = child1
            best_score = score1
    
    return best_child

def adaptive_mutation(sequence: str, mutation_rate: float, score: int, best_score: int) -> str:
    """Adaptive mutation rate based on solution quality"""
    # Increase mutation rate for solutions far from the best
    quality_factor = score / best_score if best_score > 0 else 1
    adjusted_rate = mutation_rate * (2 - quality_factor)
    
    sequence = list(sequence)
    for i in range(len(sequence)):
        if random.random() < adjusted_rate:
            sequence[i] = random.choice(['A', 'C', 'G', 'T'])
    return ''.join(sequence)

################# Main Algorithm #####################
def genetic_algorithm(strings: List[str], threshold: float, population_size: int, 
                     generations: int, mutation_rate: float, max_time: int) -> Tuple[str, int]:
    print("Initializing improved genetic algorithm...")
    
    # Initialize population with smart construction
    population = initialize_population(population_size, strings)
    scores = [evaluate_solution(ind, strings, threshold) for ind in population]
    
    best_solution = max(population, key=lambda x: evaluate_solution(x, strings, threshold))
    best_score = evaluate_solution(best_solution, strings, threshold)
    
    stagnation_counter = 0
    last_best_score = best_score
    
    start_time = time.time()
    
    for generation in range(generations):
        if time.time() - start_time > max_time:
            break
            
        # Elite preservation (top 10%)
        elite_size = max(1, population_size // 10)
        sorted_population = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)
        elite = [ind for ind, _ in sorted_population[:elite_size]]
        
        new_population = elite.copy()
        
        # Generate new individuals
        while len(new_population) < population_size:
            parent1 = adaptive_tournament_selection(population, scores, generation, generations)
            parent2 = adaptive_tournament_selection(population, scores, generation, generations)
            
            # Intelligent crossover
            child = intelligent_crossover(parent1, parent2, strings, threshold)
            
            # Adaptive mutation
            child_score = evaluate_solution(child, strings, threshold)
            child = adaptive_mutation(child, mutation_rate, child_score, best_score)
            
            new_population.append(child)
            
        population = new_population
        scores = [evaluate_solution(ind, strings, threshold) for ind in population]
        
        # Update best solution
        current_best = max(population, key=lambda x: evaluate_solution(x, strings, threshold))
        current_score = evaluate_solution(current_best, strings, threshold)
        
        if current_score > best_score:
            best_solution = current_best
            best_score = current_score
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        
        # Population restart if stagnated
        if stagnation_counter >= 20:
            print(f"Restarting population at generation {generation + 1}")
            population = initialize_population(population_size, strings)
            population[:elite_size] = elite  # Preserve elite
            stagnation_counter = 0
        
        if generation % 10 == 0:
            print(f"Generation {generation + 1}: Best score = {best_score}")
            
    return best_solution, best_score

def main():
    parser = argparse.ArgumentParser(description="Improved Genetic Algorithm for FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Path to instance file")
    parser.add_argument('-t', '--time', type=int, required=True, help="Maximum execution time in seconds")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Distance threshold (e.g., 0.75)")
    parser.add_argument('-p', '--population', type=int, default=200, help="Population size (default: 200)")
    parser.add_argument('-g', '--generations', type=int, default=1000, help="Maximum generations (default: 1000)")
    parser.add_argument('-m', '--mutation', type=float, default=0.1, help="Base mutation rate (default: 0.1)")
    
    
    args = parser.parse_args()
    
    strings = read_instance(args.instance)
    solution, score = genetic_algorithm(
        strings, args.threshold, args.population, 
        args.generations, args.mutation, args.time
    )
    
    print("\nFinal Results:")
    print(f"Best Score: {score}")
    print(f"Solution: {solution}")

if __name__ == "__main__":
    main()