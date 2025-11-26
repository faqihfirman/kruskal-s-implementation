import matplotlib.pyplot as plt
import networkx as nx

class NetworkVisualizer:
    
    @staticmethod
    def _draw_nodes_and_labels(optimizer, G, ax=None):
        coords = optimizer.village_coordinates
        village_names = optimizer.village_names
        
        draw_target = ax if ax else plt
        
        for i in range(optimizer.total_villages):
            G.add_node(i)
        
        nx.draw_networkx_nodes(G, coords, node_size=800, node_color='#3498db', edgecolors='black', ax=ax)
        labels = {i: name for i, name in enumerate(village_names)}
        nx.draw_networkx_labels(G, coords, labels, font_size=9, font_weight='bold',  font_color='white', ax=ax)

    @staticmethod
    def initial_graph(optimizer):
        
        plt.figure(figsize=(12, 8))
        G = nx.Graph()
        coords = optimizer.village_coordinates
        
        for road in optimizer.potential_roads:
            u, v = road['u'], road['v']
            x_values = [coords[u][0], coords[v][0]]
            y_values = [coords[u][1], coords[v][1]]
            
            plt.plot(x_values, y_values, c='#34495e', linewidth=1.5, zorder=1, alpha=0.6)
            
            mid_x = sum(x_values) / 2
            mid_y = sum(y_values) / 2
            info = f"{road['real_cost']}/{road['real_benefit']}"
            plt.text(mid_x, mid_y, info, fontsize=7, color='#34495e', 
                     ha='center', va='center', bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=0.5))

        NetworkVisualizer._draw_nodes_and_labels(optimizer, G)
        
        plt.title("KONDISI AWAL: Semua Proposal Jalan Masuk", fontsize=15)
        plt.suptitle("Format Label: Biaya / Benefit", fontsize=10, color='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

   
    @staticmethod
    def solution_graph(optimizer, selected_roads):

        plt.figure(figsize=(12, 8))
        G = nx.Graph()
        coords = optimizer.village_coordinates
        
        for road in optimizer.potential_roads:
            u, v = road['u'], road['v']
            x_values = [coords[u][0], coords[v][0]]
            y_values = [coords[u][1], coords[v][1]]
            plt.plot(x_values, y_values, c='lightgray', linestyle='--', zorder=1, alpha=0.5)

        for road in selected_roads:
            u, v = road['u'], road['v']
            x_values = [coords[u][0], coords[v][0]]
            y_values = [coords[u][1], coords[v][1]]
            
            plt.plot(x_values, y_values, c='#2ecc71', linewidth=3, zorder=2)
            
            mid_x = sum(x_values) / 2
            mid_y = sum(y_values) / 2
            info = f"Rp{road['real_cost']}\n(Ben:{road['real_benefit']})"
            plt.text(mid_x, mid_y, info, fontsize=8, color='darkgreen', 
                     ha='center', va='center', weight='bold',
                     bbox=dict(facecolor='white', alpha=0.9, edgecolor='#2ecc71', boxstyle='round,pad=0.3'))

        NetworkVisualizer._draw_nodes_and_labels(optimizer, G)
        
        plt.title("SOLUSI OPTIMAL: Rencana Pembangunan Jalan (MST)", fontsize=15)
        plt.axis('off')
        plt.tight_layout()
        plt.show()