import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import networkx as nx 
import random
import math
import numpy as np
# ==========================================
# PHẦN 1: LOGIC GRAPH & COLORING (OOP)
# ==========================================

class GraphColoring:
    def __init__(self, num_nodes, num_colors):
        self.n = num_nodes
        self.max_colors = num_colors
        self.adj_matrix = np.zeros((self.n, self.n), dtype=int)
        self.node_positions = {}
        self.node_colors = {}
        self.labels = [str(i) for i in range(self.n)]
        self.palette = [
            'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 
            'orange', 'purple', 'lime', 'pink', 'teal', 'lavender', 'brown'
        ]
        
    def generate_random_graph(self, edge_prob=0.4):
        self.adj_matrix = np.zeros((self.n, self.n), dtype=int)
        self.node_colors = {i: 'white' for i in range(self.n)}
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if random.random() < edge_prob:
                    self.adj_matrix[i][j] = 1
                    self.adj_matrix[j][i] = 1
        center_x, center_y = 0.5, 0.5
        radius = 0.4
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[i] = (x, y)

    def solve_greedy(self):
        result_mapping = {} 
        for node in range(self.n):
            neighbor_colors = set()
            for neighbor in range(self.n):
                if self.adj_matrix[node][neighbor] == 1 and neighbor in result_mapping:
                    neighbor_colors.add(result_mapping[neighbor])
            color_idx = 0
            while color_idx in neighbor_colors:
                color_idx += 1
            result_mapping[node] = color_idx
            if color_idx < len(self.palette):
                self.node_colors[node] = self.palette[color_idx]
            else:
                self.node_colors[node] = 'gray' 
                
            yield node 
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)
app_graph = None 

def draw_graph(highlight_node=None):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')
    
    pos = app_graph.node_positions
    adj = app_graph.adj_matrix
    n = app_graph.n
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i][j] == 1:
                x_values = [pos[i][0], pos[j][0]]
                y_values = [pos[i][1], pos[j][1]]
                ax.plot(x_values, y_values, color='black', lw=1, zorder=1)
    for i in range(n):
        x, y = pos[i]
        color = app_graph.node_colors[i]
        edge_c = 'black'
        line_w = 1
        if i == highlight_node:
            edge_c = 'red'
            line_w = 3
        circle = plt.Circle((x, y), 0.04, facecolor=color, edgecolor=edge_c, linewidth=line_w, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(i), fontsize=12, ha='center', va='center', weight='bold', zorder=3)
    status = "Đồ thị ngẫu nhiên"
    if highlight_node is not None:
        status = f"Đang tô màu đỉnh {highlight_node}..."
    ax.set_title(f"Tô màu đồ thị (Greedy Algorithm)\n{status}", fontsize=14)
    
    fig.canvas.draw()

def run_coloring(event):
    steps = app_graph.solve_greedy()
    
    for node_idx in steps:
        draw_graph(highlight_node=node_idx)
        plt.pause(0.5) 
        
    draw_graph(highlight_node=None)
    ax.set_title("Đã tô màu xong!", fontsize=14, color='green')

def new_random_graph(event):
    app_graph.generate_random_graph()
    draw_graph()
if __name__ == "__main__":
    print("--- DEMO TÔ MÀU ĐỒ THỊ (GRAPH COLORING) ---")
    try:
        n_input = int(input("Nhập số lượng đỉnh (Ví dụ: 6, 8, 10): "))
    except:
        n_input = 6
        print("-> Input sai, dùng mặc định n=6")
    app_graph = GraphColoring(num_nodes=n_input, num_colors=4)
    app_graph.generate_random_graph(edge_prob=0.4) 
    ax_run = plt.axes([0.2, 0.05, 0.25, 0.075])
    btn_run = Button(ax_run, 'Bắt đầu Tô', color='lightblue', hovercolor='0.9')
    btn_run.on_clicked(run_coloring)
    ax_new = plt.axes([0.55, 0.05, 0.25, 0.075])
    btn_new = Button(ax_new, 'Random Graph', color='lightgreen', hovercolor='0.9')
    btn_new.on_clicked(new_random_graph)

    draw_graph()
    plt.show()