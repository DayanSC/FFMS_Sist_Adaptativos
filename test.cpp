#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <climits>

using namespace std;

// Función para leer el archivo de entrada
vector<string> read_input(const string& file_path) {
    vector<string> strings;
    ifstream file(file_path);
    string line;
    if (file.is_open()) {
        while (getline(file, line)) {
            // Eliminar espacios en blanco al principio y al final
            line.erase(0, line.find_first_not_of(" \t\n\r\f\v"));
            line.erase(line.find_last_not_of(" \t\n\r\f\v") + 1);
            strings.push_back(line);
        }
        file.close();
    } else {
        cerr << "No se pudo abrir el archivo: " << file_path << endl;
    }
    return strings;
}

// Función para calcular la distancia de Hamming con umbral
int hamming_distance(const string& s1, const string& s2, double threshold) {
    int hd = 0;
    int len = s1.length();
    for (int i = 0; i < len; ++i) {
        if (s1[i] != s2[i]) {
            ++hd;
        }
    }
    if (static_cast<double>(hd) / len >= threshold) {
        return 1;
    } else {
        return 0;
    }
}

// Función para contar las ocurrencias de cada carácter en una posición específica
map<char, int> count_occurrences(const vector<string>& strings, int position) {
    map<char, int> occurrences = {{'A', 0}, {'C', 0}, {'G', 0}, {'T', 0}};
    for (const auto& s : strings) {
        char c = s[position];
        if (occurrences.find(c) != occurrences.end()) {
            ++occurrences[c];
        }
    }
    return occurrences;
}

// Función para obtener el mínimo de ocurrencias en una posición
int min_occurrences(const vector<string>& strings, int position) {
    map<char, int> occurrences = count_occurrences(strings, position);
    int min_value = INT_MAX;
    for (const auto& pair : occurrences) {
        if (pair.second < min_value) {
            min_value = pair.second;
        }
    }
    return min_value;
}

// Función para determinar la posición inicial
int DetermineStartingPosition(const vector<string>& strings, bool condition) {
    int m = strings[0].length();
    vector<int> min_occs(m);
    for (int i = 0; i < m; ++i) {
        min_occs[i] = min_occurrences(strings, i);
    }
    int min_value = *min_element(min_occs.begin(), min_occs.end());
    vector<int> candidates;
    for (int i = 0; i < m; ++i) {
        if (min_occs[i] == min_value) {
            candidates.push_back(i);
        }
    }
    if (condition) {
        int index = rand() % candidates.size();
        return candidates[index];
    } else {
        return candidates[0];
    }
}

// Función para calcular la calidad de la solución
int calculate_quality(const vector<char>& result, const vector<string>& strings, double threshold) {
    int score = 0;
    string res(result.begin(), result.end());
    for (const auto& s : strings) {
        score += hamming_distance(res, s, threshold);
    }
    return score;
}

// Función para calcular la distancia de Hamming parcial
int hamming_distance_partial(const vector<char>& s1, const string& s2, double threshold) {
    int hd = 0;
    int len = s1.size();
    for (int i = 0; i < len; ++i) {
        if (s1[i] != '\0') {
            if (s1[i] != s2[i]) {
                ++hd;
            }
        }
    }
    if (static_cast<double>(hd) / len >= threshold) {
        return 1;
    } else {
        return 0;
    }
}

// Función para calcular el puntaje parcial
int f_partial(const vector<char>& S, const vector<string>& strings, double threshold) {
    int score = 0;
    for (const auto& s : strings) {
        score += hamming_distance_partial(S, s, threshold);
    }
    return score;
}

// Función para verificar si existe un carácter que mejore el puntaje
pair<bool, char> exists_a(vector<char>& S, const vector<char>& alphabet, int j, const vector<string>& strings, double threshold) {
    int current_f_partial = f_partial(S, strings, threshold);
    for (char a : alphabet) {
        vector<char> new_S = S;
        new_S[j] = a;
        int new_f_partial = f_partial(new_S, strings, threshold);
        if (new_f_partial > current_f_partial) {
            return make_pair(true, a);
        }
    }
    return make_pair(false, '\0');
}

// Función para seleccionar el carácter con mínima ocurrencia
char select_min_occurrence_char(const vector<string>& strings, int j) {
    map<char, int> occurrences = count_occurrences(strings, j);
    int min_occ = INT_MAX;
    for (const auto& pair : occurrences) {
        if (pair.second < min_occ) {
            min_occ = pair.second;
        }
    }
    for (char c : {'A', 'C', 'G', 'T'}) {
        if (occurrences[c] == min_occ) {
            return c;
        }
    }
    return 'A'; // Valor por defecto
}

// Función principal del algoritmo
vector<char> randomized_ffmsp(const vector<string>& strings, double threshold, double drate, bool random_start_position) {
    int m = strings[0].length();
    vector<char> alphabet = {'A', 'C', 'G', 'T'};
    vector<char> S(m, '\0'); // Inicializar S con caracteres nulos
    int j = DetermineStartingPosition(strings, random_start_position);
    int k = 0;
    while (k < m) {
        double r = static_cast<double>(rand()) / RAND_MAX;
        if (r <= drate) {
            auto result = exists_a(S, alphabet, j, strings, threshold);
            bool exists = result.first;
            char a = result.second;
            if (exists) {
                S[j] = a;
            } else {
                char b = select_min_occurrence_char(strings, j);
                S[j] = b;
            }
        } else {
            char a = alphabet[rand() % 4];
            S[j] = a;
        }
        j = (j + 1) % m;
        ++k;
    }
    return S;
}

int main(int argc, char* argv[]) {
    // Variables para los argumentos
    string instance_file;
    double threshold = 0.0;
    double drate = 0.0;
    bool random_start_position = false;

    // Procesar los argumentos de línea de comandos
    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];
        if ((arg == "-i" || arg == "--instance") && i + 1 < argc) {
            instance_file = argv[++i];
        } else if ((arg == "-th" || arg == "--threshold") && i + 1 < argc) {
            threshold = stod(argv[++i]);
        } else if ((arg == "-dr" || arg == "--drate") && i + 1 < argc) {
            drate = stod(argv[++i]);
        } else if (arg == "-rsp" || arg == "--randomstartposition") {
            random_start_position = true;
        } else {
            cerr << "Argumento desconocido o faltante: " << arg << endl;
            return 1;
        }
    }

    // Verificar que los argumentos requeridos estén presentes
    if (instance_file.empty() || threshold == 0.0 || drate == 0.0) {
        cerr << "Uso: " << argv[0] << " -i <archivo_instancia> -th <umbral> -dr <drate> [-rsp]" << endl;
        return 1;
    }

    // Leer las cadenas de entrada
    vector<string> strings = read_input(instance_file);
    if (strings.empty()) {
        cerr << "Error: No se pudieron leer cadenas del archivo de entrada" << endl;
        return 1;
    }

    // Inicializar el generador de números aleatorios
    srand(time(nullptr));

    // Ejecutar el algoritmo
    clock_t start_time = clock();
    vector<char> result = randomized_ffmsp(strings, threshold, drate, random_start_position);
    clock_t end_time = clock();

    // Calcular la calidad de la solución
    int quality = calculate_quality(result, strings, threshold);

    // Mostrar el resultado
    for (char c : result) {
        cout << c;
    }
    cout << endl;
    cout << quality << endl;

    return 0;
}