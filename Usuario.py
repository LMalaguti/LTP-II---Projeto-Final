import tkinter as tk
from tkinter import messagebox
import mysql.connector


class Usuario:
    def __init__(self, db_user='root', db_host='localhost', db_password='123456', db_nome=''):
        self.user = db_user
        self.host = db_host
        self.senha = db_password
        self.db = db_nome
        self.conexao = None
        self.cursor = None

    def create_connection(self):
        self.conexao = mysql.connector.connect(user=self.user, host=self.host, password=self.senha)
        return self.conexao

    def create_cursor(self):
        self.cursor = self.conexao.cursor()
        return self.cursor

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS db_anagrama")
        self.cursor.execute("USE db_anagrama")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                idt INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50)
            )
        """)

    def insert_usuario(self, nome):
        try:
            self.cursor.execute("INSERT INTO usuarios (nome) VALUES (%s)", (nome,))
            self.conexao.commit()
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao inserir usuário: {erro}")

    def delete_usuario(self, idt):
        try:
            self.cursor.execute("DELETE FROM usuarios WHERE idt = %s", (idt,))
            self.conexao.commit()
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao deletar usuário: {erro}")

    def get_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        return self.cursor.fetchall()

    def update_usuario_BD(self, nome_update, id_update):
        sql_update = "UPDATE usuarios SET nome = %s WHERE idt = %s"
        self.cursor.execute(sql_update, (nome_update, id_update))


class AppMenu:
    def __init__(self, root):
        self.usuario = Usuario(db_nome='db_anagrama')
        self.usuario.create_connection()
        self.usuario.create_cursor()
        self.usuario.create_database()
        self.usuario.create_table()

        self.root = root
        self.root.title("Sistema de Usuários")

        self.frame_menu = tk.Frame(root)
        self.frame_menu_usuario = tk.Frame(root)
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

        self.mostrar_tela(self.frame_menu)

    def mostrar_tela(self, frame):
        # Esconde todos os frames
        for f in [self.frame_menu, self.frame_menu_usuario, self.frame_criar, self.frame_deletar, self.frame_mostrar_usuarios, self.frame_update]:
            f.pack_forget()
        # Mostra o frame desejado
        frame.pack(pady=10)


    def criar_tela_menu(self):
        tk.Label(self.frame_menu, text="Menu Principal", font=('Arial', 14)).pack(pady=10)
        tk.Button(self.frame_menu, text="Opções Usuários", width=20, command=lambda: self.mostrar_tela(self.frame_menu_usuario)).pack(pady=5)
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
        tk.Button(self.frame_deletar, text="Mostrar Usuários", command= self.atualizar_lista_usuarios_deletar).pack(pady=5)
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



if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x600')
    app = AppMenu(root)
    root.mainloop()
