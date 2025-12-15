import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import copy

BOX_SIZE = 0.6          
NODE_WIDTH = BOX_SIZE * 3
H_SPACE = 4.0       
V_SPACE = 3.5       

class Node:
    def __init__(self, data, level, fval, parent=None):
        self.data = data
        self.level = level
        self.fval = fval
        self.parent = parent  

    def generate_child(self):
        x, y = self.find(self.data, 0)
        val_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        children = []
        for i in val_list:
            child_data = self.shuffle(self.data, x, y, i[0], i[1])
            if child_data is not None:
                child_node = Node(child_data, self.level + 1, 0, parent=self) 
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        if x2 >= 0 and x2 < 3 and y2 >= 0 and y2 < 3:
            temp_puz = copy.deepcopy(puz)
            temp_puz[x1][y1] = temp_puz[x2][y2]
            temp_puz[x2][y2] = 0
            return temp_puz
        else:
            return None

    def find(self, puz, x):
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j

class Puzzle:
    def __init__(self, size):
        self.n = size
        self.open = []
        self.closed = []

    def h(self, start, goal):
        temp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if start[i][j] != 0 and start[i][j] != goal[i][j]:
                    target_x, target_y = -1, -1
                    for k in range(self.n):
                        for l in range(self.n):
                            if goal[k][l] == start[i][j]:
                                target_x, target_y = k, l
                    temp += abs(target_x - i) + abs(target_y - j)
        return temp

    def f(self, start, goal):
        return self.h(start.data, goal) + start.level

    def process(self, start_matrix, goal_matrix):
        start = Node(start_matrix, 0, 0, parent=None)
        start.fval = self.f(start, goal_matrix)
        self.open.append(start)
        
        visited_hashes = set() 
        
        print("\nĐang tìm đường tối ưu (chỉ hiển thị các bước đúng)...")
        
        while True:
            if not self.open:
                return None
            cur = self.open[0]
            for i in self.open:
                if i.fval < cur.fval:
                    cur = i
            if self.h(cur.data, goal_matrix) == 0:
                path = []
                while cur is not None:
                    path.append(cur)
                    cur = cur.parent
                return path[::-1] 
            self.open.remove(cur)
            cur_tuple = tuple(tuple(row) for row in cur.data)
            visited_hashes.add(cur_tuple)

            for i in cur.generate_child():
                child_tuple = tuple(tuple(row) for row in i.data)
                if child_tuple in visited_hashes: 
                    continue
                
                i.fval = self.f(i, goal_matrix)
                self.open.append(i)
def draw_node(ax, state, x, y, g, h, note=""):
    for i in range(3): 
        for j in range(3): 
            rect_x = x + j * BOX_SIZE
            rect_y = y - i * BOX_SIZE 
            
            face_color = 'white' if state[i][j] != 0 else '#f0f0f0' 
            
            ax.add_patch(Rectangle((rect_x, rect_y), BOX_SIZE, BOX_SIZE, 
                                   fill=True, facecolor=face_color, edgecolor='black', lw=1.5))
            
            if state[i][j] != 0:
                ax.text(rect_x + BOX_SIZE/2, rect_y + BOX_SIZE/2, str(state[i][j]),
                        fontsize=12, weight="bold", ha='center', va='center') 
    text_y = y + BOX_SIZE + 0.15 
    text_x = x + NODE_WIDTH / 2
    label = f"Step {g}\nh={h}, f={g+h}"
    if note: label += f"\n{note}"
        
    ax.text(text_x, text_y, label, fontsize=10, color='darkblue', ha='center', va='bottom')

def connect(ax, parent_pos, child_pos, is_break_line=False):
    px, py = parent_pos
    cx, cy = child_pos
    
    if is_break_line:
        ax.plot([px + NODE_WIDTH/2, cx + NODE_WIDTH/2], 
                [py - 2.2*BOX_SIZE, cy + 1.2*BOX_SIZE], 
                color="red", linewidth=1.5, linestyle="--", zorder=0)
    else:
        start_x, start_y = px + NODE_WIDTH / 2, py - 2 * BOX_SIZE 
        end_x, end_y = cx + NODE_WIDTH / 2, cy + BOX_SIZE 
        ax.arrow(start_x, start_y, end_x - start_x, end_y - start_y, 
                 head_width=0.15, color='red', length_includes_head=True, zorder=10)

if __name__ == "__main__":
    goal_state = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
    
    print("--- 8-PUZZLE: SOLUTION PATH ONLY ---")
    user_input = input("Nhập 9 số (Enter để chạy bài mẫu đẹp): ")
    
    if not user_input.strip():
        start_state = [[1, 2, 3],[0, 4, 6],[7, 5, 8]] 
    else:
        nums = list(map(int, user_input.split()))
        start_state = [nums[0:3], nums[3:6], nums[6:9]]

    puz = Puzzle(3)
    path = puz.process(start_state, goal_state)

    if not path:
        print("Không tìm thấy đường đi!")
        exit()

    steps = len(path)
    cols_per_row = 5
    
    rows = (steps // cols_per_row) + 1
    if steps % cols_per_row == 0: rows -= 1

    fig_width = cols_per_row * 3.0
    fig_height = rows * 3.5
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")
    ax.set_aspect('equal')
    plt.title(f"LỜI GIẢI TỐI ƯU: {steps-1} BƯỚC DI CHUYỂN", fontsize=16, color='red', pad=20)

    start_draw_x = 0
    start_draw_y = rows * V_SPACE
    positions = [] 

    for idx, node in enumerate(path):
        row_idx = idx // cols_per_row
        col_idx = idx % cols_per_row
        
        pos_x = start_draw_x + col_idx * H_SPACE
        pos_y = start_draw_y - row_idx * V_SPACE
        positions.append((pos_x, pos_y))
        
        h_val = puz.h(node.data, goal_state)
        
        note_txt = ""
        if idx == 0: note_txt = "(BẮT ĐẦU)"
        elif h_val == 0: note_txt = "(ĐÍCH)"
        
        draw_node(ax, node.data, pos_x, pos_y, node.level, h_val, note_txt)
        
        if idx > 0:
            parent_pos = positions[idx-1]
            is_break = (col_idx == 0) 
            connect(ax, parent_pos, (pos_x, pos_y), is_break_line=is_break)

    plt.tight_layout()
    plt.show()