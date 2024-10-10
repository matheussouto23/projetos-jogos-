import tkinter as tk

def jogar():
    palavra_secreta = "python"
    letras_acertadas = ["_" for _ in palavra_secreta]
    tentativas = 6

    def atualizar_palavra():
        return " ".join(letras_acertadas)

    def verificar_letra():
        letra = entrada_letra.get()
        if letra in palavra_secreta:
            for i, char in enumerate(palavra_secreta):
                if char == letra:
                    letras_acertadas[i] = letra
        else:
            nonlocal tentativas
            tentativas -= 1
            tentativas_label.config(text=f"Tentativas restantes: {tentativas}")

        palavra_label.config(text=atualizar_palavra())
        if "_" not in letras_acertadas:
            resultado_label.config(text="Você venceu!", fg="green")
        elif tentativas == 0:
            resultado_label.config(text=f"Você perdeu! A palavra era {palavra_secreta}.", fg="red")
    
    janela = tk.Tk()
    janela.title("Jogo da Forca")

    palavra_label = tk.Label(janela, text=atualizar_palavra(), font=("Arial", 16))
    palavra_label.pack(pady=10)

    tentativas_label = tk.Label(janela, text=f"Tentativas restantes: {tentativas}")
    tentativas_label.pack(pady=5)

    entrada_letra = tk.Entry(janela)
    entrada_letra.pack(pady=5)

    botao = tk.Button(janela, text="Verificar Letra", command=verificar_letra)
    botao.pack(pady=5)

    resultado_label = tk.Label(janela, text="")
    resultado_label.pack(pady=10)

    janela.mainloop()
