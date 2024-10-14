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

// Lee la instancia del problema desde el archivo dado
std::vector<std::string> read_instance(const std::string& file_path) {
    std::vector<std::string> strings;
    std::ifstream file(file_path);
    std::string line;
    while (std::getline(file, line)) {
        // Elimina espacios en blanco al final
        line.erase(std::remove_if(line.begin(), line.end(), ::isspace), line.end());
        if (!line.empty())
            strings.push_back(line);
    }
    return strings;
}

// Calcula la distancia de Hamming entre dos cadenas
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

// Evalúa una solución
int evaluate_solution(const std::string& solution, const std::vector<std::string>& strings, double threshold) {
    int score = 0;
    for (const auto& s : strings) {
        score += hamming_distance(solution, s, threshold);
    }
    return score;
}

// Construcción aleatoria codiciosa para FFMSP
std::string construct_greedy_randomized_solution(const std::vector<std::string>& strings, double drate) {
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

// Búsqueda local para FFMSP
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

// GRASP para FFMSP con comportamiento Any-Time
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

int main(int argc, char* argv[]) {
    // Parseo de argumentos de línea de comandos
    std::string instance;
    int max_time = 0;
    double threshold = 0.0;
    double drate = 0.9;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if ((arg == "-i" || arg == "--instance") && i + 1 < argc) {
            instance = argv[++i];
        } else if ((arg == "-t" || arg == "--time") && i + 1 < argc) {
            max_time = std::stoi(argv[++i]);
        } else if ((arg == "-th" || arg == "--threshold") && i + 1 < argc) {
            threshold = std::stod(argv[++i]);
        } else if ((arg == "-dr" || arg == "--drate") && i + 1 < argc) {
            drate = std::stod(argv[++i]);
        } else {
            std::cerr << "Unknown argument: " << arg << std::endl;
            return 1;
        }
    }

    if (instance.empty() || max_time <= 0 || threshold <= 0.0) {
        std::cerr << "Usage: " << argv[0] << " -i <instance> -t <time> -th <threshold> [-dr <drate>]" << std::endl;
        return 1;
    }

    // Lee la instancia
    std::vector<std::string> strings = read_instance(instance);

    // Ejecuta GRASP
    auto [solution, score, time_found] = grasp(strings, threshold, drate, max_time);

    std::cout << "Best solution found" << std::endl;
    std::cout << "Score: " << score << ", Time: " << std::fixed << std::setprecision(12) << time_found << std::endl;
    std::cout << "Solution: " << solution << std::endl;

    return 0;
}