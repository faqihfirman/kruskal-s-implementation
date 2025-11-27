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


    def register_road_proposal(self, u, v, distance_km, cost_rp, benefit_score):
        
        if benefit_score == 0: benefit_score = 0.001

        if self.mode == 'distance':
            weight = distance_km 
        elif self.mode == 'cost':
            weight = cost_rp    
        else:
            weight = cost_rp / benefit_score 
        
        self.potential_roads.append({
            'u': u,
            'v': v,
            'weight': weight,           
            'real_cost': cost_rp,       
            'real_benefit': benefit_score, 
            'distance': distance_km     
        })

    def optimize_network_budget(self):
        solver = KruskalSolver(self.total_villages, self.potential_roads)
        mst_edges = solver.find_mst()
        
        summary = {
            'total_cost': 0, 
            'total_benefit': 0,
            'total_distance': 0 
        }
        
        for edge in mst_edges:
            summary['total_cost'] += edge['real_cost']
            summary['total_benefit'] += edge['real_benefit']
            summary['total_distance'] += edge['distance'] 
            
        return mst_edges, summary