# experiment_runner.py
import glob
import os
import statistics
import sys
from typing import List, Tuple

from FFMSP_aco import aco_algorithm, read_instance

def average(scores: List[int]) -> float:
    """Calculate average score"""
    return sum(scores) / len(scores)

def standar_deviation(scores: List[int], mean) -> float:
    """Calculate standard deviation of scores"""
    variance = sum((x - mean)**2 for x in scores) / len(scores)
    return statistics.sqrt(variance)

def run_experiments(path, threshold, max_time, num_ants, num_iterations, alpha, beta, evaporation_rate):
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

    print(f"threshold: {threshold}, max_time: {max_time}, num_ants: {num_ants}, num_iterations: {num_iterations}, alpha: {alpha}, beta: {beta}, evaporation_rate: {evaporation_rate}")
    # Run experiments for each dataset group
    for archivos, nombre in archivos_matrix:
        scores = []
        time = []
        
        for archivo in archivos:
            # Read instance
            strings = read_instance(archivo)
            
            # Run genetic algorithm
            solution, score, time_found = aco_algorithm(
                strings=strings,
                threshold=threshold,
                max_time=max_time,
                num_ants=num_ants,
                num_iterations=num_iterations,
                alpha=alpha,
                beta=beta,
                evaporation_rate=evaporation_rate
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
        max_time=60,
        num_ants=94,
        num_iterations=292,
        alpha=0.9981,
        beta=2.8719,
        evaporation_rate=0.4946
    )