import csv
import time
import math
import os


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
        next(reader)
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

    return nodes, matrix, berat_paket, total_berat, skenario


class TSPExactSolver:
    def __init__(self, nodes, matrix):
        self.nodes = nodes
        self.matrix = matrix
        self.num_nodes = len(nodes)

        self.min_distance = float('inf')
        self.best_path = []

    def solve(self):
        visited = [False] * self.num_nodes
        visited[0] = True
        current_path = [0]

        self._dfs(0, 1, 0.0, visited, current_path)
        return self.best_path, self.min_distance
    
    def _dfs(self, curr_node,  visited_count, current_dist, visited, path):
        if current_dist >= self.min_distance:
            return 
        
        if visited_count == self.num_nodes:
            dist_to_hub = self.matrix[curr_node][0]
            if dist_to_hub != float('inf'):
                total_dist = current_dist + dist_to_hub
                if total_dist < self.min_distance:
                    self.min_distance = total_dist
                    self.best_path = path[:] + [0]
            return
        
        for next_node in range(self.num_nodes):
            dist_to_next = self.matrix[curr_node][next_node]
            if not visited[next_node] and dist_to_next != float('inf'):
                visited[next_node] = True
                path.append(next_node)

                self._dfs(next_node, visited_count + 1, current_dist + dist_to_next, visited, path)

                visited[next_node] = False
                path.pop()

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

    print("Memuat data CSV....")

    try:
        nodes, matrix, berat_paket, total_berat, skenario = load_data(jarak_file, berat_file, skenario_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Pastikan semua nama file CSV benar dan file CSV ada di folder yang benar")
        return

    print("Data berhasil dimuat.")

    print("Memulai pencarian rute eksask dengan algoritma DFS Pruning")
    solver = TSPExactSolver(nodes, matrix)

    start_time = time.perf_counter()
    best_path_indices, min_dist = solver.solve()
    end_time = time.perf_counter()

    waktu_eksekusi_ms = (end_time - start_time) * 1000
    biaya_komputasi = waktu_eksekusi_ms * BIAYA_SERVER_PER_MS

    best_path_names = [nodes[i] for i in best_path_indices]
    total_fuel = calculate_fuel(best_path_indices, matrix, nodes, berat_paket, total_berat)

    print("\n==========================================================")
    print("      HASIL OPTIMASI RUTE (EXACT ALGORITHM)              ")
    print("==========================================================")
    print(f"Rute Terbaik : {' -> '.join(best_path_names)}")
    print(f"Total Jarak  : {min_dist} km")
    print(f"Waktu Eksekusi: {waktu_eksekusi_ms:.4f} milidetik")
    print(f"BBM Terpakai : {total_fuel:.4f} Liter")
    print("----------------------------------------------------------")

    for nama_skenario, harga_bbm in skenario.items():
        biaya_bbm = total_fuel * harga_bbm
        tco = biaya_komputasi + biaya_bbm
        print(f"\n[SKENARIO: {nama_skenario.upper()}] - Harga BBM Rp {harga_bbm:,.0f}/L")
        print(f"  Biaya Server (Komputasi) : Rp {biaya_komputasi:,.2f}")
        print(f"  Biaya BBM Rute           : Rp {biaya_bbm:,.2f}")
        print(f"  TOTAL COST OF OWNERSHIP  : Rp {tco:,.2f}")

if __name__ == "__main__":
    main()