import matplotlib.pyplot as plt
import networkx as nx

class NetworkVisualizer:
    
    @staticmethod
    def _get_layout(G, seed=42):

        return nx.spring_layout(G, k=5, iterations=50, seed=seed)

    @staticmethod
    def _format_currency(value, currency_code="IDR"):
 
        if value >= 1000:
            val_m = value / 1000
            return f"{currency_code} {val_m:g} M"
        else:
            return f"{currency_code} {value:g} Jt"

    @staticmethod
    def _draw_nodes_and_labels(G, pos, village_names, ax=None, node_color='#3498db'):
        draw_target = ax if ax else plt
    
        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=node_color, 
                               edgecolors='black', linewidths=1.5, ax=ax)
        
        pos_labels = {k: (v[0], v[1] - 0.08) for k, v in pos.items()}
        labels = {i: name for i, name in enumerate(village_names)}
        nx.draw_networkx_labels(G, pos_labels, labels, font_size=9, 
                                font_weight='bold', font_color='black', ax=ax)

    @staticmethod
    def initial_graph(optimizer, 
                      title="KONDISI AWAL: Semua Proposal Masuk", 
                      title_weight='normal', 
                      node_color='#3498db', 
                      currency_code="IDR"):
        
        plt.figure(figsize=(14, 9))
        
        G = nx.Graph()
        G.add_nodes_from(range(optimizer.total_villages))
        for road in optimizer.potential_roads:
            G.add_edge(road['u'], road['v'])
            
        pos = NetworkVisualizer._get_layout(G)
        
        for road in optimizer.potential_roads:
            u, v = road['u'], road['v']
            x_values = [pos[u][0], pos[v][0]]
            y_values = [pos[u][1], pos[v][1]]
            
            plt.plot(x_values, y_values, c='#34495e', linewidth=1.5, zorder=1, alpha=0.6)
            
            mid_x = sum(x_values) / 2
            mid_y = sum(y_values) / 2
            
            cost_str = NetworkVisualizer._format_currency(road['real_cost'], currency_code)
            
            info = f"Biaya: {cost_str}\nBenefit: {road['real_benefit']}"
            plt.text(mid_x, mid_y, info, fontsize=7, color='black', 
                     ha='center', va='center', 
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='#bdc3c7', boxstyle='round,pad=0.2'))

        NetworkVisualizer._draw_nodes_and_labels(G, pos, optimizer.village_names, node_color=node_color)

        plt.title(title, fontsize=16, pad=20, fontweight=title_weight)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def solution_graph(optimizer, selected_roads, 
                       title="SOLUSI OPTIMAL: MST", 
                       title_weight='bold', 
                       node_color='#3498db', 
                       mst_edge_color='#2ecc71',
                       currency_code="IDR"):
        
        plt.figure(figsize=(14, 9))
        
        G = nx.Graph()
        G.add_nodes_from(range(optimizer.total_villages))
        for road in optimizer.potential_roads:
            G.add_edge(road['u'], road['v'])
            
        pos = NetworkVisualizer._get_layout(G)
        
        for road in optimizer.potential_roads:
            u, v = road['u'], road['v']
            x_values = [pos[u][0], pos[v][0]]
            y_values = [pos[u][1], pos[v][1]]
            plt.plot(x_values, y_values, c='lightgray', linestyle='--', zorder=1, alpha=0.5)

        for road in selected_roads:
            u, v = road['u'], road['v']
            x_values = [pos[u][0], pos[v][0]]
            y_values = [pos[u][1], pos[v][1]]
            
            plt.plot(x_values, y_values, c=mst_edge_color, linewidth=3, zorder=2)
            
            mid_x = sum(x_values) / 2
            mid_y = sum(y_values) / 2
            
            cost_str = NetworkVisualizer._format_currency(road['real_cost'], currency_code)
            
            info = f"Biaya: {cost_str}\nBenefit: {road['real_benefit']}"
            
            plt.text(mid_x, mid_y, info, fontsize=8, color='darkgreen', 
                     ha='center', va='center', weight='bold',
                     bbox=dict(facecolor='white', alpha=1.0, edgecolor=mst_edge_color, boxstyle='round,pad=0.4'))

        NetworkVisualizer._draw_nodes_and_labels(G, pos, optimizer.village_names, node_color=node_color)
        
        plt.title(title, fontsize=16, pad=20, fontweight=title_weight)
        plt.axis('off')
        plt.tight_layout()
        plt.show()