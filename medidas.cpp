#include <iostream>
#include <vector>
#include <string>
#include <filesystem>
#include <fstream>
#include <cmath>
#include <algorithm>

namespace fs = std::filesystem;

std::vector<std::string> read_instance(const std::string& filename) {
    std::vector<std::string> strings;
    std::ifstream file(filename);
    std::string line;
    while (std::getline(file, line)) {
        strings.push_back(line);
    }
    return strings;
}

std::vector<std::string> construct_greedy_randomized_solution(const std::vector<std::string>& strings, double threshold, double drate) {
    size_t num_strings = strings.size();
    size_t string_length = strings[0].size();

    std::string greedy_string;

    // Generadores aleatorios
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0, 1);
    std::uniform_int_distribution<> char_dis(0, 3);
    const char nucleotides[4] = { 'A', 'C', 'G', 'T' };

    for (size_t i = 0; i < string_length; ++i) {
        double chance = dis(gen);

        if (chance < drate) {
            // Cuenta la frecuencia de cada carácter en la posición i
            std::map<char, int> counts = { {'A', 0}, {'C', 0}, {'G', 0}, {'T', 0} };
            for (const auto& s : strings) {
                counts[s[i]] += 1;
            }
            // Encuentra el carácter con la frecuencia mínima
            char min_char = 'A';
            int min_count = counts['A'];
            for (const auto& pair : counts) {
                if (pair.second < min_count) {
                    min_char = pair.first;
                    min_count = pair.second;
                }
            }
            greedy_string.push_back(min_char);
        } else {
            // Selecciona un carácter aleatorio
            greedy_string.push_back(nucleotides[char_dis(gen)]);
        }
    }

    return greedy_string;
}

std::pair<std::string, int> local_search(const std::string& initial_solution, const std::vector<std::string>& strings, double threshold) {
    bool improved = true;
    std::string solution = initial_solution;
    int best_score = evaluate_solution(solution, strings, threshold);

    while (improved) {
        improved = false;
        std::string best_solution = solution;
        for (size_t i = 0; i < solution.size(); ++i) {
            for (char new_char : { 'A', 'C', 'G', 'T' }) {
                if (new_char != solution[i]) {
                    std::string new_solution = solution;
                    new_solution[i] = new_char;
                    int new_score = evaluate_solution(new_solution, strings, threshold);
                    if (new_score > best_score) {
                        best_solution = new_solution;
                        best_score = new_score;
                        improved = true;
                    }
                }
            }
        }
        solution = best_solution;
    }

    return { solution, best_score };
}

// GRASP para FFMSP
std::tuple<std::string, int, double> grasp(const std::vector<std::string>& strings, double threshold, double drate, int max_time) {
    auto start_time = std::chrono::steady_clock::now();
    std::string best_solution;
    int best_score = 0;
    double best_time = 0.0;

    std::cout << "Score: " << best_score << ", Time: " << std::fixed << std::setprecision(12) << best_time << std::endl;

    while (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::steady_clock::now() - start_time).count() < max_time) {
        // Fase de construcción
        std::string solution = construct_greedy_randomized_solution(strings, drate);

        // Fase de búsqueda local
        auto [local_solution, score] = local_search(solution, strings, threshold);

        if (score > best_score) {
            best_solution = local_solution;
            best_score = score;
            best_time = std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::steady_clock::now() - start_time).count();
            std::cout << "New solution found" << std::endl;
            std::cout << "Score: " << best_score << ", Time: " << std::fixed << std::setprecision(12) << best_time << std::endl;
        }
    }

    return { best_solution, best_score, best_time };
}

int hamming_distance(const std::string& s1, const std::string& s2, double threshold) {
    int hd = 0;
    for (size_t i = 0; i < s1.size(); ++i) {
        if (s1[i] != s2[i]) {
            ++hd;
        }
    }
    if (static_cast<double>(hd) / s1.size() >= threshold) {
        return 1;
    } else {
        return 0;
    }
}

double evaluate_solution(const std::vector<std::string>& solution, const std::vector<std::string>& strings, double threshold) {
    int score = 0;
    for (const auto& s : strings) {
        score += hamming_distance(solution, s, threshold);
    }
    return score;
}

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

int main() {
    std::vector<double> score;
    std::string path = "datasets/";
    std::vector<std::string> archivos_aux;
    
    for (const auto& entry : fs::directory_iterator(path)) {
        if (entry.path().extension() == ".txt" && entry.path().filename() != "readme.txt" entry.path().filename() != "test.txt") {
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
        cont++;
        for (const auto& archivo : archivos) {
            auto strings = read_instance(archivo);
            auto solution = grasp(strings, 0.8, 0.95, 10); // Ejemplo de valores para threshold y drate
            score.push_back(evaluate_solution(solution, strings, 0.5));
        }
        double media = average(score, strings[0].size());
        std::cout << std::string(50, '-') << std::endl;
        std::cout << "dataset: " << nombre << std::endl;
        std::cout << "average: " << media << std::endl;
        double sd = standard_deviation(score, average(score, strings[0].size()), strings[0].size());
        std::cout << "standard deviation: " << sd << std::endl;
        std::cout << std::string(50, '-') << std::endl;
    }

    return 0;
}