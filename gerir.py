import tkinter as tk
from tkinter import ttk
import mysql.connector

def consultar_dados():
    # Conectar ao banco de dados
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dpar"
    )
    cursor = conn.cursor()

    # Executar a consulta SQL
    cursor.execute("SELECT * FROM detecoes")

    # Obter os resultados da consulta
    rows = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Limpar a tabela antes de inserir novos dados
    for row in treeview.get_children():
        treeview.delete(row)

    # Exibir os resultados em uma tabela
    for row in rows:
        # Substituir 1 por "Sim" e 0 por "Não" na coluna "Aglomeracao"
        if row[5] == 1:
            row = list(row)
            row[5] = "Sim"
            treeview.insert('', 'end', values=row)
        else:
            row = list(row)
            row[5] = "Não"
            treeview.insert('', 'end', values=row)

# Criar a janela principal
root = tk.Tk()
root.title("Histórico de Deteção")

# Criar a tabela estilizada
columns = ('ID', 'Tipo', 'Data', 'Hora', 'Numero de pessoas', 'Aglomeração')
treeview = ttk.Treeview(root, columns=columns, show='headings')

# Definir o cabeçalho da tabela com negrito
style = ttk.Style()
style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
for col in columns:
    treeview.heading(col, text=col, anchor='center')

# Definir o estilo de célula para centralizar o texto
style.configure('Treeview', font=('Helvetica', 10), cellwidth=100)

# Adicionar a tabela à janela
treeview.pack(expand=True, fill='both')

# Botão para consultar os dados
consultar_button = tk.Button(root, text="Consultar Dados", command=consultar_dados)
consultar_button.pack(pady=10)

# Iniciar o loop principal do Tkinter
root.mainloop()
