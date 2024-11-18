import random
import argparse
import time

################# Util #####################
# Lectura de la instancia
def read_instance(file_path):
    with open(file_path, 'r') as file:
        strings = [line.strip() for line in file.readlines()]
    return strings

# Distancia de Hamming
def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# Función de evaluación: cuenta las secuencias que están lejos según el umbral
def evaluate_solution(solution, strings, threshold):
    count = 0
    for s in strings:
        if hamming_distance(solution, s) / len(s) >= threshold:
            count += 1
    return count

################# Greedy #####################

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

################# Initial Population #####################

def initialize_population_with_greedy(population_size, strings, drate):
    population = []
    for _ in range(population_size):
        population.append(construct_greedy_randomized_solution(strings, drate))
    return population

################# Genetic Algorithm #####################
# Selección por torneo
def tournament_selection(population, scores, k=3):
    selected = random.sample(list(zip(population, scores)), k)
    return max(selected, key=lambda x: x[1])[0]

# Crossover de un punto
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

# Mutación: cambia un carácter de la secuencia
def mutate(sequence, mutation_rate):
    sequence = list(sequence)
    for i in range(len(sequence)):
        if random.random() < mutation_rate:
            sequence[i] = random.choice(['A', 'C', 'G', 'T'])
    return ''.join(sequence)

# Algoritmo genético
def genetic_algorithm(strings, threshold, population_size, generations, mutation_rate, max_time, drate):
    print("Generating initial population...")
    
    best_solution = None
    best_score = 0

    population = initialize_population_with_greedy(population_size, strings, drate)
    scores = [evaluate_solution(ind, strings, threshold) for ind in population]

    start_time = time.time()

    for generation in range(generations):
        if time.time() - start_time > max_time:
            break
        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)
            offspring = crossover(parent1, parent2)
            offspring = mutate(offspring, mutation_rate)
            new_population.append(offspring)
        population = new_population
        scores = [evaluate_solution(ind, strings, threshold) for ind in population]

        # Guardar el mejor individuo
        current_best = max(population, key=lambda ind: evaluate_solution(ind, strings, threshold))
        current_best_score = evaluate_solution(current_best, strings, threshold)
        if current_best_score > best_score:
            best_solution = current_best
            best_score = current_best_score

        print(f"Generation {generation+1}: Best score = {best_score}")

    return best_solution, best_score

# Función principal para manejo de argumentos
def main():
    parser = argparse.ArgumentParser(description="Algoritmo Genético para FFMSP")
    parser.add_argument('-i', '--instance', required=True, help="Ruta al archivo de instancia")
    parser.add_argument('-t', '--time', type=int, required=True, help="Tiempo máximo de ejecución en segundos")
    parser.add_argument('-th', '--threshold', type=float, required=True, help="Umbral de porcentaje (e.g., 0.75, 0.80)")
    parser.add_argument('-dr', '--drate', type=float, default=0.9, help="Parámetro D-rate para GRASP (default: 0.9)")
    parser.add_argument('-p', '--population', type=int, default=100, help="Tamaño de la población (default: 100)")
    parser.add_argument('-g', '--generations', type=int, default=100, help="Número máximo de generaciones (default: 1000)")
    parser.add_argument('-m', '--mutation', type=float, default=0.1, help="Tasa de mutación (default: 0.1)")
    
    args = parser.parse_args()

    threshold = args.threshold
    max_time = args.time
    instance = args.instance
    population_size = args.population
    generations = args.generations
    mutation_rate = args.mutation
    drate = args.drate
    
    strings = read_instance(instance)

    solution, score = genetic_algorithm(strings, threshold, population_size, generations, mutation_rate, max_time, drate)
    
    print("Best solution found")
    print(f"Score: {score}")
    print(f"Solution: {solution}")

if __name__ == "__main__":
    main()
