class UnionFind:
    def __init__(self, total_elements):
        self.parent = list(range(total_elements)) 
        self.rank = [1] * total_elements

    def find(self, element_id):
        if self.parent[element_id] != element_id:
            self.parent[element_id] = self.find(self.parent[element_id])

        return self.parent[element_id]
    
    def union(self, village_id_a, village_id_b):
      
        root_a = self.find(village_id_a)
        root_b = self.find(village_id_b)

        if root_a != root_b:
            if self.rank[root_a] > self.rank[root_b]:
                self.parent[root_b] = root_a
            else:
                self.parent[root_a] = root_b
                if self.rank[root_a] == self.rank[root_b]:
                    self.rank[root_b] += 1
            return True 
       
        return False