import tkinter as tk

def jogar():
    janela = tk.Tk()
    janela.title("Jogo da Velha")
    
    # Cria o tabuleiro e os botões
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    botoes = [[None for _ in range(3)] for _ in range(3)]
    
    turno = ["X"]
    
    def checar_vitoria():
        # Verifica vitória nas linhas
        for linha in tabuleiro:
            if linha[0] == linha[1] == linha[2] != " ":
                return linha[0]
        
        # Verifica vitória nas colunas
        for col in range(3):
            if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] != " ":
                return tabuleiro[0][col]
        
        # Verifica vitória nas diagonais
        if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != " ":
            return tabuleiro[0][0]
        if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != " ":
            return tabuleiro[0][2]
        
        return None
    
    def clique(x, y):
        if tabuleiro[x][y] == " ":
            tabuleiro[x][y] = turno[0]
            botoes[x][y].config(text=turno[0])
            vencedor = checar_vitoria()
            if vencedor:
                resultado.config(text=f"Jogador {vencedor} venceu!")
                desativar_botoes()
            elif all(tabuleiro[i][j] != " " for i in range(3) for j in range(3)):
                resultado.config(text="Empate!")
            else:
                turno[0] = "O" if turno[0] == "X" else "X"
    
    def desativar_botoes():
        for i in range(3):
            for j in range(3):
                botoes[i][j].config(state="disabled")
    
    # Criando os botões no grid
    for i in range(3):
        for j in range(3):
            botoes[i][j] = tk.Button(janela, text=" ", font=("Arial", 24), width=5, height=2, 
                                     command=lambda i=i, j=j: clique(i, j))
            botoes[i][j].grid(row=i, column=j)
    
    resultado = tk.Label(janela, text="")
    resultado.grid(row=3, column=0, columnspan=3)
    
    janela.mainloop()

# Garante que o código seja executado ao rodar o arquivo diretamente
if __name__ == "__main__":
    jogar()
