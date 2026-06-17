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

