from .union_find import UnionFind

class KruskalSolver:
    def __init__(self, num_nodes, edges):
        self.num_nodes = num_nodes
        self.edges = edges

    def find_mst(self):
        sorted_edges = sorted(self.edges, key=lambda x: x['weight'])

        mst_result = []
        unionf_find = UnionFind(self.num_nodes)
        edge_count = 0

        for edge in sorted_edges:
            u ,v = edge['u'], edge['v']

            if unionf_find.union(u, v):
                mst_result.append(edge)
                edge_count += 1

                if edge_count == self.num_nodes - 1:
                    break

        return mst_result

            
                
        
