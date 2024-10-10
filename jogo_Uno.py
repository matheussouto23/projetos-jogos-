import random
import tkinter as tk
from tkinter import messagebox

class JogoUNO:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("UNO")
        self.janela.geometry("800x600")
        self.janela.configure(bg="green")  # Cor de fundo verde para lembrar um tapete de jogo

        self.cartas = self.gerar_baralho()
        self.jogador1_cartas = []
        self.jogador2_cartas = []
        self.pilha_descarte = []
        self.pontos_jogador1 = 0
        self.pontos_jogador2 = 0
        self.turno = "jogador1"

        self.iniciar_jogo()

    def gerar_baralho(self):
        cores = ["vermelho", "azul", "verde", "amarelo"]
        valores = list(range(0, 10)) + ["+2", "Reverso", "Bloqueio"]
        baralho = []

        for cor in cores:
            for valor in valores:
                baralho.append(f"{cor} {valor}")
                if valor != 0:  # Cartas de 1 a 9 aparecem duas vezes
                    baralho.append(f"{cor} {valor}")
        baralho += ["Curinga", "Curinga +4"] * 4

        random.shuffle(baralho)
        return baralho

    def iniciar_jogo(self):
        self.jogador1_cartas = [self.cartas.pop() for _ in range(7)]
        self.jogador2_cartas = [self.cartas.pop() for _ in range(7)]
        self.pilha_descarte.append(self.cartas.pop())

        self.mostrar_estado_jogo()

    def mostrar_estado_jogo(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        # Exibir cartas do jogador ativo
        if self.turno == "jogador1":
            cartas_atual = self.jogador1_cartas
            cartas_oponente = self.jogador2_cartas
            tk.Label(self.janela, text="Suas Cartas (Jogador 1)", font=("Arial", 20), bg="green", fg="white").pack()
        else:
            cartas_atual = self.jogador2_cartas
            cartas_oponente = self.jogador1_cartas
            tk.Label(self.janela, text="Suas Cartas (Jogador 2)", font=("Arial", 20), bg="green", fg="white").pack()

        cartas_frame = tk.Frame(self.janela, bg="green")
        cartas_frame.pack(pady=10)

        for idx, carta in enumerate(cartas_atual):
            cor_carta = carta.split()[0]
            btn = tk.Button(cartas_frame, text=carta, command=lambda idx=idx: self.jogar_carta(idx),
                            bg=self.obter_cor(cor_carta), fg="white", font=("Arial", 12), width=10, height=3)
            btn.pack(side="left", padx=5)

        # Exibir cartas do oponente
        tk.Label(cartas_frame, text="Cartas do Oponente: " + str(len(cartas_oponente)), bg="green", fg="white", font=("Arial", 12)).pack(side="left", padx=5)

        carta_topo_frame = tk.Frame(self.janela, bg="green")
        carta_topo_frame.pack(pady=20)

        tk.Label(carta_topo_frame, text="Carta no topo da pilha:", font=("Arial", 18), bg="green", fg="white").pack()
        carta_topo = tk.Label(carta_topo_frame, text=self.pilha_descarte[-1], font=("Arial", 16, "bold"),
                              bg=self.obter_cor(self.pilha_descarte[-1].split()[0]), fg="white", width=10, height=3)
        carta_topo.pack()

        btn_comprar = tk.Button(self.janela, text="Comprar Carta", command=self.comprar_carta,
                                font=("Arial", 14), bg="yellow", width=15, height=2)
        btn_comprar.pack(pady=20)

        # Exibir pontos
        tk.Label(self.janela, text=f"Pontos Jogador 1: {self.pontos_jogador1}", font=("Arial", 16), bg="green", fg="white").pack(pady=5)
        tk.Label(self.janela, text=f"Pontos Jogador 2: {self.pontos_jogador2}", font=("Arial", 16), bg="green", fg="white").pack(pady=5)

    def jogar_carta(self, idx):
        if self.turno == "jogador1":
            cartas_atual = self.jogador1_cartas
        else:
            cartas_atual = self.jogador2_cartas

        carta_jogada = cartas_atual[idx]
        carta_topo = self.pilha_descarte[-1]

        if self.carta_valida(carta_jogada, carta_topo):
            self.pilha_descarte.append(carta_jogada)
            if self.turno == "jogador1":
                del self.jogador1_cartas[idx]
            else:
                del self.jogador2_cartas[idx]

            if len(cartas_atual) == 1:  # Checar se o jogador gritou UNO
                messagebox.showinfo("UNO!", "Você gritou UNO!")

            if len(cartas_atual) == 0:
                if self.turno == "jogador1":
                    self.calcular_pontos("jogador1")
                    if self.pontos_jogador1 >= 500:
                        messagebox.showinfo("UNO", "Jogador 1 venceu o jogo!")
                        self.janela.quit()
                    else:
                        messagebox.showinfo("UNO", "Jogador 1 venceu esta rodada!")
                else:
                    self.calcular_pontos("jogador2")
                    if self.pontos_jogador2 >= 500:
                        messagebox.showinfo("UNO", "Jogador 2 venceu o jogo!")
                        self.janela.quit()
                    else:
                        messagebox.showinfo("UNO", "Jogador 2 venceu esta rodada!")
                self.iniciar_jogo()
            else:
                self.turno = "jogador2" if self.turno == "jogador1" else "jogador1"
        else:
            messagebox.showerror("Movimento inválido", "Você não pode jogar essa carta.")

        self.mostrar_estado_jogo()

    def comprar_carta(self):
        if self.turno == "jogador1":
            nova_carta = self.cartas.pop()
            self.jogador1_cartas.append(nova_carta)
        else:
            nova_carta = self.cartas.pop()
            self.jogador2_cartas.append(nova_carta)

        self.turno = "jogador2" if self.turno == "jogador1" else "jogador1"
        self.mostrar_estado_jogo()

    def calcular_pontos(self, vencedor):
        if vencedor == "jogador1":
            pontos = sum(self.calcular_valor(carta) for carta in self.jogador2_cartas)
            self.pontos_jogador1 += pontos
        else:
            pontos = sum(self.calcular_valor(carta) for carta in self.jogador1_cartas)
            self.pontos_jogador2 += pontos

    def calcular_valor(self, carta):
        if "Curinga" in carta or "+4" in carta:
            return 50
        elif "+2" in carta or "Bloqueio" in carta:
            return 20
        else:
            return int(carta.split()[1])

    def carta_valida(self, carta_jogada, carta_topo):
        if "Curinga" in carta_jogada:
            return True

        cor_jogada, valor_jogado = carta_jogada.split(" ", 1)
        cor_topo, valor_topo = carta_topo.split(" ", 1)

        return cor_jogada == cor_topo or valor_jogado == valor_topo

    def obter_cor(self, cor):
        cores = {
            "vermelho": "#FF4C4C",
            "azul": "#4C4CFF",
            "verde": "#4CFF4C",
            "amarelo": "#FFFF4C",
        }
        return cores.get(cor, "gray")

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoUNO(root)
    root.mainloop()
