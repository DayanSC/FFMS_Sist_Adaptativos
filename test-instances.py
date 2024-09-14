'''
    # Leer la instancias del problema
    score = []    
    
    path = 'datasets/'
    
    archivos_aux = glob.glob(os.path.join(path, "*.txt"))
    archivos_filtrados = [archivo for archivo in archivos_aux if not archivo.endswith("readme.txt")]
    
    archivos_matrix = [ # (1,2)
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-300")],"100-300"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-600")],"100-600"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("100-800")],"100-800"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-300")],"200-300"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-600")],"200-600"),
        ([archivo for archivo in archivos_filtrados if os.path.basename(archivo).startswith("200-800")],"200-800"),
    ]
    cont = 0
    for archivos,nombre in archivos_matrix:
        cont += 1
        for archivo in archivos:
            strings = read_instance(archivo)
            solution = greedy_ffmsp(strings, threshold, drate)
            score.append(evaluate_solution(solution, strings, threshold))
        media = average(score,len(strings[0]))
        print('-'*50)
        print(f"dataset: {nombre}")
        print(f"average: {media:.4f}")
        sd = standar_deviation(score,average(score,len(strings[0])),len(strings[0]))
        print(f"standar deviation: {sd:.4f}")
        print('-'*50)
'''