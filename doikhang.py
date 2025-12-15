import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
import math
import copy

class TicTacToeGame:
    def __init__(self, n=3):
        self.n = n
        self.board = [['' for _ in range(n)] for _ in range(n)]
        self.current_turn = 'X'
        self.game_over = False
        self.winner = None

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_turn
            if self.check_winner(self.current_turn):
                self.game_over = True
                self.winner = self.current_turn
            elif self.is_full():
                self.game_over = True
                self.winner = "Draw"
            else:
                # Đổi lượt
                self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            return True
        return False

    def check_winner(self, player):
        n = self.n
        b = self.board
        
        for r in range(n):
            if all(b[r][c] == player for c in range(n)): return True
            
        for c in range(n):
            if all(b[r][c] == player for r in range(n)): return True
            
        if all(b[i][i] == player for i in range(n)): return True
        
        if all(b[i][n-1-i] == player for i in range(n)): return True
        
        return False

    def is_full(self):
        return all(cell != '' for row in self.board for cell in row)
    
    def get_empty_cells(self):
        cells = []
        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] == '':
                    cells.append((r, c))
        return cells

class AIPlayer:
    def __init__(self, player_symbol='O', n=3):
        self.symbol = player_symbol
        self.opponent = 'X' if player_symbol == 'O' else 'O'
        self.n = n
        self.max_depth = 9 if n == 3 else 4 

    def minimax(self, game_board, depth, is_maximizing, alpha, beta):
        if self.check_win_static(game_board, self.symbol): return 10 - depth
        if self.check_win_static(game_board, self.opponent): return depth - 10
        if self.is_full_static(game_board): return 0
        if depth >= self.max_depth: return 0 

        if is_maximizing:
            max_eval = -math.inf
            for r, c in self.get_moves_static(game_board):
                game_board[r][c] = self.symbol
                eval = self.minimax(game_board, depth + 1, False, alpha, beta)
                game_board[r][c] = ''
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break 
            return max_eval
        else:
            min_eval = math.inf
            for r, c in self.get_moves_static(game_board):
                game_board[r][c] = self.opponent
                eval = self.minimax(game_board, depth + 1, True, alpha, beta)
                game_board[r][c] = ''
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

    def get_best_move(self, current_board_obj):
        board_copy = copy.deepcopy(current_board_obj)
        best_score = -math.inf
        best_move = None
        
        moves = self.get_moves_static(board_copy)
        
        if self.n == 3 and len(moves) >= 8 and board_copy[1][1] == '':
            return (1, 1)

        print("AI đang suy nghĩ (Minimax + Alpha Beta)...")
        
        for r, c in moves:
            board_copy[r][c] = self.symbol
            score = self.minimax(board_copy, 0, False, -math.inf, math.inf)
            board_copy[r][c] = '' 
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
        return best_move

    def check_win_static(self, b, p):
        n = self.n
        lines = []
        lines.extend([row for row in b])
        lines.extend([[b[r][c] for r in range(n)] for c in range(n)]) 
        lines.append([b[i][i] for i in range(n)]) 
        lines.append([b[i][n-1-i] for i in range(n)]) 
        
        for line in lines:
            if all(x == p for x in line): return True
        return False

    def is_full_static(self, b):
        return all(c != '' for r in b for c in r)

    def get_moves_static(self, b):
        return [(r, c) for r in range(self.n) for c in range(self.n) if b[r][c] == '']

fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.2)
game = None
ai = None

def draw_board():
    ax.clear()
    n = game.n
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.axis('off')
    
    rect = Rectangle((0,0), n, n, fill=False, color='black', lw=3)
    ax.add_patch(rect)
    
    for i in range(1, n):
        ax.plot([i, i], [0, n], color='black', lw=1) 
        ax.plot([0, n], [i, i], color='black', lw=1) 

    # 2. Vẽ X và O
    for r in range(n):
        for c in range(n):
            symbol = game.board[r][c]
            if symbol != '':
                x_pos = c + 0.5
                y_pos = (n - 1 - r) + 0.5
                
                color = 'red' if symbol == 'X' else 'blue'
                ax.text(x_pos, y_pos, symbol, 
                        fontsize=40 - (n*3), 
                        ha='center', va='center', 
                        color=color, weight='bold')

    if game.game_over:
        if game.winner == "Draw":
            msg = "HÒA CỜ!"
            col = "gray"
        else:
            msg = f"NGƯỜI CHƠI {game.winner} CHIẾN THẮNG!"
            col = "red" if game.winner == 'X' else "blue"
    else:
        turn_msg = "Lượt của bạn (X)" if game.current_turn == 'X' else "Máy đang nghĩ..."
        msg = f"Tic-Tac-Toe {n}x{n}\n{turn_msg}"
        col = "black"
        
    ax.set_title(msg, fontsize=14, color=col, pad=10)
    fig.canvas.draw()

def on_click(event):
    if game.game_over or event.inaxes != ax:
        return
    
    if game.current_turn == 'X': 
        n = game.n
        col = int(event.xdata)
        row = n - 1 - int(event.ydata)
        
        if 0 <= row < n and 0 <= col < n:
            success = game.make_move(row, col)
            if success:
                draw_board()
                if not game.game_over:
                    plt.pause(0.1) 
                    ai_turn()

def ai_turn():
    if game.game_over: return
    
    move = ai.get_best_move(game.board)
    if move:
        game.make_move(move[0], move[1])
        draw_board()

def restart(event):
    global game, ai
    game = TicTacToeGame(game.n) 
    ai = AIPlayer('O', game.n)
    draw_board()

if __name__ == "__main__":
    print("--- TIC TAC TOE (MINIMAX + ALPHA BETA) ---")
    print("Chọn kích thước bàn cờ:")
    print("1. Cổ điển (3x3) - AI Bất bại")
    print("2. Mở rộng (4x4) - Thử thách")
    print("3. Khó (5x5) - Cần chuỗi 5")
    
    choice = input("Nhập lựa chọn (1/2/3, mặc định 1): ").strip()
    
    size = 3
    if choice == '2': size = 4
    elif choice == '3': size = 5
    
    game = TicTacToeGame(n=size)
    ai = AIPlayer('O', n=size)
    
    ax_restart = plt.axes([0.4, 0.05, 0.2, 0.075])
    btn_restart = Button(ax_restart, 'Chơi lại', color='lightgreen', hovercolor='0.975')
    btn_restart.on_clicked(restart)
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    
    draw_board()
    plt.show()