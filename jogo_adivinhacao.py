import tkinter as tk
import random

def jogar():
    numero_secreto = random.randint(1, 100)
    
    # Função para verificar a tentativa
    def verificar():
        tentativa = entrada.get()
        if tentativa.isdigit():  # Verifica se a entrada é um número
            tentativa = int(tentativa)
            if tentativa == numero_secreto:
                resultado.config(text=f"Você acertou! O número era {numero_secreto}.", fg="green")
                desativar_entrada()
            elif tentativa < numero_secreto:
                resultado.config(text="Tente um número maior.", fg="blue")
            else:
                resultado.config(text="Tente um número menor.", fg="blue")
        else:
            resultado.config(text="Por favor, insira um número válido.", fg="red")
    
    # Função para desativar entrada e botão após vitória
    def desativar_entrada():
        entrada.config(state="disabled")
        botao.config(state="disabled")

    # Configurações da janela
    janela = tk.Tk()
    janela.title("Jogo de Adivinhação")
    janela.geometry("400x300")
    janela.configure(bg="#2c3e50")

    # Estilos
    estilo_label = {"font": ("Arial", 14), "bg": "#2c3e50", "fg": "#ecf0f1"}
    estilo_botao = {"font": ("Arial", 12, "bold"), "bg": "#3498db", "fg": "#ecf0f1", 
                    "activebackground": "#2980b9", "activeforeground": "#ecf0f1"}

    # Label de instruções
    instrucoes = tk.Label(janela, text="Adivinhe um número entre 1 e 100", **estilo_label)
    instrucoes.pack(pady=20)

    # Campo de entrada para o número
    entrada = tk.Entry(janela, font=("Arial", 16), justify="center")
    entrada.pack(pady=10)

    # Botão de adivinhar
    botao = tk.Button(janela, text="Adivinhar", command=verificar, **estilo_botao)
    botao.pack(pady=10)

    # Label de resultado
    resultado = tk.Label(janela, text="", **estilo_label)
    resultado.pack(pady=20)

    janela.mainloop()

# Executa o jogo se o arquivo for executado diretamente
if __name__ == "__main__":
    jogar()
