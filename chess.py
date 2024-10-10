import tkinter as tk
from tkinter import messagebox

class JogoXadrez:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Xadrez")
        
        # Configurando o tabuleiro
        self.tabuleiro = [["" for _ in range(8)] for _ in range(8)]
        self.botoes = [[None for _ in range(8)] for _ in range(8)]
        self.turno = "branco"
        self.selecionado = None
        self.casas_possiveis = []
        self.criar_tabuleiro()
        self.configurar_pecas()
    
    def criar_tabuleiro(self):
        for i in range(8):
            for j in range(8):
                cor = "white" if (i + j) % 2 == 0 else "gray"
                botao = tk.Button(self.janela, width=8, height=4, bg=cor,
                                  command=lambda i=i, j=j: self.clique_casa(i, j))
                botao.grid(row=i, column=j)
                self.botoes[i][j] = botao

    def configurar_pecas(self):
        # Peças brancas
        self.tabuleiro[0] = ['Torre_b', 'Cavalo_b', 'Bispo_b', 'Rainha_b', 'Rei_b', 'Bispo_b', 'Cavalo_b', 'Torre_b']
        self.tabuleiro[1] = ['Peao_b'] * 8

        # Peças pretas
        self.tabuleiro[7] = ['Torre_p', 'Cavalo_p', 'Bispo_p', 'Rainha_p', 'Rei_p', 'Bispo_p', 'Cavalo_p', 'Torre_p']
        self.tabuleiro[6] = ['Peao_p'] * 8
        
        self.atualizar_tabuleiro()

    def atualizar_tabuleiro(self):
        pecas_unicode = {
            'Torre_b': '♖', 'Cavalo_b': '♘', 'Bispo_b': '♗', 'Rainha_b': '♕', 'Rei_b': '♔', 'Peao_b': '♙',
            'Torre_p': '♜', 'Cavalo_p': '♞', 'Bispo_p': '♝', 'Rainha_p': '♛', 'Rei_p': '♚', 'Peao_p': '♟'
        }
        
        for i in range(8):
            for j in range(8):
                peca = self.tabuleiro[i][j]
                texto = pecas_unicode.get(peca, "")
                self.botoes[i][j].config(text=texto)

    def clique_casa(self, i, j):
        peca = self.tabuleiro[i][j]
        
        if self.selecionado:
            # Se há uma peça selecionada, tenta mover para a casa clicada
            if (i, j) != self.selecionado:  # Evita mover para a mesma casa
                self.mover_peca(i, j)
            else:
                # Caso clique novamente na mesma peça, cancela a seleção
                self.desmarcar_selecao()
        elif peca and peca.endswith(self.turno[0]):  # Verifica se a peça pertence ao jogador atual
            self.selecionar_peca(i, j)
    
    def selecionar_peca(self, i, j):
        self.selecionado = (i, j)
        # Destaca a casa selecionada mudando a cor
        self.botoes[i][j].config(bg="yellow")
        self.mostrar_casas_possiveis(i, j)
    
    def mostrar_casas_possiveis(self, i, j):
        peca = self.tabuleiro[i][j]
        casas_possiveis = []
        
        for x in range(8):
            for y in range(8):
                if self.validar_movimento(peca, i, j, x, y):
                    casas_possiveis.append((x, y))
        
        # Destaca as casas possíveis
        for x, y in casas_possiveis:
            if self.tabuleiro[x][y] == "":
                self.botoes[x][y].config(bg="lightgreen")  # Casa vazia
            else:
                self.botoes[x][y].config(bg="orange")  # Casa ocupada por uma peça do adversário
        
        self.casas_possiveis = casas_possiveis

    def desmarcar_selecao(self):
        x, y = self.selecionado
        cor = "white" if (x + y) % 2 == 0 else "gray"
        self.botoes[x][y].config(bg=cor)  # Restaura a cor original da casa
        self.selecionado = None
        
        # Restaura a cor das casas possíveis
        for x, y in self.casas_possiveis:
            cor = "white" if (x + y) % 2 == 0 else "gray"
            self.botoes[x][y].config(bg=cor)
        
        self.casas_possiveis = []

    def mover_peca(self, i, j):
        x, y = self.selecionado
        peca = self.tabuleiro[x][y]
        
        # Valida o movimento com base na peça selecionada
        if self.validar_movimento(peca, x, y, i, j):
            self.tabuleiro[i][j] = peca
            self.tabuleiro[x][y] = ""
            self.desmarcar_selecao()
            self.atualizar_tabuleiro()
            self.verificar_fim_de_turno()
        else:
            messagebox.showerror("Movimento inválido", "Esse movimento não é permitido.")
            self.desmarcar_selecao()
    
    def validar_movimento(self, peca, x, y, i, j):
        if peca.startswith('Peao'):
            return self.movimento_peao(peca, x, y, i, j)
        elif peca.startswith('Torre'):
            return self.movimento_torre(peca, x, y, i, j)
        elif peca.startswith('Cavalo'):
            return self.movimento_cavalo(peca, x, y, i, j)
        elif peca.startswith('Bispo'):
            return self.movimento_bispo(peca, x, y, i, j)
        elif peca.startswith('Rainha'):
            return self.movimento_rainha(peca, x, y, i, j)
        elif peca.startswith('Rei'):
            return self.movimento_rei(peca, x, y, i, j)
        return False
    
    def movimento_peao(self, peca, x, y, i, j):
        direcao = 1 if peca.endswith('b') else -1  # Direção do movimento invertida
        # Movimento para frente
        if x + direcao == i and y == j and not self.tabuleiro[i][j]:  # Movimento simples
            return True
        # Captura diagonal
        if x + direcao == i and abs(y - j) == 1:
            if self.tabuleiro[i][j] and self.tabuleiro[i][j].endswith('p' if peca.endswith('b') else 'b'):
                return True
        return False
    
    def movimento_torre(self, peca, x, y, i, j):
        return (x == i or y == j) and self.caminho_livre(x, y, i, j)
    
    def movimento_cavalo(self, peca, x, y, i, j):
        return (abs(x - i) == 2 and abs(y - j) == 1) or (abs(x - i) == 1 and abs(y - j) == 2)
    
    def movimento_bispo(self, peca, x, y, i, j):
        return abs(x - i) == abs(y - j) and self.caminho_livre(x, y, i, j)
    
    def movimento_rainha(self, peca, x, y, i, j):
        return (x == i or y == j or abs(x - i) == abs(y - j)) and self.caminho_livre(x, y, i, j)
    
    def movimento_rei(self, peca, x, y, i, j):
        return abs(x - i) <= 1 and abs(y - j) <= 1
    
    def caminho_livre(self, x, y, i, j):
        if x == i:  # Movimento horizontal
            step = 1 if y < j else -1
            for col in range(y + step, j, step):
                if self.tabuleiro[x][col]:
                    return False
            return True
        elif y == j:  # Movimento vertical
            step = 1 if x < i else -1
            for row in range(x + step, i, step):
                if self.tabuleiro[row][y]:
                    return False
            return True
        elif abs(x - i) == abs(y - j):  # Movimento diagonal
            step_x = 1 if i > x else -1
            step_y = 1 if j > y else -1
            row, col = x + step_x, y + step_y
            while row != i and col != j:
                if self.tabuleiro[row][col]:
                    return False
                row += step_x
                col += step_y
            return True
        return False

    def verificar_fim_de_turno(self):
        # Alterna o turno
        self.turno = "preto" if self.turno == "branco" else "branco"

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoXadrez(root)
    root.mainloop()
