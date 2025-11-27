import random
from .kruskal import KruskalSolver
from .union_find import UnionFind

class RoadNetworkOptimizer:
    def __init__(self, village_names, optimization_mode='ratio'):
     
        self.village_names = village_names
        self.total_villages = len(village_names)
        self.potential_roads = []
        self.mode = optimization_mode 
        
        self.village_coordinates = {
            i: (random.randint(5, 95), random.randint(5, 95)) 
            for i in range(self.total_villages)
        }

    def register_road_proposal(self, u, v, cost, benefit=1):
       
        if benefit == 0: benefit = 0.001
        
        if self.mode == 'distance':
            weight = cost
        else:
            weight = cost / benefit
        
        self.potential_roads.append({
            'u': u,
            'v': v,
            'weight': weight,      
            'real_cost': cost,      
            'real_benefit': benefit 
        })

    def optimize_network_budget(self):
        solver = KruskalSolver(self.total_villages, self.potential_roads)
        mst_edges = solver.find_mst()
        
        summary = {'total_cost': 0, 'total_benefit': 0}
        for edge in mst_edges:
            summary['total_cost'] += edge['real_cost']
            summary['total_benefit'] += edge['real_benefit']
            
        return mst_edges, summary