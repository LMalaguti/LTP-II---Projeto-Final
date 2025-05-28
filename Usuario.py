import mysql.connector
from tkinter import messagebox


class Usuario:
    def __init__(self, db_user='root', db_host='127.0.0.1', db_password='example_root_password', db_nome=''):
        self.user = db_user
        self.host = db_host
        self.senha = db_password
        self.db = db_nome
        self.conexao = None
        self.cursor = None

    def commit(self):
        pass

    def create_connection(self):
        self.conexao = mysql.connector.connect(user=self.user, host=self.host, password=self.senha, database="db_anagrama")
        return self.conexao

    def create_cursor(self):
        self.cursor = self.conexao.cursor()
        return self.cursor

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS db_anagrama")
        self.cursor.execute("USE db_anagrama")

    def create_table_usuario(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                idt_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) UNIQUE NOT NULL
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
            self.cursor.execute("DELETE FROM usuarios WHERE idt_usuario = %s", (idt,))
            self.conexao.commit()
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao deletar usuário: {erro}")

    def get_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        return self.cursor.fetchall()

    def update_usuario_BD(self, nome_update, id_update):
        sql_update = "UPDATE usuarios SET nome = %s WHERE idt_usuario = %s"
        self.cursor.execute(sql_update, (nome_update, id_update))

    def create_table_pontuacao(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pontuacao (
                idt_usuario INT,
                idt_pontos INT AUTO_INCREMENT PRIMARY KEY,
                pontuacao INT DEFAULT 0,
                FOREIGN KEY (idt_usuario) REFERENCES usuarios (idt_usuario)
            )
        """)

    def insert_pontuacao(self, pontuacao, idt_usuario):
        self.cursor.execute("INSERT INTO pontuacao (pontuacao, idt_usuario) VALUES (%s, %s)", (pontuacao, idt_usuario,))
        self.conexao.commit()

    def ranking(self):
        self.cursor.execute("""
            SELECT u.nome, SUM(p.pontuacao) as soma_pontuacoes
            FROM usuarios u
            INNER JOIN pontuacao p ON u.idt_usuario = p.idt_usuario
            GROUP BY u.idt_usuario, u.nome
            ORDER BY soma_pontuacoes DESC
        """)
        return self.cursor.fetchall()