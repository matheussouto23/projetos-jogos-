import subprocess
import tkinter as tk
from tkinter import ttk
import webbrowser

# Funções para abrir os jogos
def abrir_clue():
    subprocess.run(["python", "clue.py"])

def abrir_jogo_adivinhacao():
    subprocess.run(["python", "jogo_adivinhacao.py"])

def abrir_jogo_forca():
    subprocess.run(["python", "jogo_forca.py"])

def abrir_jogo_pedra_papel_tesoura():
    subprocess.run(["python", "jogo_pedra_papel_tesoura.py"])

def abrir_jogo_velha():
    subprocess.run(["python", "jogo_velha.py"])

def abrir_jogo_uno():
    subprocess.run(["python", "jogo_Uno.py"])

def abrir_jogo_xadrez():
    subprocess.run(["python", "chess.py"])

def abrir_jogo_damas():
    subprocess.run(["python", "Damas.py"])

def abrir_jogo_pc_man():
    subprocess.run(["python", "pc_man.py"])

def abrir_cardgame():
    subprocess.run(["python", "cardgame.py"])

# Função para abrir o LinkedIn
def abrir_linkedin():
    webbrowser.open("https://www.linkedin.com/in/matheus-souto-3a8448328/")

# Função para criar a janela principal com uma estilização aprimorada
def criar_janela_principal():
    janela = tk.Tk()
    janela.title("Menu Principal de Jogos")
    janela.geometry("400x600")
    janela.configure(bg="#2c3e50")  # Cor de fundo

    # Estilo de botões com o ttk
    estilo_botao = {
        "font": ("Arial", 12, "bold"),
        "width": 25,
        "bg": "#3498db",  # Cor do botão
        "fg": "#ecf0f1",  # Cor do texto
        "activebackground": "#2980b9",  # Cor do botão quando pressionado
        "activeforeground": "#ecf0f1",  # Cor do texto quando pressionado
    }

    # Label principal
    label = tk.Label(janela, text="Escolha um Jogo", font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
    label.pack(pady=20)

    # Adicionando os botões com o novo estilo
    botoes_jogos = [
        ("Clue", abrir_clue),
        ("Adivinhação", abrir_jogo_adivinhacao),
        ("Forca", abrir_jogo_forca),
        ("Pedra, Papel, Tesoura", abrir_jogo_pedra_papel_tesoura),
        ("Jogo da Velha", abrir_jogo_velha),
        ("UNO", abrir_jogo_uno),
        ("Xadrez", abrir_jogo_xadrez),
        ("Damas", abrir_jogo_damas),
        ("PC Man", abrir_jogo_pc_man),  # Chamando PC Man
        ("Card Game", abrir_cardgame),  # Chamando Card Game
    ]

    for nome, comando in botoes_jogos:
        botao = tk.Button(janela, text=nome, command=comando, **estilo_botao)
        botao.pack(pady=10)

    # Botão para sair
    botao_sair = tk.Button(janela, text="Sair", command=janela.quit, **estilo_botao)
    botao_sair.pack(pady=20)

    # Adicionando a seção do desenvolvedor
    desenvolvedor_label = tk.Label(janela, text="Desenvolvedor: Matheus Nogueira Souto", font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1")
    desenvolvedor_label.pack(pady=10)

    # Link para o LinkedIn
    linkedin_label = tk.Label(janela, text="LinkedIn", font=("Arial", 10, "underline"), fg="#3498db", bg="#2c3e50")
    linkedin_label.pack(pady=5)
    linkedin_label.bind("<Button-1>", lambda e: abrir_linkedin())  # Adiciona a funcionalidade de abrir o LinkedIn ao clicar

    janela.mainloop()

if __name__ == "__main__":
    criar_janela_principal()
