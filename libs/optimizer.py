import random
from kruskal import KruskalSolver

class RoadNetworkOptimizer:
    def __init__(self, village_names):
        self.village_names = village_names
        self.total_villages = len(village_names)
        self.potential_roads = []
        
        self.village_coordinates = {
            i: (random.randint(0, 100), random.randint(0, 100)) 
            for i in range(self.total_villages)
        }

    def register_road_proposal(self, u, v, construction_cost, economic_impact):
        if economic_impact == 0: economic_impact = 0.00001
     
        efficiency_ratio = construction_cost / economic_impact
        
        road_data = {
            'u': u,
            'v': v,
            'weight': efficiency_ratio, 
            'real_cost': construction_cost,
            'real_benefit': economic_impact
        }
        
        self.potential_roads.append(road_data)

    def optimize_network_budget(self):
        solver = KruskalSolver(self.total_villages, self.potential_roads)
        mst_edges = solver.find_mst()
        summary = {'total_cost': 0, 'total_benefit': 0}
        
        for edge in mst_edges:
            summary['total_cost'] += edge['real_cost']
            summary['total_benefit'] += edge['real_benefit']
            
        return mst_edges, summary