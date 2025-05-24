import tkinter as tk
from AppMenu import AppMenu
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Jogo de Anagramas")
    root.geometry("1920x1080")  # Janela Full HD
    root.configure(bg="#f7f7f7")
    app = AppMenu(root)
    root.mainloop()
