class Greedy:
    # Tambahkan rasio_penuh dan rasio_kosong sebagai parameter penerima
    def __init__(self, nodes, matrix, berat_paket, total_berat, rasio_penuh, rasio_kosong):
        self.nodes = nodes
        self.matrix = matrix
        self.num_nodes = len(nodes)
        
        self.berat_paket = berat_paket
        self.total_berat = total_berat
        
        # Simpan nilai yang dikirim dari program.py
        self.rasio_penuh = rasio_penuh
        self.rasio_kosong = rasio_kosong

    def solve(self):
        unvisited = set(range(1, self.num_nodes))
        current_node = 0
        path = [0]
        
        current_weight = self.total_berat
        total_distance = 0.0
        selisih_rasio = self.rasio_penuh - self.rasio_kosong

        while unvisited:
            rasio_saat_ini = self.rasio_kosong + (selisih_rasio * (current_weight / self.total_berat))
            
            best_next = None
            best_fuel_cost = float('inf')
            best_dist_step = 0.0

            for next_node in unvisited:
                jarak = self.matrix[current_node][next_node]
                if jarak == float('inf'):
                    continue
                
                fuel_cost = jarak * rasio_saat_ini
                
                if fuel_cost < best_fuel_cost:
                    best_fuel_cost = fuel_cost
                    best_next = next_node
                    best_dist_step = jarak

            path.append(best_next)
            total_distance += best_dist_step
            current_node = best_next
            unvisited.remove(best_next)
            
            nama_lokasi = self.nodes[best_next]
            current_weight -= self.berat_paket.get(nama_lokasi, 0)

        jarak_pulang = self.matrix[current_node][0]
        total_distance += jarak_pulang
        path.append(0)

        return path, total_distance