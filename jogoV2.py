import tkinter as tk
from itertools import permutations
from collections import defaultdict
from spellchecker import SpellChecker
import threading
#from playsound import playsound

# Verificador de palavras em português
spell = SpellChecker(language='pt')

#Classe Jogo com callback para poder retornar ao menu
class Jogo:
    def __init__(self, root, volta_menu=None):
        self.root = root
        self.volta_menu = volta_menu

    #Sons
    def tocar_som_click(self):
        threading.Thread(target=lambda: playsound("click.wav"), daemon=True).start()
    def tocar_som_sucesso(self):
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
    def pontos_palavra(self, palavra):
        return self.tabela_pontos.get(len(palavra), 8 if len(palavra) > 7 else 0)

    # Desenhar peças
    def desenhar_pecas(self, canvas, texto):
        canvas.delete("all")
        for i, letra in enumerate(texto.upper()):
            x = 10 + i * 60
            canvas.create_rectangle(x, 10, x + 50, 60, fill="#DEB887", outline="#8B4513", width=2)
            canvas.create_text(x + 25, 35, text=letra, font=("Arial", 24, "bold"))

    # Atualizar peças ao digitar
    def ao_digitar(self, event=None):
        self.desenhar_pecas(self.canvas_letras, self.campo_texto.get())
        self.tocar_som_click()

    # Gera as linhas da grade de palavras ocultas e preenche word_positions.
    def construir_grade(self):
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
    def mostrar_grade(self):
        self.resultado_text.delete("1.0", tk.END)
        for line in output_lines:
            self.resultado_text.insert(tk.END, line + "\n")
        self.atualizar_pontuacao()

    #Revela Palavra ao acertar
    def revelar_palavra(self, palavra):
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

    def mostrar_grade_atualizada(self):
        self.mostrar_grade()

    def atualizar_pontuacao(self):
        self.label_pontos.config(text=f"Pontuação: {pontuacao}")

    # Verificar tentativa
    def verificar_palavra(self, event=None):
        global pontuacao
        tentativa = self.campo_texto.get().lower().strip()
        if tentativa in palavras_validas and tentativa not in palavras_descobertas:
            palavras_descobertas.add(tentativa)
            self.revelar_palavra(tentativa)
            pontuacao_adicionada = self.pontos_palavra(tentativa)
            pontuacao += pontuacao_adicionada
            self.mostrar_grade_atualizada()
            self.campo_texto.delete(0, tk.END)
            self.tocar_som_sucesso()
            self.resultado_text.insert(tk.END, f"\n✔ +{pontuacao_adicionada} pontos!\n")
            if palavras_descobertas == palavras_validas:
                self.resultado_text.insert(tk.END, "\n🎉 Parabéns! Você encontrou todas as palavras!\n")
        else:
            self.campo_texto.delete(0, tk.END)
            self.resultado_text.insert(tk.END, "\n❌ Palavra inválida! (-1 ponto)\n")
            pontuacao -= 1
            self.atualizar_pontuacao()

    # Gerar palavras e iniciar o jogo
    def iniciar_jogo(self):
        global palavras_validas, palavras_descobertas, palavras_por_tamanho, pontuacao
        entrada = self.campo_texto.get().upper()
        if not entrada.isalpha():
            return

        self.desenhar_pecas(self.canvas_letras, entrada)
        self.resultado_text.delete("1.0", tk.END)
        palavras_validas = set()
        palavras_descobertas = set()
        palavras_por_tamanho = defaultdict(set)
        pontuacao = 0
        self.atualizar_pontuacao()

        for i in range(4, len(entrada) + 1):
            for p in permutations(entrada, i):
                palavra = ''.join(p).lower()
                if palavra in spell:
                    palavras_validas.add(palavra)
                    palavras_por_tamanho[len(palavra)].add(palavra)

        self.resultado_text.insert(tk.END, f"{len(palavras_validas)} palavras possíveis.\n")
        self.campo_texto.delete(0, tk.END)
        self.campo_texto.focus()

        self.construir_grade()
        self.mostrar_grade()

    # Revela todas as palavras faltantes na grade
    def mostrar_todas(self):
        global palavras_descobertas, pontuacao
        faltando = palavras_validas - palavras_descobertas
        if not faltando:
            self.resultado_text.insert(tk.END, "\n👏 Você já descobriu todas!\n")
            return

        for palavra in sorted(faltando):
            palavras_descobertas.add(palavra)
            self.revelar_palavra(palavra)
        self.mostrar_grade()
        self.resultado_text.insert(tk.END, "\n👀 Todas as palavras foram reveladas!\n")


    # Interface
    def interface(self):
        self.canvas_letras = tk.Canvas(self.root, width=1000, height=100, bg="#f7f7f7", highlightthickness=0)
        self.canvas_letras.pack(pady=10)

        self.label_pontos = tk.Label(self.root, text="Pontuação: 0", font=("Arial", 18, "bold"), bg="#f7f7f7", fg="#4B9500")
        self.label_pontos.pack(pady=5)

        self.campo_texto = tk.Entry(self.root, font=("Arial", 18), width=20, justify="center")
        self.campo_texto.pack()
        self.campo_texto.bind("<KeyRelease>", self.ao_digitar)
        self.campo_texto.bind("<Return>", self.verificar_palavra)

        self.frame_botoes = tk.Frame(self.root, bg="#f7f7f7")
        self.frame_botoes.pack(pady=10)

        self.btn_iniciar = tk.Button(self.frame_botoes, text="🎲 Iniciar Jogo", font=("Arial", 14), command=self.iniciar_jogo)
        self.btn_iniciar.grid(row=0, column=0, padx=10)

        self.btn_mostrar = tk.Button(self.frame_botoes, text="❓ Mostrar Todas", font=("Arial", 14), command=self.mostrar_todas)
        self.btn_mostrar.grid(row=0, column=1, padx=10)

        self.btn_voltar = tk.Button(self.frame_botoes, text="↩️ Voltar ao Menu", font=("Arial", 14), command=self.volta_menu)
        self.btn_voltar.grid(row=0, column=2, padx=10)




    # Adiciona rolagem ao Text
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.resultado_text = tk.Text(self.root, font=("Courier New", 14), width=140, height=35, yscrollcommand=self.scrollbar.set)
        self.resultado_text.pack(pady=10, padx=10)

        self.scrollbar.config(command=self.resultado_text.yview)