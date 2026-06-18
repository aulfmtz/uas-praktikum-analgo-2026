class Eksak:
    def __init__(self, nodes, matrix, berat_paket, total_berat, rasio_penuh, rasio_kosong):
        self.nodes = nodes
        self.matrix = matrix
        self.num_nodes = len(nodes)
        
        # Tambahan parameter dari inisialisasi seperti class Greedy Anda
        self.berat_paket = berat_paket
        self.total_berat = total_berat
        self.rasio_penuh = rasio_penuh
        self.rasio_kosong = rasio_kosong

        # Kita ubah orientasi optimasinya menjadi mencari FUEL terkecil
        self.min_fuel = float('inf') 
        self.best_path = []
        self.best_distance = 0.0 # Menyimpan jarak dari rute paling hemat bensin

    def solve(self):
        visited = [False] * self.num_nodes
        visited[0] = True  # Mulai dari Hub
        current_path = [0]

        # Parameter DFS ditambah: current_fuel dan current_weight
        self._dfs(0, 1, 0.0, 0.0, self.total_berat, visited, current_path)
        
        return self.best_path, self.best_distance
    
    def _dfs(self, curr_node, visited_count, current_dist, current_fuel, current_weight, visited, path):
        # PRUNING BERDASARKAN BENSIN: 
        # Jika bensin sementara sudah melebihi rekor bensin terhemat, potong cabang ini!
        if current_fuel >= self.min_fuel:
            return 
        
        # Base Case: Jika semua node sudah dikunjungi
        if visited_count == self.num_nodes:
            dist_to_hub = self.matrix[curr_node][0]
            if dist_to_hub != float('inf'):
                # Hitung rasio untuk pulang ke Hub (biasanya sisa beban = 0)
                selisih_rasio = self.rasio_penuh - self.rasio_kosong
                rasio_saat_ini = self.rasio_kosong + (selisih_rasio * (current_weight / self.total_berat))
                fuel_to_hub = dist_to_hub * rasio_saat_ini
                
                total_fuel = current_fuel + fuel_to_hub
                total_dist = current_dist + dist_to_hub
                
                # Cek apakah total bensin rute ini lebih irit dari rekor sebelumnya
                if total_fuel < self.min_fuel:
                    self.min_fuel = total_fuel
                    self.best_distance = total_dist
                    self.best_path = path[:] + [0]
            return
        
        # Hitung rasio BBM di titik saat ini (sebelum berangkat ke node berikutnya)
        selisih_rasio = self.rasio_penuh - self.rasio_kosong
        rasio_saat_ini = self.rasio_kosong + (selisih_rasio * (current_weight / self.total_berat))
        
        # Eksplorasi tetangga
        for next_node in range(self.num_nodes):
            dist_to_next = self.matrix[curr_node][next_node]
            
            if not visited[next_node] and dist_to_next != float('inf'):
                # Kalkulasi konsumsi bensin untuk step ini (Persis seperti Greedy)
                fuel_cost = dist_to_next * rasio_saat_ini
                
                # Simulasikan drop paket
                nama_lokasi = self.nodes[next_node]
                next_weight = current_weight - self.berat_paket.get(nama_lokasi, 0)
                
                visited[next_node] = True
                path.append(next_node)

                # Panggil rekursi dengan membawa state beban dan bensin terbaru
                self._dfs(next_node, visited_count + 1, current_dist + dist_to_next, current_fuel + fuel_cost, next_weight, visited, path)

                # Backtracking
                visited[next_node] = False
                path.pop()