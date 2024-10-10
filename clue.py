import tkinter as tk
from tkinter import ttk
from random import shuffle

# Classe para o jogador
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_cards(self, cards):
        self.cards.extend(cards)

# Classe principal do jogo
class ClueGame:
    def __init__(self):
        self.players = []
        self.rooms = ["Cozinha", "Salão de festas", "Biblioteca", "Sala de estar", "Sala de jantar", "Conservatório", "Salão de jogos", "Hall", "Estufa"]
        self.weapons = ["Faca", "Candelabro", "Revolver", "Corda", "Cno de chumbo", "Chave inglesa"]
        self.characters = ["Srta. Scarlet", "Coronel Mustard", "Professor Plum", "Reverendo Green", "Sra. White", "Sra. Peacock"]
        self.solution = {}  # Envelope secreto
        self.all_cards = self.rooms + self.weapons + self.characters

    def add_player(self, player_name):
        self.players.append(Player(player_name))

    def set_solution(self):
        shuffle(self.rooms)
        shuffle(self.weapons)
        shuffle(self.characters)

        self.solution = {
            "room": self.rooms.pop(),
            "weapon": self.weapons.pop(),
            "character": self.characters.pop()
        }

        print(f'Solução: {self.solution}')  # Exibe a solução no console (opcional)

    def distribute_cards(self):
        num_players = len(self.players)

        if num_players == 0:
            print("Erro: Nenhum jogador adicionado! Adicione jogadores antes de distribuir as cartas.")
            return

        remaining_cards = self.rooms + self.weapons + self.characters
        shuffle(remaining_cards)

        cards_per_player = len(remaining_cards) // num_players
        for i, card in enumerate(remaining_cards):
            self.players[i % num_players].add_cards([card])

