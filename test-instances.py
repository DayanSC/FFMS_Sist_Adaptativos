# experiment_runner.py
import glob
import os
import statistics
from typing import List, Tuple
from ffmsp_solver import genetic_algorithm, read_instance

def average(scores: List[int]) -> float:
    """Calculate average score"""
    return sum(scores) / len(scores)

def standar_deviation(scores: List[int], mean) -> float:
    """Calculate standard deviation of scores"""
    variance = sum((x - mean)**2 for x in scores) / len(scores)
    return statistics.sqrt(variance)

def run_experiments(path, threshold, population_size, 
                   crossover_rate, mutation_rate, 
                   max_time, drate):
    """Run experiments on all dataset groups"""
    
    # Get all txt files except readme
    archivos_aux = glob.glob(os.path.join(path, "*.txt"))
    archivos_filtrados = [archivo for archivo in archivos_aux if not archivo.endswith("readme.txt")]

    # Group files by dataset type
    archivos_matrix = [
        ([a for a in archivos_filtrados if os.path.basename(a).startswith("100-300")], "100-300"),
        ([a for a in archivos_filtrados if os.path.basename(a).startswith("100-600")], "100-600"),
        ([a for a in archivos_filtrados if os.path.basename(a).startswith("100-800")], "100-800"),
        ([a for a in archivos_filtrados if os.path.basename(a).startswith("200-300")], "200-300"),
        ([a for a in archivos_filtrados if os.path.basename(a).startswith("200-600")], "200-600"),
        ([a for a in archivos_filtrados if os.path.basename(a).startswith("200-800")], "200-800"),
    ]

    print(f"threshold: {threshold}, population_size: {population_size}, crossover_rate: {crossover_rate}, mutation_rate: {mutation_rate}, max_time: {max_time}, drate: {drate}")
    # Run experiments for each dataset group
    for archivos, nombre in archivos_matrix:
        scores = []
        time = []
        
        for archivo in archivos:
            # Read instance
            strings = read_instance(archivo)
            
            # Run genetic algorithm
            solution, score, time_found = genetic_algorithm(
                strings=strings,
                threshold=threshold,
                population_size=population_size,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate,
                max_time=max_time,
                drate=drate
            )
            
            scores.append(score)
            time.append(time_found)
            #print(f"Dataset: {nombre}, Archivo: {archivo}, Score: {score}, Time: {time_found:.2f}")
            
        # Calculate statistics
        #print(len(scores))
        media = average(scores)
        sd = standar_deviation(scores, media)
        media_time = average(time)
        
        # Print results
        print('-'*50)
        print(f"Dataset: {nombre}")
        print(f"Average: {media:.6f}")
        print(f"Standard deviation: {sd:.6f}")
        print(f"Average time: {media_time:.6f}")
        print('-'*50)

if __name__ == "__main__":
    print ("Running experiments ...")
    # Example usage
    run_experiments(
        path='datasets/',
        threshold=0.75,
        population_size=150,
        crossover_rate=0.9742,
        mutation_rate=0.0102,
        max_time=10,
        drate=0.656
    )