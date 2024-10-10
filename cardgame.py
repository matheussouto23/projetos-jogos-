import tkinter as tk
from tkinter import messagebox
import random

class Carta:
    def __init__(self, nome, elemento, ataque, defesa, vida, habilidade, custo_mana, emoji):
        self.nome = nome
        self.elemento = elemento
        self.ataque = ataque
        self.defesa = defesa
        self.vida = vida
        self.habilidade = habilidade
        self.custo_mana = custo_mana
        self.emoji = emoji
        self.usada = False  # Para rastrear se a habilidade foi usada
        self.status = None  # Efeito de status (Queimar, Congelar, etc.)

    def aplicar_efeito_status(self):
        if self.status == "Queimar":
            self.vida -= 1  # Dano ao longo do tempo
            messagebox.showinfo("Efeito de Status", f"{self.nome} está queimando! Perdeu 1 de vida.")
        elif self.status == "Congelar":
            self.defesa += 2  # Aumenta defesa temporariamente
            messagebox.showinfo("Efeito de Status", f"{self.nome} está congelado! Defesa aumentada.")
        elif self.status == "Envenenar":
            self.vida -= 2  # Dano ao longo do tempo
            messagebox.showinfo("Efeito de Status", f"{self.nome} está envenenado! Perdeu 2 de vida.")

def determinar_vantagem(carta_atacante, carta_defensora):
    vantagens = {
        "Fogo": "Terra",
        "Terra": "Água",
        "Água": "Fogo",
        "Ar": "Terra",
        "Sombra": "Luz",
        "Luz": "Sombra"
    }
    if vantagens[carta_atacante.elemento] == carta_defensora.elemento:
        return 2  # Ataque é mais forte
    elif vantagens[carta_defensora.elemento] == carta_atacante.elemento:
        return 0.5  # Defesa é mais forte
    return 1  # Sem vantagem

# Lista de cartas disponíveis
cartas_disponiveis = [
    Carta("Dragão", "Fogo", 10, 5, 15, "Golpe Crítico", 5, "🐉"),
    Carta("Mago", "Água", 8, 3, 12, "Curar", 3, "🧙"),
    Carta("Guerreiro", "Terra", 7, 4, 15, "Dano em área", 4, "⚔️"),
    Carta("Arqueiro", "Ar", 6, 2, 10, "Dano em área", 3, "🏹"),
    Carta("Espectro", "Sombra", 9, 4, 10, "Agarra", 2, "👻"),
    Carta("Gigante", "Terra", 12, 6, 20, "Destruição", 6, "🪨"),
    Carta("Elfo", "Natureza", 7, 5, 8, "Flecha Mágica", 3, "🌳"),
    Carta("Feiticeiro", "Mágico", 8, 2, 10, "Raio", 4, "🔮"),
    Carta("Bárbaro", "Fogo", 10, 4, 15, "Fúria", 5, "💥"),
    Carta("Lobisomem", "Sombra", 9, 3, 14, "Transformação", 4, "🐺"),
    Carta("Paladino", "Luz", 6, 7, 12, "Proteção", 3, "⚔️"),
    Carta("Ninja", "Sombra", 8, 1, 9, "Golpe Silencioso", 2, "🥷"),
    Carta("Necromante", "Morte", 5, 4, 8, "Reviver", 4, "💀"),
    Carta("Dragão de Gelo", "Água", 10, 4, 15, "Congelar", 5, "❄️"),
    Carta("Sereia", "Água", 6, 3, 8, "Canto Hipnótico", 3, "🐚"),
    Carta("Cavaleiro", "Terra", 7, 6, 14, "Corte Duplo", 4, "🏇"),
]

# Variáveis globais
cartas_jogador1 = []
cartas_jogador2 = []
carta_selecionada_jogador1 = None
carta_selecionada_jogador2 = None
turno = 1
mana_jogador1 = 10
mana_jogador2 = 10

