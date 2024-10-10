import tkinter as tk

class Checkers:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        
        self.board = self.create_board()
        self.selected_piece = None
        
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def create_board(self):
        # Criação de um tabuleiro 8x8
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = "black"  # Peças pretas
                    elif row > 4:
                        board[row][col] = "red"    # Peças vermelhas
        return board

    def draw_board(self):
        # Desenha o tabuleiro e as peças
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                
                # Cor do quadrado
                color = "white" if (row + col) % 2 == 0 else "brown"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                
                # Desenha as peças
                piece = self.board[row][col]
                if piece:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=piece)

    def on_canvas_click(self, event):
        col = event.x // 50
        row = event.y // 50

        if self.selected_piece:
            src_row, src_col = self.selected_piece
            if self.move_piece(src_row, src_col, row, col):
                self.selected_piece = None
        else:
            if self.board[row][col] is not None:
                self.selected_piece = (row, col)

        self.draw_board()

    def move_piece(self, src_row, src_col, dest_row, dest_col):
        piece_color = self.board[src_row][src_col]

        # Verifica se o movimento é válido
        if self.is_valid_move(src_row, src_col, dest_row, dest_col):
            mid_row = (src_row + dest_row) // 2
            mid_col = (src_col + dest_col) // 2
            
            if abs(dest_row - src_row) == 2:  # Captura
                self.board[mid_row][mid_col] = None  # Remove a peça capturada
                
            self.board[dest_row][dest_col] = piece_color
            self.board[src_row][src_col] = None  # Remove a peça original
            return True
            
        return False

    def is_valid_move(self, src_row, src_col, dest_row, dest_col):
        piece_color = self.board[src_row][src_col]
        
        # Verifica se a peça existe
        if piece_color is None:
            return False

        # Lógica para movimento normal
        if piece_color == "black":
            if dest_row == src_row + 1 and (dest_col == src_col - 1 or dest_col == src_col + 1):
                return True
            if dest_row == src_row + 2 and (dest_col == src_col - 2 or dest_col == src_col + 2):
                return self.can_capture(src_row, src_col, dest_row, dest_col)
        elif piece_color == "red":
            if dest_row == src_row - 1 and (dest_col == src_col - 1 or dest_col == src_col + 1):
                return True
            if dest_row == src_row - 2 and (dest_col == src_col - 2 or dest_col == src_col + 2):
                return self.can_capture(src_row, src_col, dest_row, dest_col)

        return False

    def can_capture(self, src_row, src_col, dest_row, dest_col):
        mid_row = (src_row + dest_row) // 2
        mid_col = (src_col + dest_col) // 2
        
        # Verifica se há uma peça adversária a ser capturada
        if self.board[mid_row][mid_col] and self.board[mid_row][mid_col] != self.board[src_row][src_col]:
            return True
        
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = Checkers(root)
    root.mainloop()
