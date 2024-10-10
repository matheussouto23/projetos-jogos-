import tkinter as tk
import random

# Emojis para representar Pedra, Papel e Tesoura
emoji_opcoes = {'pedra': '🪨', 'papel': '📄', 'tesoura': '✂️'}

def jogar_rodada(escolha_jogador):
    opcoes = ['pedra', 'papel', 'tesoura']
    escolha_computador = random.choice(opcoes)
    
    # Atualizando os resultados com emojis
    resultado_computador.config(text=f"🤖 Computador escolheu: {emoji_opcoes[escolha_computador]}")
    resultado_jogador.config(text=f"👤 Você escolheu: {emoji_opcoes[escolha_jogador]}")

    if escolha_jogador == escolha_computador:
        resultado_final.config(text="😐 Empate!", fg="orange")
    elif (escolha_jogador == 'pedra' and escolha_computador == 'tesoura') or \
         (escolha_jogador == 'papel' and escolha_computador == 'pedra') or \
         (escolha_jogador == 'tesoura' and escolha_computador == 'papel'):
        resultado_final.config(text="🎉 Você ganhou!", fg="green")
    else:
        resultado_final.config(text="💔 Você perdeu!", fg="red")

# Criando a janela principal
janela = tk.Tk()
janela.title("Pedra, Papel, Tesoura")
janela.geometry("300x400")
janela.config(bg="lightblue")

# Label para escolher opção
label = tk.Label(janela, text="Escolha uma opção:", font=('Arial', 16, 'bold'), bg="lightblue")
label.pack(pady=20)

# Botões de opções (Pedra, Papel, Tesoura) com emojis
botao_pedra = tk.Button(janela, text="🪨 Pedra", font=('Arial', 14), command=lambda: jogar_rodada('pedra'), width=15)
botao_pedra.pack(pady=10)

botao_papel = tk.Button(janela, text="📄 Papel", font=('Arial', 14), command=lambda: jogar_rodada('papel'), width=15)
botao_papel.pack(pady=10)

botao_tesoura = tk.Button(janela, text="✂️ Tesoura", font=('Arial', 14), command=lambda: jogar_rodada('tesoura'), width=15)
botao_tesoura.pack(pady=10)

# Labels para mostrar o resultado do jogador e do computador
resultado_jogador = tk.Label(janela, text="", font=('Arial', 12), bg="lightblue")
resultado_jogador.pack(pady=10)

resultado_computador = tk.Label(janela, text="", font=('Arial', 12), bg="lightblue")
resultado_computador.pack(pady=10)

# Label para mostrar o resultado final (Ganhou, Perdeu, Empate)
resultado_final = tk.Label(janela, text="", font=('Arial', 16, 'bold'), bg="lightblue")
resultado_final.pack(pady=20)

# Iniciando o loop principal da janela
janela.mainloop()