# Função para escolher cartas
def escolher_cartas(jogador):
    global cartas_jogador1, cartas_jogador2

    if jogador == 1 and len(cartas_jogador1) < 3:
        selected_card = listbox_cartas.get(tk.ACTIVE)
        if selected_card:  # Verificar se alguma carta foi selecionada
            for carta in cartas_disponiveis:
                if carta.nome == selected_card and carta not in cartas_jogador1 and carta not in cartas_jogador2:
                    cartas_jogador1.append(carta)
                    listbox_cartas.delete(tk.ACTIVE)
                    break
    elif jogador == 2 and len(cartas_jogador2) < 3:
        selected_card = listbox_cartas.get(tk.ACTIVE)
        if selected_card:  # Verificar se alguma carta foi selecionada
            for carta in cartas_disponiveis:
                if carta.nome == selected_card and carta not in cartas_jogador2 and carta not in cartas_jogador1:
                    cartas_jogador2.append(carta)
                    listbox_cartas.delete(tk.ACTIVE)
                    break

    if len(cartas_jogador1) == 3 and len(cartas_jogador2) == 3:
        iniciar_jogo()

def iniciar_jogo():
    global turno, mana_jogador1, mana_jogador2
    mana_jogador1 = 10
    mana_jogador2 = 10
    turno = 1

    label_turno.config(text=f"Turno: Jogador {turno}")
    label_mana_jogador1.config(text=f"Mana Jogador 1: {mana_jogador1}")
    label_mana_jogador2.config(text=f"Mana Jogador 2: {mana_jogador2}")

    # Limpar e recriar as cartas
    atualizar_cartas()

def atualizar_cartas():
    for widget in frame_cartas_jogador1.winfo_children():
        widget.destroy()
    for widget in frame_cartas_jogador2.winfo_children():
        widget.destroy()

    # Atualiza a interface das cartas para o jogador 1
    for carta in cartas_jogador1:
        if carta.vida > 0:  # Verifica se a carta está viva
            criar_carta_interface(carta, frame_cartas_jogador1, 1)

    # Atualiza a interface das cartas para o jogador 2
    for carta in cartas_jogador2:
        if carta.vida > 0:  # Verifica se a carta está viva
            criar_carta_interface(carta, frame_cartas_jogador2, 2)

def criar_carta_interface(carta, frame, jogador):
    button = tk.Button(frame, text=f"{carta.emoji} {carta.nome}\nAtaque: {carta.ataque}\nDefesa: {carta.defesa}\nVida: {carta.vida}\nHabilidade: {carta.habilidade}",
                       font=("Arial", 12), relief=tk.RAISED, padx=10, pady=10,
                       command=lambda: selecionar_carta(carta, jogador))
    button.pack(padx=10, pady=5)

    # Desabilitar cartas já selecionadas
    if (jogador == 1 and carta in cartas_jogador1) or (jogador == 2 and carta in cartas_jogador2):
        button.config(state=tk.DISABLED)

    # Botão para usar a habilidade
    botao_usar_habilidade = tk.Button(frame, text="Usar Habilidade", 
                                       command=lambda: usar_habilidade(carta, jogador))
    botao_usar_habilidade.pack(pady=5)

def selecionar_carta(carta, jogador):
    global carta_selecionada_jogador1, carta_selecionada_jogador2
    if jogador == 1:
        carta_selecionada_jogador1 = carta
        messagebox.showinfo("Selecionar Carta", f"Jogador 1 selecionou: {carta.nome}")
    else:
        carta_selecionada_jogador2 = carta
        messagebox.showinfo("Selecionar Carta", f"Jogador 2 selecionou: {carta.nome}")