# Classe para a interface gráfica (GUI)
class ClueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clue Game")
        self.root.configure(bg="#2C3E50")  # Cor de fundo
        self.game = ClueGame()
        self.current_player_index = 0  # Índice do jogador atual

        # Estilos
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.configure('TLabel', background="#2C3E50", foreground="#ECF0F1", font=('Helvetica', 12))
        
        # Interface para adicionar jogadores
        self.title_label = ttk.Label(root, text="Bem-vindo ao Clue Game!")
        self.title_label.pack(pady=20)

        self.player_name_label = ttk.Label(root, text="Nome do Jogador:")
        self.player_name_label.pack()

        self.player_name_entry = ttk.Entry(root, font=('Helvetica', 12), width=20)
        self.player_name_entry.pack(pady=5)

        self.add_player_button = ttk.Button(root, text="Adicionar Jogador", command=self.add_player)
        self.add_player_button.pack(pady=5)

        self.distribute_button = ttk.Button(root, text="Distribuir Cartas", command=self.distribute_cards)
        self.distribute_button.pack(pady=10)

        self.players_frame = tk.Frame(root, bg="#34495E")
        self.players_frame.pack(pady=10)

        self.player_buttons = []

        self.suggestion_label = ttk.Label(root, text="Clique nas suas cartas para fazer uma sugestão:")
        self.suggestion_label.pack(pady=10)

        self.suggestion_frame = tk.Frame(root, bg="#34495E")
        self.suggestion_frame.pack()

        self.suggestion_cards = []
        self.selected_cards = {"character": None, "weapon": None, "room": None}  # Armazenar cartas selecionadas
        self.selected_buttons = {"character": None, "weapon": None, "room": None}  # Armazenar botões selecionados

        self.suggest_button = ttk.Button(root, text="Fazer Sugestão", command=self.display_suggestion_options)
        self.suggest_button.pack(pady=10)

        self.final_suggestion_button = ttk.Button(root, text="Sugestão Final", command=self.final_suggestion)
        self.final_suggestion_button.pack(pady=10)

    def add_player(self):
        player_name = self.player_name_entry.get()
        if player_name:
            self.game.add_player(player_name)
            print(f"Jogador {player_name} adicionado.")
            self.player_name_entry.delete(0, tk.END)

            player_button = ttk.Button(self.players_frame, text=f"Ver cartas de {player_name}", command=lambda: self.show_cards(player_name))
            player_button.pack(pady=5)
            self.player_buttons.append(player_button)
        else:
            print("Erro: Nome do jogador não pode estar vazio.")

    def distribute_cards(self):
        self.game.set_solution()
        self.game.distribute_cards()
        self.update_turn_display()

    def show_cards(self, player_name):
        player = next((p for p in self.game.players if p.name == player_name), None)
        if player:
            self.show_card_selection(player)

    def show_card_selection(self, player):
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        for card in player.cards:
            button = ttk.Button(self.suggestion_frame, text=card, command=lambda c=card: self.select_card(c))
            button.pack(side=tk.LEFT, padx=10, pady=5)

    def select_card(self, card):
        category = self.get_card_category(card)
        if category:
            self.selected_cards[category] = card  # Armazena a carta selecionada
            self.highlight_selected_card(category)  # Destaca o botão da carta selecionada
            print(f"{category.capitalize()} selecionada: {card}")

    def highlight_selected_card(self, category):
        # Remove destaque do botão anterior, se existir
        if self.selected_buttons[category]:
            self.selected_buttons[category].config(style='TButton')  # Remove o destaque

        # Destaca o botão da carta selecionada
        button = next((b for b in self.suggestion_frame.winfo_children() if b.cget("text") == self.selected_cards[category]), None)
        if button:
            button.config(style='Highlighted.TButton')  # Aplica o estilo de destaque
            self.selected_buttons[category] = button  # Armazena o botão selecionado

    def get_card_category(self, card):
        if card in self.game.characters:
            return "character"
        elif card in self.game.weapons:
            return "weapon"
        elif card in self.game.rooms:
            return "room"
        return None

    def display_suggestion_options(self):
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        character_frame = tk.Frame(self.suggestion_frame, bg="#34495E")
        weapon_frame = tk.Frame(self.suggestion_frame, bg="#34495E")
        room_frame = tk.Frame(self.suggestion_frame, bg="#34495E")

        character_frame.pack(side=tk.LEFT, padx=10)
        weapon_frame.pack(side=tk.LEFT, padx=10)
        room_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(character_frame, text="Personagens").pack()
        for character in self.game.characters:
            button = ttk.Button(character_frame, text=character, command=lambda c=character: self.select_card(c))
            button.pack(pady=5)

        ttk.Label(weapon_frame, text="Armas").pack()
        for weapon in self.game.weapons:
            button = ttk.Button(weapon_frame, text=weapon, command=lambda w=weapon: self.select_card(w))
            button.pack(pady=5)

        ttk.Label(room_frame, text="Cômodos").pack()
        for room in self.game.rooms:
            button = ttk.Button(room_frame, text=room, command=lambda r=room: self.select_card(r))
            button.pack(pady=5)

        confirm_button = ttk.Button(self.suggestion_frame, text="Confirmar Sugestão", command=self.make_suggestion)
        confirm_button.pack(pady=10)

    def make_suggestion(self):
        if all(self.selected_cards.values()):  # Verifica se todas as cartas foram selecionadas
            print(f"Sugestão: {self.selected_cards}")
            self.show_opponent_suggestion(self.selected_cards)
            self.reset_selected_cards()  # Reseta as cartas selecionadas após a sugestão
            self.update_turn_display()  # Atualiza o turno após a sugestão
        else:
            print("Selecione uma carta de cada categoria para fazer uma sugestão.")

    def show_opponent_suggestion(self, suggestion):
        suggestion_window = tk.Toplevel(self.root)
        suggestion_window.title("Sugestão do Oponente")
        ttk.Label(suggestion_window, text="Seu oponente sugeriu:").pack(pady=5)

        for card in suggestion.values():
            ttk.Label(suggestion_window, text=card).pack()

        opponent = self.game.players[1]  # Supondo que o jogador 2 é o segundo jogador
        matching_cards = [card for card in opponent.cards if card in suggestion.values()]

        if matching_cards:
            ttk.Label(suggestion_window, text=f"{opponent.name} mostrou uma carta: {matching_cards[0]}").pack(pady=5)
        else:
            ttk.Label(suggestion_window, text=f"{opponent.name} não tem cartas correspondentes.").pack(pady=5)

    def reset_selected_cards(self):
        self.selected_cards = {"character": None, "weapon": None, "room": None}
        self.selected_buttons = {"character": None, "weapon": None, "room": None}

    def update_turn_display(self):
        current_player = self.game.players[self.current_player_index]
        print(f"É a vez de: {current_player.name}")

    def final_suggestion(self):
        # Lógica para a sugestão final
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ClueApp(root)
    root.mainloop()
