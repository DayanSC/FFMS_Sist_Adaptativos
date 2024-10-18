// g++ ffms-mh.cpp medidas.cpp -o medidasGreedy
// ./medidasGreddy
// ajustar threshold, drate y max_time en main
// tambien threshold_string en main
// no olvidar cambiar el nombre del archivo de salida (Greedy, GreedyRandomized)
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <random>
#include <algorithm>
#include <chrono>
#include <tuple>
#include <iomanip>
#include <cmath>
#include <filesystem>
#include <numeric>

namespace fs = std::filesystem;


int hamming_distance(const std::string& s1, const std::string& s2, double threshold);

int evaluate_solution(const std::string& solution, const std::vector<std::string>& strings, double threshold);

std::vector<std::string> read_instance(const std::string& file_path);

std::string construct_greedy_randomized_solution(const std::vector<std::string>& strings, double drate);

double average(const std::vector<double>& scores, size_t length) {
    double sum = std::accumulate(scores.begin(), scores.end(), 0.0);
    return sum / length;
}

double standard_deviation(const std::vector<double>& scores, double avg, size_t length) {
    double sum = 0.0;
    for (const auto& score : scores) {
        sum += std::pow(score - avg, 2);
    }
    return std::sqrt(sum / length);
}

inline void display_progress(std::int64_t u, std::int64_t v) {
    const double progress = u / double(v);
    const std::int64_t width = 70;
    const std::int64_t p = width * progress;
    std::int64_t i;

    std::cout << "\033[1m[";
    for (i = 0; i < width; i++) {
        if (i < p)
            std::cout << "=";
        else if (i == p)
            std::cout << ">";
        else
            std::cout << " ";
    }
    std::cout << "] " << std::int64_t(progress * 100.0) << "%\r\033[0m";
    std::cout.flush();
}

int main() {
    double threshold = 0.85;
    std::string threshold_string = "085";
    double drate = 1.0;
    int max_time = 10;
    // imprimir treshold, drate y max_time en una linea
    std::cout << "Threshold: " << threshold << ", Drate: " << drate << ", Max time: " << max_time << std::endl;
    
    std::vector<double> scores;
    std::string path = "datasets/";
    std::vector<std::string> archivos_aux;
    
    std::ofstream csv_file;
    csv_file.open("Greedy_" + threshold_string + ".csv");
    csv_file << "dataset,t_mean_sol,t_stdev" << std::endl; // Encabezados del CSV
    
    for (const auto& entry : fs::directory_iterator(path)) {
        if (entry.path().extension() == ".txt" && entry.path().filename() != "readme.txt" && entry.path().filename() != "test.txt") {
            archivos_aux.push_back(entry.path().string());
        }
    }

    std::vector<std::pair<std::vector<std::string>, std::string>> archivos_matrix = {
        {std::vector<std::string>(), "100-300"},
        {std::vector<std::string>(), "100-600"},
        {std::vector<std::string>(), "100-800"},
        {std::vector<std::string>(), "200-300"},
        {std::vector<std::string>(), "200-600"},
        {std::vector<std::string>(), "200-800"}
    };

    for (auto& [archivos, nombre] : archivos_matrix) {
        for (const auto& archivo : archivos_aux) {
            if (archivo.find(nombre) != std::string::npos) {
                archivos.push_back(archivo);
            }
        }
    }

    int cont = 0;
    for (const auto& [archivos, nombre] : archivos_matrix) {
        std::vector<std::string> strings;
        for (const auto& archivo : archivos) {
            display_progress(++cont, 900);
            strings = read_instance(archivo);
            auto solution= construct_greedy_randomized_solution(strings, drate);
            scores.push_back(evaluate_solution(solution, strings, threshold));
        }
        int tam = archivos.size();
        double media = average(scores, tam);
        double sd = standard_deviation(scores, media, tam);
        csv_file << nombre << "," << media << "," << sd << "," << std::endl;
        scores.clear();
    }
    
    csv_file.close();

    return 0;
}