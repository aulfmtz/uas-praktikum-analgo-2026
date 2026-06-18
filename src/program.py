import csv
import time
import math
import os

from programGreedy import Greedy
from programACO import ACO
from programEksak import Eksak

BIAYA_SERVER_PER_MS = 50.0
RASIO_PENUH = 0.05
RASIO_KOSONG = 0.01

def load_data(jarak_file, berat_file, skenario_file):
    skenario = {}
    with open(skenario_file, mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 2:
                skenario[row[0].strip()] = float(row[1])
    
    berat_paket = {}
    total_berat = 0.0
    with open(berat_file, mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 2:
                nama_lokasi = row[0].strip()
                berat = float(row[1])
                berat_paket[nama_lokasi] = berat
                total_berat += berat

    nodes = []
    matrix = []
    with open(jarak_file, mode='r') as f:
        reader = csv.reader(f)
        header = next(reader)
        nodes = [col.strip() for col in header[1:]]

        for row in reader:
            jarak_row = []
            for val in row[1:]:
                v = val.strip().lower()
                if v == 'inf' or v == '':
                    jarak_row.append(float('inf'))
                else:
                    jarak_row.append(float(v))
            matrix.append(jarak_row)

    n = len(nodes)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]

    # Pastikan jarak dari sebuah lokasi ke dirinya sendiri selalu 0
    for i in range(n):
        matrix[i][i] = 0.0

    return nodes, matrix, berat_paket, total_berat, skenario

def calculate_fuel(best_path, matrix, nodes, berat_paket, total_berat):
    total_fuel = 0.0
    current_weight = total_berat
    selisih_rasio = RASIO_PENUH - RASIO_KOSONG

    for i in range(len(best_path) - 1):
        u = best_path[i]
        v = best_path[i + 1]
        jarak = matrix[u][v]

        rasio_saat_ini = RASIO_KOSONG + (selisih_rasio * (current_weight / total_berat))
        total_fuel += (jarak * rasio_saat_ini)

        if v != 0:
            nama_lokasi = nodes[v]
            current_weight -= berat_paket.get(nama_lokasi, 0)

    return total_fuel

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    jarak_file = os.path.join(base_dir, 'data', 'matriks_jarak.csv')
    berat_file = os.path.join(base_dir, 'data', 'berat_paket.csv')
    skenario_file = os.path.join(base_dir, 'data', 'skenario_ekonomi.csv')

    try:
        nodes, matrix, berat_paket, total_berat, skenario = load_data(jarak_file, berat_file, skenario_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return


    daftar_algoritma = [
        ("GREEDY (Heuristik Cepat)", Greedy(nodes, matrix, berat_paket, total_berat, RASIO_PENUH, RASIO_KOSONG)),
        ("ACO (Metaheuristik)", ACO(nodes, matrix, berat_paket, total_berat, RASIO_PENUH, RASIO_KOSONG, num_ants=20, iterations=50)),
        ("DFS PRUNING (Eksak)", Eksak(nodes, matrix, berat_paket, total_berat, RASIO_PENUH, RASIO_KOSONG))
    ]

    for nama_algo, solver in daftar_algoritma:
        print(f">>> {nama_algo}...")
        
        start_time = time.perf_counter()
        best_path_indices, min_dist = solver.solve()
        end_time = time.perf_counter()

        waktu_eksekusi_ms = (end_time - start_time) * 1000
        biaya_komputasi = waktu_eksekusi_ms * BIAYA_SERVER_PER_MS
        best_path_names = [nodes[i] for i in best_path_indices]
        
        total_fuel = calculate_fuel(best_path_indices, matrix, nodes, berat_paket, total_berat)

        print("\n==========================================================")
        print(f"      HASIL OPTIMASI RUTE : {nama_algo} ")
        print("==========================================================")
        print(f"Rute Terbaik  : {' -> '.join(best_path_names)}")
        print(f"Total Jarak   : {min_dist:.2f} km")
        print(f"Waktu Eksekusi: {waktu_eksekusi_ms:.4f} milidetik")
        print(f"BBM Terpakai  : {total_fuel:.4f} Liter")
        print("----------------------------------------------------------")

        for nama_skenario, harga_bbm in skenario.items():
            biaya_bbm = total_fuel * harga_bbm
            tco = biaya_komputasi + biaya_bbm
            print(f"[{nama_skenario.upper()}] - Harga BBM Rp {harga_bbm:,.0f}/L")
            print(f"  Biaya Server (Komputasi) : Rp {biaya_komputasi:,.2f}")
            print(f"  Biaya BBM Rute           : Rp {biaya_bbm:,.2f}")
            print(f"  TOTAL COST OF OWNERSHIP  : Rp {tco:,.2f}\n")
        
        print("**********************************************************\n")

if __name__ == "__main__":
    main()