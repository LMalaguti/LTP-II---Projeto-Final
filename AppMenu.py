import tkinter as tk
from tkinter import messagebox
from Usuario import Usuario
from jogoV2 import Jogo



class AppMenu:
    def __init__(self, root):
        self.usuario = Usuario(db_nome='db_anagrama')
        self.usuario.create_connection()
        self.usuario.create_cursor()
        self.usuario.create_database()
        self.usuario.create_table_usuario()
        self.usuario.create_table_pontuacao()

        self.root = root
        self.root.title("Sistema de Usuários")

        self.frame_menu = tk.Frame(root)
        self.frame_menu_usuario = tk.Frame(root)
        self.frame_jogo = tk.Frame(root)
        self.frame_criar = tk.Frame(root)
        self.frame_deletar = tk.Frame(root)
        self.frame_mostrar_usuarios = tk.Frame(root)
        self.frame_update = tk.Frame(root)

        self.criar_tela_menu()
        self.criar_tela_menu_usuario()
        self.criar_tela_criar_usuario()
        self.criar_tela_deletar_usuario()
        self.criar_tela_mostrar_usuario()
        self.criar_tela_update()

        self.criar_tela_ranking()
        self.mostrar_tela(self.frame_menu)

    def mostrar_tela(self, frame):
        # Esconde todos os frames
        for f in [self.frame_menu, self.frame_menu_usuario, self.frame_jogo, self.frame_criar, self.frame_deletar, self.frame_mostrar_usuarios, self.frame_update, self.frame_ranking]:
            f.pack_forget()
        # Mostra o frame desejado
        frame.pack(pady=10)


    def criar_tela_menu(self):
        tk.Label(self.frame_menu, text="Menu Principal", font=('Arial', 14)).pack(pady=10)
        tk.Button(self.frame_menu, text="Jogar", width=20, command=self.iniciar_jogo).pack(pady=5)
        tk.Button(self.frame_menu, text="Opções Usuários", width=20, command=lambda: self.mostrar_tela(self.frame_menu_usuario)).pack(pady=5)
        tk.Button(self.frame_menu, text="Ranking", width=20, command=self.mostrar_tela_ranking).pack(pady=5)
        tk.Button(self.frame_menu, text="Sair", width=20, command=self.root.quit).pack(pady=5)

    def criar_tela_menu_usuario(self):
        tk.Label(self.frame_menu_usuario, text="Opções Usuário", font=('Arial', 14)).pack(pady=10)
        tk.Button(self.frame_menu_usuario, text="Criar Usuário", width=20, command=lambda: self.mostrar_tela(self.frame_criar)).pack(pady=5)
        tk.Button(self.frame_menu_usuario, text="Mostrar Usuário", width=20, command=lambda: [self.atualizar_lista_usuarios_mostrar(), self.mostrar_tela(self.frame_mostrar_usuarios)]).pack(pady=5)
        tk.Button(self.frame_menu_usuario, text="Update Usuário", width=20, command=lambda: self.mostrar_tela(self.frame_update)).pack(pady=5)
        tk.Button(self.frame_menu_usuario, text="Deletar Usuário", width=20, command=lambda: [self.atualizar_lista_usuarios_deletar(), self.mostrar_tela(self.frame_deletar)]).pack(pady=5)
        tk.Button(self.frame_menu_usuario, text="Voltar ao Menu Principal", width=20, command=lambda: self.mostrar_tela(self.frame_menu)).pack(pady=5)

    def criar_tela_criar_usuario(self):
        tk.Label(self.frame_criar, text="Digite o nome do usuário:").pack(pady=5)
        self.entry_nome = tk.Entry(self.frame_criar)
        self.entry_nome.pack(pady=5)

        tk.Button(self.frame_criar, text="Salvar", command=self.salvar_usuario).pack(pady=5)
        tk.Button(self.frame_criar, text="Voltar as Opções de Usuário", command=lambda: self.mostrar_tela(self.frame_menu_usuario)).pack(pady=5)

    def salvar_usuario(self):
        nome = self.entry_nome.get().strip()
        if nome:
            self.usuario.insert_usuario(nome)
            messagebox.showinfo("Sucesso", f"Usuário '{nome}' inserido!")
            self.entry_nome.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "O campo nome não pode estar vazio.")

    def criar_tela_deletar_usuario(self):
        tk.Label(self.frame_deletar, text="Digite o ID para deletar:").pack(pady=5)
        self.entry_id = tk.Entry(self.frame_deletar)
        self.entry_id.pack(pady=5)

        self.text_area_deletar = tk.Text(self.frame_deletar, height=10, width=40)
        self.text_area_deletar.pack(pady=5)
        self.atualizar_lista_usuarios_deletar()

        tk.Button(self.frame_deletar, text="Deletar", command=self.deletar_usuario).pack(pady=5)
        tk.Button(self.frame_deletar, text="Voltar as Opções de Usuário", command=lambda: self.mostrar_tela(self.frame_menu_usuario)).pack(pady=5)

    def atualizar_lista_usuarios_deletar(self):
        usuarios = self.usuario.get_usuarios()
        self.text_area_deletar.delete('1.0', tk.END)
        for u in usuarios:
            self.text_area_deletar.insert(tk.END, f"{u[0]}: {u[1]}\n")

    def atualizar_lista_usuarios_mostrar(self):
        usuarios = self.usuario.get_usuarios()
        self.text_area_mostrar.delete('1.0', tk.END)
        for u in usuarios:
            self.text_area_mostrar.insert(tk.END, f"{u[0]}: {u[1]}\n")

    def deletar_usuario(self):
        id_str = self.entry_id.get().strip()
        if id_str:
            try:
                id_int = int(id_str)
                self.usuario.delete_usuario(id_int)
                messagebox.showinfo("Sucesso", "Usuário deletado!")
                self.entry_id.delete(0, tk.END)
                self.atualizar_lista_usuarios_deletar()
            except ValueError:
                messagebox.showerror("Erro", "O ID deve ser um número.")
        else:
            messagebox.showwarning("Aviso", "O campo ID não pode estar vazio.")

    def criar_tela_mostrar_usuario(self):
        tk.Label(self.frame_mostrar_usuarios, text='Usuários: ').pack(pady=5)

        self.text_area_mostrar = tk.Text(self.frame_mostrar_usuarios, height=10, width=40)
        self.text_area_mostrar.pack(pady=5)
        self.atualizar_lista_usuarios_mostrar()

        tk.Button(self.frame_mostrar_usuarios, text="Voltar as Opções de Usuário", command=lambda: self.mostrar_tela(self.frame_menu_usuario)).pack(pady=5)

    def criar_tela_update(self):
        tk.Label(self.frame_update, text='Update de usuário: ').pack(pady=5)
        tk.Label(self.frame_update, text="Digite o nome para ser atualizado:").pack(pady=5)
        self.entry_nome_update = tk.Entry(self.frame_update)
        self.entry_nome_update.pack(pady=10)
        tk.Label(self.frame_update, text="Digite o ID do usuário: ").pack(pady=5)
        self.entry_id_update = tk.Entry(self.frame_update)
        self.entry_id_update.pack(pady=10)

        tk.Button(self.frame_update, text="Update", command=self.update_usuario).pack(pady=5)
        tk.Button(self.frame_update, text="Voltar as Opções de Usuário", command=lambda: self.mostrar_tela(self.frame_menu_usuario)).pack(pady=5)

    def update_usuario(self):
        id_str = self.entry_id_update.get().strip()
        nome_update = self.entry_nome_update.get().strip()
        if id_str and self.entry_nome_update:
            try:
                id_int = int(id_str)
                self.usuario.update_usuario_BD(nome_update, id_int)
                messagebox.showinfo("Sucesso", "Usuário foi atualizado!")
                self.entry_nome_update.delete(0, tk.END)
                self.entry_id_update.delete(9, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "O ID deve ser um número.")

    def criar_tela_ranking(self):
        self.frame_ranking = tk.Frame(self.root)
        tk.Label(self.frame_ranking, text='Ranking de Usuários', font=('Arial', 14)).pack(pady=10)

        self.text_area_ranking = tk.Text(self.frame_ranking, height=12, width=45, state='disabled')
        self.text_area_ranking.pack(pady=5)

        tk.Button(self.frame_ranking, text="Voltar ao Menu Principal", command=lambda: self.mostrar_tela(self.frame_menu)).pack(pady=5)

    def mostrar_tela_ranking(self):
        self.atualizar_ranking()
        self.mostrar_tela(self.frame_ranking)

    def atualizar_ranking(self):
        self.usuario.create_connection()
        self.usuario.create_cursor()
        ranking = self.usuario.ranking()
        self.text_area_ranking.config(state='normal')
        self.text_area_ranking.delete('1.0', tk.END)
        if ranking:
            self.text_area_ranking.insert(tk.END, f"{'Pos':<5}{'Nome':<20}{'Pontuação':>10}\n")
            self.text_area_ranking.insert(tk.END, "-"*40 + "\n")
            for idx, (nome, pontuacao) in enumerate(ranking, 1):
                self.text_area_ranking.insert(tk.END, f"{idx:<5}{nome:<20}{pontuacao:>10}\n")
        else:
            self.text_area_ranking.insert(tk.END, "Nenhum dado de ranking disponível.\n")
        self.text_area_ranking.config(state='disabled')

    def iniciar_jogo(self):
        self.mostrar_tela(self.frame_jogo)
        jogo = Jogo(self.frame_jogo, volta_menu=lambda: self.mostrar_tela(self.frame_menu))
        jogo.interface()