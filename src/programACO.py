import random

class ACO:
    def __init__(self, nodes, matrix, berat_paket, total_berat, rasio_penuh, rasio_kosong, num_ants=20, iterations=50):
        self.nodes = nodes
        self.matrix = matrix
        self.num_nodes = len(nodes)
        
        self.berat_paket = berat_paket
        self.total_berat = total_berat
        
        self.rasio_penuh = rasio_penuh
        self.rasio_kosong = rasio_kosong
        
        self.num_ants = num_ants
        self.iterations = iterations
        self.alpha = 1.0 
        self.beta = 2.0
        self.evaporation = 0.5
        
        self.pheromone = []
        for i in range(self.num_nodes):
            baris_baru = []
            for j in range(self.num_nodes):
                baris_baru.append(1.0)
            self.pheromone.append(baris_baru)

    def solve(self):
        jalur_terpendek = None
        min_bbm = float('inf')
        jarak = 0.0
        
        selisih_rasio = self.rasio_penuh - self.rasio_kosong

        for n in range(self.iterations):
            all_jalur = []
            
            for ant in range(self.num_ants):
                jalur = [0]
                visited = {0}
                current_node = 0
                current_weight = self.total_berat
                ant_bbm = 0.0
                ant_jarak = 0.0
                
                while len(jalur) < self.num_nodes:
                    rasio = self.rasio_kosong + (selisih_rasio * (current_weight / self.total_berat))
                    probs = []
                    total_prob = 0.0
                    
                    for next_node in range(self.num_nodes):
                        if next_node not in visited and self.matrix[current_node][next_node] != float('inf'):
                            jarak_langkah = self.matrix[current_node][next_node]
                            biaya_bbm = jarak_langkah * rasio
                            
                            eta = 1.0 / biaya_bbm if biaya_bbm > 0 else 1.0
                            tau = self.pheromone[current_node][next_node]
                            
                            p = (tau ** self.alpha) * (eta ** self.beta)
                            probs.append((next_node, p, jarak_langkah, biaya_bbm))
                            total_prob += p
                    
                    val = random.uniform(0, total_prob)
                    cumulative = 0.0
                    chosen_next = None
                    
                    for next_node, p, jrk, bbm in probs:
                        cumulative += p
                        if cumulative >= val:
                            chosen_next = next_node
                            ant_jarak += jrk
                            ant_bbm += bbm
                            break

                    # antisipasi dead end
                    if chosen_next is None:
                        ant_bbm = float('inf') 
                        break 

                    jalur.append(chosen_next)
                    visited.add(chosen_next)
                    current_node = chosen_next
                    nama_lokasi = self.nodes[chosen_next]
                    current_weight -= self.berat_paket.get(nama_lokasi, 0)
                
                if len(jalur) == self.num_nodes:
                    if self.matrix[current_node][0] != float('inf'):
                        jarak_pulang = self.matrix[current_node][0]
                        rasio_pulang = self.rasio_kosong + (selisih_rasio * (current_weight / self.total_berat))
                        ant_jarak += jarak_pulang
                        ant_bbm += (jarak_pulang * rasio_pulang)
                        jalur.append(0)
                    else:
                        ant_bbm = float('inf')
                
                all_jalur.append((jalur, ant_bbm))
                
                if ant_bbm < min_bbm:
                    min_bbm = ant_bbm
                    jalur_terpendek = jalur[:]
                    jarak = ant_jarak
            
            for i in range(self.num_nodes):
                for j in range(self.num_nodes):
                    self.pheromone[i][j] *= (1.0 - self.evaporation)
            
            for jalur_k, bbbm in all_jalur:
                deposit = 1.0 / bbbm

                for i in range(len(jalur_k) - 1):
                    u = jalur_k[i]
                    v = jalur_k[i+1]
                    self.pheromone[u][v] += deposit
                    
        return jalur_terpendek, jarak