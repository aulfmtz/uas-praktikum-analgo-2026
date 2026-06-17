import random

class ACO:
    def __init__(self, nodes, matrix, berat_paket, total_berat, rasio_penuh, rasio_kosong, num_ants=20, iterations=50):
        self.nodes = nodes
        self.matrix = matrix
        self.num_nodes = len(nodes)
        
        self.berat_paket = berat_paket
        self.total_berat = total_berat
        
        # Simpan rasio yang dikirim dari program.py
        self.rasio_penuh = rasio_penuh
        self.rasio_kosong = rasio_kosong
        
        # Parameter ACO
        self.num_ants = num_ants
        self.iterations = iterations
        self.alpha = 1.0  # Bobot Feromon
        self.beta = 2.0   # Bobot Heuristik (BBM)
        self.evaporation = 0.5
        
        # Matriks Feromon awal
        self.pheromone = [[1.0 for _ in range(self.num_nodes)] for _ in range(self.num_nodes)]

    def solve(self):
        best_path_global = None
        min_fuel_global = float('inf')
        best_dist_global = 0.0
        
        # Gunakan atribut rasio milik class ini
        selisih_rasio = self.rasio_penuh - self.rasio_kosong

        for _ in range(self.iterations):
            all_paths = []
            
            # Setiap semut membangun rute
            for ant in range(self.num_ants):
                path = [0]
                visited = {0}
                current_node = 0
                current_weight = self.total_berat
                ant_fuel = 0.0
                ant_dist = 0.0
                
                while len(path) < self.num_nodes:
                    rasio_saat_ini = self.rasio_kosong + (selisih_rasio * (current_weight / self.total_berat))
                    
                    probs = []
                    total_prob = 0.0
                    
                    # Hitung probabilitas transisi ke kota yang belum dikunjungi
                    for next_node in range(self.num_nodes):
                        if next_node not in visited and self.matrix[current_node][next_node] != float('inf'):
                            jarak = self.matrix[current_node][next_node]
                            biaya_bbm = jarak * rasio_saat_ini
                            
                            # Heuristik ACO: 1 / biaya_bbm
                            eta = 1.0 / biaya_bbm if biaya_bbm > 0 else 1.0
                            tau = self.pheromone[current_node][next_node]
                            
                            p = (tau ** self.alpha) * (eta ** self.beta)
                            probs.append((next_node, p, jarak, biaya_bbm))
                            total_prob += p
                    
                    # Seleksi roulette wheel berdasarkan probabilitas
                    rand_val = random.uniform(0, total_prob)
                    cumulative = 0.0
                    chosen_next = None
                    
                    for next_node, p, jrk, bbm in probs:
                        cumulative += p
                        if cumulative >= rand_val:
                            chosen_next = next_node
                            ant_dist += jrk
                            ant_fuel += bbm
                            break
                    
                    # Antisipasi rounding error jika probabilitas tidak bulat
                    if chosen_next is None and probs:
                        chosen_next = probs[-1][0]
                        ant_dist += probs[-1][2]
                        ant_fuel += probs[-1][3]
                        
                    path.append(chosen_next)
                    visited.add(chosen_next)
                    current_node = chosen_next
                    nama_lokasi = self.nodes[chosen_next]
                    current_weight -= self.berat_paket.get(nama_lokasi, 0)
                
                # Semut pulang ke Hub
                jarak_pulang = self.matrix[current_node][0]
                rasio_pulang = self.rasio_kosong + (selisih_rasio * (current_weight / self.total_berat))
                ant_dist += jarak_pulang
                ant_fuel += (jarak_pulang * rasio_pulang)
                path.append(0)
                
                all_paths.append((path, ant_fuel))
                
                if ant_fuel < min_fuel_global:
                    min_fuel_global = ant_fuel
                    best_path_global = path[:]
                    best_dist_global = ant_dist
            
            # Evaporasi feromon
            for i in range(self.num_nodes):
                for j in range(self.num_nodes):
                    self.pheromone[i][j] *= (1.0 - self.evaporation)
            
            # Tambahkan feromon baru berdasarkan kualitas rute (BBM)
            for path_k, fuel in all_paths:
                deposit = 1.0 / fuel
                # Iterasi sebanyak panjang rute dikurangi 1 agar tidak out-of-bounds
                for i in range(len(path_k) - 1):
                    u = path_k[i]
                    v = path_k[i+1]
                    self.pheromone[u][v] += deposit
                    
        return best_path_global, best_dist_global