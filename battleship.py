import tkinter as tk
from tkinter import messagebox

class BattleshipGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Batalha Naval")
        
        self.board_size = 5
        self.player_boards = [[['O'] * self.board_size for _ in range(self.board_size)] for _ in range(2)]
        self.current_player = 0
        self.ships_sunk = [0, 0]
        
        self.ships = {
            4: 1,  # 1 navio de 4 quadrados
            3: 2,  # 2 navios de 3 quadrados
            2: 3,  # 3 navios de 2 quadrados
            1: 4   # 4 navios de 1 quadrado
        }
        
        self.setup_ui()

    def setup_ui(self):
        self.start_frame = tk.Frame(self.master)
        self.start_frame.pack()

        self.start_label = tk.Label(self.start_frame, text="Clique em 'Iniciar' para posicionar seus navios.")
        self.start_label.pack()

        self.start_button = tk.Button(self.start_frame, text="Iniciar", command=self.setup_positioning)
        self.start_button.pack()

    def setup_positioning(self):
        self.start_frame.pack_forget()
        self.positioning_frame = tk.Frame(self.master)
        self.positioning_frame.pack()

        self.positioning_label = tk.Label(self.positioning_frame, text=f"Jogador {self.current_player + 1}, posicione seus navios:")
        self.positioning_label.pack()

        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ship_size_var = tk.StringVar(value='1')
        self.orientation_var = tk.StringVar(value='horizontal')

        for i in range(self.board_size):
            for j in range(self.board_size):
                btn = tk.Button(self.positioning_frame, text='O', width=4, height=2,
                                command=lambda row=i, col=j: self.place_ship(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.ship_selector = tk.OptionMenu(self.positioning_frame, self.ship_size_var, *self.ships.keys())
        self.ship_selector.pack()

        self.orientation_selector = tk.OptionMenu(self.positioning_frame, self.orientation_var, 'horizontal', 'vertical')
        self.orientation_selector.pack()

        self.finish_button = tk.Button(self.positioning_frame, text="Finalizar Posicionamento", command=self.finish_positioning)
        self.finish_button.pack()

    def place_ship(self, row, col):
        ship_size = int(self.ship_size_var.get())
        orientation = self.orientation_var.get()

        if self.can_place_ship(row, col, ship_size, orientation):
            if orientation == 'horizontal':
                for i in range(ship_size):
                    self.player_boards[self.current_player][row][col + i] = 'S'  # 'S' para navio
                    self.buttons[row][col + i].config(text='S', bg='blue')
            else:
                for i in range(ship_size):
                    self.player_boards[self.current_player][row + i][col] = 'S'
                    self.buttons[row + i][col].config(text='S', bg='blue')
        else:
            messagebox.showwarning("Aviso", "Não é possível posicionar o navio aqui.")

    def can_place_ship(self, row, col, size, orientation):
        if orientation == 'horizontal':
            if col + size > self.board_size:
                return False
            for i in range(size):
                if self.player_boards[self.current_player][row][col + i] == 'S':
                    return False
        else:
            if row + size > self.board_size:
                return False
            for i in range(size):
                if self.player_boards[self.current_player][row + i][col] == 'S':
                    return False
        return True

    def finish_positioning(self):
        self.current_player += 1
        if self.current_player < 2:
            self.positioning_label.config(text=f"Jogador {self.current_player + 1}, posicione seus navios:")
            for i in range(self.board_size):
                for j in range(self.board_size):
                    self.buttons[i][j].config(text='O', bg='SystemButtonFace')
            self.ship_size_var.set('1')
            self.orientation_var.set('horizontal')
        else:
            self.positioning_frame.pack_forget()
            self.start_battle()

    def start_battle(self):
        self.battle_frame = tk.Frame(self.master)
        self.battle_frame.pack()

        self.battle_label = tk.Label(self.battle_frame, text=f"Jogador 1, é sua vez de atacar!")
        self.battle_label.pack()

        self.battle_buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                btn = tk.Button(self.battle_frame, text='O', width=4, height=2,
                                command=lambda row=i, col=j: self.attack(row, col))
                btn.grid(row=i, column=j)
                self.battle_buttons[i][j] = btn

    def attack(self, row, col):
        enemy_board = self.player_boards[1 - self.current_player]
        if enemy_board[row][col] == 'O':
            enemy_board[row][col] = 'X'  # Marcar como erro
            self.battle_buttons[row][col].config(text='X', bg='red')
            self.battle_label.config(text=f"Jogador {self.current_player + 2}, é sua vez de atacar!")
            self.current_player = 1 - self.current_player
        elif enemy_board[row][col] == 'S':
            enemy_board[row][col] = 'H'  # Marcar como acerto
            self.battle_buttons[row][col].config(text='H', bg='green')
            self.check_sink(row, col)
            self.battle_label.config(text=f"Jogador {self.current_player + 2}, é sua vez de atacar!")
            self.current_player = 1 - self.current_player

        self.check_game_over()

    def check_sink(self, row, col):
        sunk = True
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.player_boards[1 - self.current_player][i][j] == 'S':
                    sunk = False
                    break
        if sunk:
            self.ships_sunk[self.current_player] += 1
            messagebox.showinfo("Navio Afundado", f"Jogador {self.current_player + 1} afundou um navio do Jogador {self.current_player + 2}!")

    def check_game_over(self):
        if self.ships_sunk[0] == sum(self.ships.values()) or self.ships_sunk[1] == sum(self.ships.values()):
            winner = 1 if self.ships_sunk[0] == sum(self.ships.values()) else 2
            messagebox.showinfo("Fim do Jogo", f"Jogador {winner} venceu!")
            self.ask_restart()  # Pergunta para reiniciar o jogo

    def ask_restart(self):
        if messagebox.askyesno("Reiniciar", "Deseja jogar novamente?"):
            self.restart_game()
        else:
            self.master.quit()

    def restart_game(self):
        self.player_boards = [[['O'] * self.board_size for _ in range(self.board_size)] for _ in range(2)]
        self.current_player = 0
        self.ships_sunk = [0, 0]
        self.setup_ui()  # Reinicia a interface

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipGame(root)
    root.mainloop()