def usar_habilidade(carta, jogador):
    global mana_jogador1, mana_jogador2

    if jogador == 1 and carta.usada:
        messagebox.showwarning("Aviso", "Essa habilidade já foi usada neste turno.")
        return
    elif jogador == 2 and carta.usada:
        messagebox.showwarning("Aviso", "Essa habilidade já foi usada neste turno.")
        return

    if jogador == 1:
        mana_jogador1 -= carta.custo_mana
    else:
        mana_jogador2 -= carta.custo_mana

    if mana_jogador1 < 0 or mana_jogador2 < 0:
        messagebox.showwarning("Aviso", "Mana insuficiente para usar essa habilidade.")
        return

    # Aqui você pode adicionar a lógica específica para cada habilidade
    if carta.habilidade == "Golpe Crítico":
        messagebox.showinfo("Habilidade", f"{carta.nome} usou Golpe Crítico! Dano dobrado.")
    elif carta.habilidade == "Curar":
        carta.vida += 5
        messagebox.showinfo("Habilidade", f"{carta.nome} usou Curar! Vida aumentada para {carta.vida}.")
    elif carta.habilidade == "Dano em área":
        # Aqui você pode implementar lógica para dano em área
        messagebox.showinfo("Habilidade", f"{carta.nome} usou Dano em Área! Dano em todas as cartas inimigas.")
    elif carta.habilidade == "Congelar":
        carta.status = "Congelar"
        messagebox.showinfo("Habilidade", f"{carta.nome} usou Congelar!")
    elif carta.habilidade == "Queimar":
        carta.status = "Queimar"
        messagebox.showinfo("Habilidade", f"{carta.nome} usou Queimar!")
    elif carta.habilidade == "Envenenar":
        carta.status = "Envenenar"
        messagebox.showinfo("Habilidade", f"{carta.nome} usou Envenenar!")
    
    carta.usada = True  # Marcar habilidade como usada
    atualizar_mana()

def atualizar_mana():
    label_mana_jogador1.config(text=f"Mana Jogador 1: {mana_jogador1}")
    label_mana_jogador2.config(text=f"Mana Jogador 2: {mana_jogador2}")

def finalizar_turno():
    global turno, carta_selecionada_jogador1, carta_selecionada_jogador2

    if turno == 1:
        for carta in cartas_jogador1:
            carta.aplicar_efeito_status()
        turno = 2
    else:
        for carta in cartas_jogador2:
            carta.aplicar_efeito_status()
        turno = 1

    label_turno.config(text=f"Turno: Jogador {turno}")

    carta_selecionada_jogador1 = None
    carta_selecionada_jogador2 = None

    if not any(carta.vida > 0 for carta in cartas_jogador1):
        messagebox.showinfo("Fim de Jogo", "Jogador 2 venceu!")
        reiniciar_jogo()
    elif not any(carta.vida > 0 for carta in cartas_jogador2):
        messagebox.showinfo("Fim de Jogo", "Jogador 1 venceu!")
        reiniciar_jogo()

def reiniciar_jogo():
    global cartas_jogador1, cartas_jogador2, turno
    cartas_jogador1.clear()
    cartas_jogador2.clear()
    turno = 1
    atualizar_cartas()
    listbox_cartas.delete(0, tk.END)
    for carta in cartas_disponiveis:
        listbox_cartas.insert(tk.END, carta.nome)

# Criação da interface gráfica
root = tk.Tk()
root.title("Jogo de Cartas")

frame_cartas_jogador1 = tk.Frame(root)
frame_cartas_jogador1.pack(side=tk.LEFT, padx=10)

frame_cartas_jogador2 = tk.Frame(root)
frame_cartas_jogador2.pack(side=tk.RIGHT, padx=10)

frame_selecionar_cartas = tk.Frame(root)
frame_selecionar_cartas.pack(side=tk.TOP, pady=10)

label_turno = tk.Label(root, text="Turno: Jogador 1", font=("Arial", 14))
label_turno.pack(pady=5)

label_mana_jogador1 = tk.Label(root, text="Mana Jogador 1: 10", font=("Arial", 12))
label_mana_jogador1.pack(pady=5)

label_mana_jogador2 = tk.Label(root, text="Mana Jogador 2: 10", font=("Arial", 12))
label_mana_jogador2.pack(pady=5)

listbox_cartas = tk.Listbox(frame_selecionar_cartas, font=("Arial", 12))
listbox_cartas.pack(padx=10, pady=10)

for carta in cartas_disponiveis:
    listbox_cartas.insert(tk.END, carta.nome)

button_escolher_jogador1 = tk.Button(frame_selecionar_cartas, text="Escolher Carta Jogador 1", 
                                      command=lambda: escolher_cartas(1))
button_escolher_jogador1.pack(pady=5)

button_escolher_jogador2 = tk.Button(frame_selecionar_cartas, text="Escolher Carta Jogador 2", 
                                      command=lambda: escolher_cartas(2))
button_escolher_jogador2.pack(pady=5)

button_finalizar_turno = tk.Button(root, text="Finalizar Turno", command=finalizar_turno)
button_finalizar_turno.pack(pady=10)

root.mainloop()
