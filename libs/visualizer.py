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
            
            dist_val = road.get('distance', 0)
            
            info = f"Jarak: {dist_val} km\nBiaya: {cost_str}\nBen: {road['real_benefit']}"
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
            
            dist_val = road.get('distance', 0)
            
            info = f"Jarak: {dist_val} km\nBiaya: {cost_str}\nBen: {road['real_benefit']}"
            
            plt.text(mid_x, mid_y, info, fontsize=8, color='darkgreen', 
                     ha='center', va='center', weight='bold',
                     bbox=dict(facecolor='white', alpha=1.0, edgecolor=mst_edge_color, boxstyle='round,pad=0.4'))

        NetworkVisualizer._draw_nodes_and_labels(G, pos, optimizer.village_names, node_color=node_color)
        
        plt.title(title, fontsize=16, pad=20, fontweight=title_weight)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def print_report(optimizer, mst_result, stats, currency_code="IDR"):
       
        total_proposals = len(optimizer.potential_roads)
        total_built = len(mst_result)
        total_distance = sum(item.get('distance', 0) for item in mst_result)
        formatted_total_cost = NetworkVisualizer._format_currency(stats['total_cost'], currency_code)
        
        
        current_mode = getattr(optimizer, 'mode', 'ratio') 
        
        if current_mode == 'distance':
            label_weight = "Weight (Km)"
            note_text = "*Note: Mode DISTANCE (Mencari total jarak terpendek)"
        elif current_mode == 'cost':
            label_weight = "Weight (Rp)"
            note_text = "*Note: Mode COST (Mencari biaya termurah tanpa peduli benefit)"
        else:
            label_weight = "Ratio (C/B)"
            note_text = "*Note: Mode RATIO (Semakin kecil rasio = Semakin Efisien)"

        print(f"\n{'='*95}")
        print(f"LAPORAN KEPUTUSAN PEMBANGUNAN JALAN DESA (MODE: {current_mode.upper()})")
        print(f"{'='*95}")
        print(f"Total Usulan Masuk   : {total_proposals} ruas")
        print(f"Total Jalan Dibangun : {total_built} ruas")
        print(f"Total Panjang Jalan  : {total_distance} km")
        print(f"Total Anggaran       : {formatted_total_cost}")
        print(f"Total Dampak Ekonomi : {stats['total_benefit']} Poin")
        print("-" * 95)
        
        print(f"{'Rute Terpilih':<30} | {'Jarak':<10} | {'Biaya':<12} | {'Benefit':<8} | {label_weight:<12}")
        print("-" * 95)

        for item in mst_result:
            u_name = optimizer.village_names[item['u']]
            v_name = optimizer.village_names[item['v']]
            nama_rute = f"{u_name} <--> {v_name}"
            
            cost_str = NetworkVisualizer._format_currency(item['real_cost'], currency_code)
            
            dist_val = item.get('distance', 0)
            dist_str = f"{dist_val} km" if dist_val > 0 else "-"
            
            print(f"{nama_rute:<30} | {dist_str:<10} | {cost_str:<12} | {item['real_benefit']:<8} | {item['weight']:.2f}")

        print("-" * 95)
        print(note_text) 