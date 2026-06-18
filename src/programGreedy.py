class Greedy:
    def __init__(self, nodes, matrix, berat_paket, total_berat, rasio_penuh, rasio_kosong):
        self.nodes = nodes
        self.matrix = matrix
        self.num_nodes = len(nodes)
        
        self.berat_paket = berat_paket
        self.total_berat = total_berat
        
        self.rasio_penuh = rasio_penuh
        self.rasio_kosong = rasio_kosong

    def solve(self):
        unvisited = set(range(1, self.num_nodes))
        curr = 0
        jalur = [0]
        
        berat = self.total_berat
        total_jarak = 0.0
        selisih_rasio = self.rasio_penuh - self.rasio_kosong

        while unvisited:
            curr_rasio = self.rasio_kosong + (selisih_rasio * (berat / self.total_berat))
            
            next = None
            harga_min = float('inf')
            best_jarak = 0.0

            for next_node in unvisited:
                jarak = self.matrix[curr][next_node]
                if jarak == float('inf'):
                    continue
                
                bbm = jarak * curr_rasio
                
                if bbm < harga_min:
                    harga_min = bbm
                    next = next_node
                    best_jarak = jarak

            jalur.append(next)
            total_jarak += best_jarak
            curr = next
            unvisited.remove(next)
            
            lokasi = self.nodes[next]
            if lokasi in self.berat_paket:
                berat -= self.berat_paket[lokasi]

        jarak_pulang = self.matrix[curr][0]
        total_jarak += jarak_pulang
        jalur.append(0)

        return jalur, total_jarak