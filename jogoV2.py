import tkinter as tk
from itertools import permutations
from collections import defaultdict
from spellchecker import SpellChecker
import threading
from playsound import playsound

# Verificador de palavras em português
spell = SpellChecker(language='pt')

# Sons
def tocar_som_click():
    threading.Thread(target=lambda: playsound("click.wav"), daemon=True).start()
def tocar_som_sucesso():
    threading.Thread(target=lambda: playsound("success.wav"), daemon=True).start()

# Variáveis globais
palavras_validas = set()
palavras_descobertas = set()
palavras_por_tamanho = defaultdict(set)
output_lines = []
word_positions = {}
pontuacao = 0

# Tabela de pontuação por tamanho de palavra
tabela_pontos = {4: 1, 5: 2, 6: 3, 7: 5}
# Palavras maiores que 7 letras ganham 8 pontos
def pontos_palavra(palavra):
    return tabela_pontos.get(len(palavra), 8 if len(palavra) > 7 else 0)

# Desenhar peças
def desenhar_pecas(canvas, texto):
    canvas.delete("all")
    for i, letra in enumerate(texto.upper()):
        x = 10 + i * 60
        canvas.create_rectangle(x, 10, x + 50, 60, fill="#DEB887", outline="#8B4513", width=2)
        canvas.create_text(x + 25, 35, text=letra, font=("Arial", 24, "bold"))

# Atualizar peças ao digitar
def ao_digitar(event):
    desenhar_pecas(canvas_letras, campo_texto.get())
    tocar_som_click()

# Gera as linhas da grade de palavras ocultas e preenche word_positions.
def construir_grade():
    global output_lines, word_positions
    output_lines = []
    word_positions = {}
    NUM_COLS = 5
    line_index = 0

    for tamanho in sorted(palavras_por_tamanho):
        output_lines.append(f"\nPalavras de {tamanho} letras:")
        line_index += 1
        col_count = 0
        row_str = ""
        lista_palavras = sorted(palavras_por_tamanho[tamanho])
        for idx, palavra in enumerate(lista_palavras):
            word_positions[palavra] = (line_index, col_count, tamanho)
            row_str += f"{'■ ' * tamanho}".ljust(15)
            col_count += 1
            if col_count == NUM_COLS:
                output_lines.append(row_str)
                line_index += 1
                row_str = ""
                col_count = 0
        if row_str:
            output_lines.append(row_str)
            line_index += 1

#Mostra a grade
def mostrar_grade():
    resultado_text.delete("1.0", tk.END)
    for line in output_lines:
        resultado_text.insert(tk.END, line + "\n")
    atualizar_pontuacao()

#Revela Palavra ao acertar
def revelar_palavra(palavra):
    global output_lines, word_positions
    if palavra in word_positions:
        line_idx, col_idx, tamanho = word_positions[palavra]
        # Pega a linha atual da grade
        line = output_lines[line_idx]
        # Divide a linha em colunas de 15 caracteres
        cols = [line[i:i+15] for i in range(0, len(line), 15)]
        # Substitui o campo oculto pela palavra
        cols[col_idx] = palavra.upper().ljust(15)
        # Recria a linha
        output_lines[line_idx] = ''.join(cols)

def mostrar_grade_atualizada():
    mostrar_grade()

def atualizar_pontuacao():
    label_pontos.config(text=f"Pontuação: {pontuacao}")

# Verificar tentativa
def verificar_palavra(event=None):
    global pontuacao
    tentativa = campo_texto.get().lower().strip()
    if tentativa in palavras_validas and tentativa not in palavras_descobertas:
        palavras_descobertas.add(tentativa)
        revelar_palavra(tentativa)
        pontuacao_adicionada = pontos_palavra(tentativa)
        pontuacao += pontuacao_adicionada
        mostrar_grade_atualizada()
        campo_texto.delete(0, tk.END)
        tocar_som_sucesso()
        resultado_text.insert(tk.END, f"\n✔ +{pontuacao_adicionada} pontos!\n")
        if palavras_descobertas == palavras_validas:
            resultado_text.insert(tk.END, "\n🎉 Parabéns! Você encontrou todas as palavras!\n")
    else:
        campo_texto.delete(0, tk.END)
        resultado_text.insert(tk.END, "\n❌ Palavra inválida! (-1 ponto)\n")
        pontuacao -= 1
        atualizar_pontuacao()

# Gerar palavras e iniciar o jogo
def iniciar_jogo():
    global palavras_validas, palavras_descobertas, palavras_por_tamanho, pontuacao
    entrada = campo_texto.get().upper()
    if not entrada.isalpha():
        return

    desenhar_pecas(canvas_letras, entrada)
    resultado_text.delete("1.0", tk.END)
    palavras_validas = set()
    palavras_descobertas = set()
    palavras_por_tamanho = defaultdict(set)
    pontuacao = 0
    atualizar_pontuacao()

    for i in range(4, len(entrada) + 1):
        for p in permutations(entrada, i):
            palavra = ''.join(p).lower()
            if palavra in spell:
                palavras_validas.add(palavra)
                palavras_por_tamanho[len(palavra)].add(palavra)

    resultado_text.insert(tk.END, f"{len(palavras_validas)} palavras possíveis.\n")
    campo_texto.delete(0, tk.END)
    campo_texto.focus()

    construir_grade()
    mostrar_grade()

# Revela todas as palavras faltantes na grade
def mostrar_todas():
    global palavras_descobertas, pontuacao
    faltando = palavras_validas - palavras_descobertas
    if not faltando:
        resultado_text.insert(tk.END, "\n👏 Você já descobriu todas!\n")
        return

    for palavra in sorted(faltando):
        palavras_descobertas.add(palavra)
        revelar_palavra(palavra)
    mostrar_grade()
    resultado_text.insert(tk.END, "\n👀 Todas as palavras foram reveladas!\n")

# Interface
root = tk.Tk()
root.title("Jogo de Anagramas")
root.geometry("1920x1080")  # Janela Full HD
root.configure(bg="#f7f7f7")

canvas_letras = tk.Canvas(root, width=1000, height=100, bg="#f7f7f7", highlightthickness=0)
canvas_letras.pack(pady=10)

label_pontos = tk.Label(root, text="Pontuação: 0", font=("Arial", 18, "bold"), bg="#f7f7f7", fg="#4B9500")
label_pontos.pack(pady=5)

campo_texto = tk.Entry(root, font=("Arial", 18), width=20, justify="center")
campo_texto.pack()
campo_texto.bind("<KeyRelease>", ao_digitar)
campo_texto.bind("<Return>", verificar_palavra)

frame_botoes = tk.Frame(root, bg="#f7f7f7")
frame_botoes.pack(pady=10)

btn_iniciar = tk.Button(frame_botoes, text="🎲 Iniciar Jogo", font=("Arial", 14), command=iniciar_jogo)
btn_iniciar.grid(row=0, column=0, padx=10)

btn_mostrar = tk.Button(frame_botoes, text="❓ Mostrar Todas", font=("Arial", 14), command=mostrar_todas)
btn_mostrar.grid(row=0, column=1, padx=10)

# Adiciona rolagem ao Text
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

resultado_text = tk.Text(root, font=("Courier New", 14), width=140, height=35, yscrollcommand=scrollbar.set)
resultado_text.pack(pady=10, padx=10)

scrollbar.config(command=resultado_text.yview)

root.mainloop()