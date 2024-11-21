import time
import random
import argparse

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

def tournament_selection(population, fitness, k=3):
    """Tournament selection with probability of selecting best"""
    tournament = random.sample(list(range(len(population))), k)
    tournament_fitness = [fitness[i] for i in tournament]
    
    # Add probability of selecting the best
    if random.random() < 0.9:  # 90% chance of selecting the best
        return population[tournament[tournament_fitness.index(max(tournament_fitness))]]
    else:
        return population[random.choice(tournament)]

def uniform_crossover(parent1, parent2):
    """Uniform crossover with improved gene selection"""
    child1 = list(parent1)
    child2 = list(parent2)
    
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1[i], child2[i] = child2[i], child1[i]
    
    return ''.join(child1), ''.join(child2)

def mutate(individual, mutation_rate, alphabet, strings, threshold):
    """Smart mutation operator that considers position-specific information"""
    individual = list(individual)
    string_length = len(individual)
    
    for i in range(string_length):
        if random.random() < mutation_rate:
            # Count frequencies at this position
            counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
            for s in strings:
                counts[s[i]] += 1
            
            # Choose from less frequent characters
            sorted_chars = sorted(counts.items(), key=lambda x: x[1])
            possible_chars = [char for char, _ in sorted_chars[:2]]  # Take the two least frequent
            
            # Don't choose the current character if possible
            if individual[i] in possible_chars:
                possible_chars.remove(individual[i])
            
            if possible_chars:
                individual[i] = random.choice(possible_chars)
            else:
                individual[i] = random.choice([c for c in alphabet if c != individual[i]])
    
    return ''.join(individual)

def construct_greedy_randomized_solution(strings, drate):
    """Enhanced greedy randomized construction"""
    string_length = len(strings[0])
    greedy_string = []
    
    for i in range(string_length):
        # Count frequencies at this position
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
        for s in strings:
            counts[s[i]] += 1
        
        if random.random() < drate:
            # Choose from the two least frequent characters
            sorted_chars = sorted(counts.items(), key=lambda x: x[1])
            possible_chars = [char for char, _ in sorted_chars[:2]]
            greedy_string.append(random.choice(possible_chars))
        else:
            greedy_string.append(random.choice(['A', 'C', 'G', 'T']))
    
    return ''.join(greedy_string)

def genetic_algorithm(strings, threshold, population_size, crossover_rate, mutation_rate, max_time, drate):
    """Algorithm for FFMSP"""
    start_time = time.time()
    best_solution = None
    best_score = 0
    best_time = 0
    generations_without_improvement = 0
    max_generations_without_improvement = 20
    
    string_length = len(strings[0])
    alphabet = ['A', 'C', 'G', 'T']
    
    # Initialize population
    population = []
    seen_solutions = set()
    
    while len(population) < population_size:
        individual = construct_greedy_randomized_solution(strings, drate)
        if individual not in seen_solutions:
            population.append(individual)
            seen_solutions.add(individual)
    
    # Evaluate initial population
    fitness = []
    for individual in population:
        score = evaluate_solution(individual, strings, threshold)
        fitness.append(score)
        if score > best_score:
            best_solution = individual
            best_score = score
            best_time = time.time() - start_time
    
    print(f"Initial best score: {best_score}")
    generation = 0
    
    while time.time() - start_time < max_time:
        generation += 1
        new_population = []
        new_fitness = []
        
        # Elitism: Keep the best solution
        elite_idx = fitness.index(max(fitness))
        new_population.append(population[elite_idx])
        new_fitness.append(fitness[elite_idx])
        
        # Generate new population
        while len(new_population) < population_size:
            # Selection
            parent1 = tournament_selection(population, fitness)
            parent2 = tournament_selection(population, fitness)
            
            # Crossover
            if random.random() < crossover_rate:
                child1, child2 = uniform_crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            
            # Mutation
            child1 = mutate(child1, mutation_rate, alphabet, strings, threshold)
            child2 = mutate(child2, mutation_rate, alphabet, strings, threshold)

            # Evaluate and add children
            for child in [child1, child2]:
                if len(new_population) < population_size:
                    score = evaluate_solution(child, strings, threshold)
                    new_population.append(child)
                    new_fitness.append(score)
                    
                    if score > best_score:
                        best_solution = child
                        best_score = score
                        best_time = time.time() - start_time
                        generations_without_improvement = 0
                        print(f"New best solution found in generation {generation}")
                        print(f"Score: {best_score}, Time: {best_time:.2f}")
        
        # Update population and fitness
        population = new_population
        fitness = new_fitness
        
        # Check for stagnation
        generations_without_improvement += 1
        if generations_without_improvement >= max_generations_without_improvement:
            # Introduce diversity
            num_to_replace = population_size // 4  # Replace 25% of population
            for _ in range(num_to_replace):
                idx = random.randint(1, len(population) - 1)  # Don't replace the elite
                new_individual = construct_greedy_randomized_solution(strings, drate)
                population[idx] = new_individual
                fitness[idx] = evaluate_solution(new_individual, strings, threshold)
            generations_without_improvement = 0
            #print(f"Introducing diversity in generation {generation}")
    
    return best_solution, best_score, best_time


def main():
    parser = argparse.ArgumentParser(description="Genetic Algorithm for FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Path to the problem instance file")
    parser.add_argument('-t', '--time', type=int, required=True, help="Maximum execution time in seconds")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Threshold percentage (e.g., 0.75, 0.80, 0.85)")
    parser.add_argument('-p', '--population_size', type=int, default=150, help="Population size")
    parser.add_argument('-c', '--crossover_rate', type=float, default=0.9742, help="Crossover rate")
    parser.add_argument('-m', '--mutation_rate', type=float, default=0.0102, help="Mutation rate")
    parser.add_argument('-dr', '--drate', type=float, default=0.656, help="drate parameter for GA")

    args = parser.parse_args()
    
    strings = read_instance(args.instance)
    
    solution, score, time_found = genetic_algorithm(
        strings, 
        args.threshold, 
        args.population_size, 
        args.crossover_rate, 
        args.mutation_rate, 
        args.time, 
        args.drate
    )
    
    print("\nBest solution found:")
    print(f"Score: {score}")
    print(f"Time found: {time_found:.4f}")
    print(f"Solution: {solution}")
    
    # print(score) This line only for tuning purposes

if __name__ == "__main__":
    main()
