import mysql.connector
from tkinter import messagebox


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

