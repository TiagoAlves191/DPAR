import tkinter as tk
from tkinter import ttk
import mysql.connector

def mostrar_configuracao():
    def salvar_alteracoes():
        # Conectar ao banco de dados
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dpar"
        )
        cursor = conn.cursor()

        # Atualizar dados na tabela gestores
        query = "UPDATE gestores SET Nome = %s, Nr_Gestor = %s, Estado = %s, Contacto = %s, Admin = %s WHERE Nr_Gestor = %s"
        cursor.execute(query, (entry_nome.get(), entry_nr_gestor.get(), entry_estado.get(), entry_contacto.get(), entry_admin.get(), selected_gestor_id.get()))

        # Commit das alterações
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        # Atualizar a lista de gestores na combobox
        atualizar_combobox()

        # Limpar os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_nr_gestor.delete(0, tk.END)
        entry_estado.delete(0, tk.END)
        entry_contacto.delete(0, tk.END)
        entry_admin.delete(0, tk.END)

        # Mostrar mensagem de sucesso
        label_status["text"] = "Alterações salvas com sucesso!"

    def selecionar_gestor(event):
        # Limpar os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_nr_gestor.delete(0, tk.END)
        entry_estado.delete(0, tk.END)
        entry_contacto.delete(0, tk.END)
        entry_admin.delete(0, tk.END)

        # Obter o ID do gestor selecionado
        selected_index = combo_gestores.current()
        selected_gestor_id.set(gestores_ids[selected_index])

        # Conectar ao banco de dados
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dpar"
        )
        cursor = conn.cursor()

        # Selecionar dados do gestor selecionado
        cursor.execute("SELECT Nome, Nr_Gestor, Estado, Contacto, Admin FROM gestores WHERE Nr_Gestor = %s", (selected_gestor_id.get(),))
        gestor = cursor.fetchone()

        print("Dados do gestor selecionado:", gestor)  # Nova instrução de depuração

        # Preencher os campos de entrada com os dados do gestor
        entry_nome.insert(0, gestor[0])
        entry_nr_gestor.insert(0, gestor[1])
        entry_estado.insert(0, gestor[2])
        entry_contacto.insert(0, gestor[3])
        entry_admin.insert(0, gestor[4])

        # Fechar a conexão com o banco de dados
        conn.close()

    def atualizar_combobox():
        # Limpar a combobox
        combo_gestores['values'] = []

        # Conectar ao banco de dados
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dpar"
        )
        cursor = conn.cursor()

        # Selecionar todos os gestores
        cursor.execute("SELECT Nome, Nr_Gestor FROM gestores")
        gestores = cursor.fetchall()

        print("Gestores recuperados do banco de dados:")
        for gestor in gestores:
            print(gestor)

        # Preencher a combobox com os nomes e números dos gestores
        nomes_nr_gestores = [f"{gestor[1]} - {gestor[0]}" for gestor in gestores]
        gestores_ids.clear()
        for gestor in gestores:
            gestores_ids.append(gestor[0])

        combo_gestores['values'] = nomes_nr_gestores

        # Fechar a conexão com o banco de dados
        conn.close()

    # Criar janela de configuração
    config_window = tk.Toplevel(root)
    config_window.title("Configurações de Gestores")

    # Variável para armazenar o ID do gestor selecionado
    selected_gestor_id = tk.IntVar()

    # Frame para seleção de gestor
    frame_selecao = tk.Frame(config_window)
    frame_selecao.pack(pady=10)

    # Combobox para selecionar gestor
    combo_gestores = ttk.Combobox(frame_selecao, state="readonly")
    combo_gestores.bind("<<ComboboxSelected>>", selecionar_gestor)
    combo_gestores.pack()

    # Frame para entrada de dados do gestor
    frame_dados_gestor = tk.LabelFrame(config_window, text="Dados do Gestor")
    frame_dados_gestor.pack(pady=10)

    # Nome do gestor
    lbl_nome = tk.Label(frame_dados_gestor, text="Nome:")
    lbl_nome.grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(frame_dados_gestor)
    entry_nome.grid(row=0, column=1)

    # Nr_Gestor
    lbl_nr_gestor = tk.Label(frame_dados_gestor, text="Nr_Gestor:")
    lbl_nr_gestor.grid(row=1, column=0, sticky="w")
    entry_nr_gestor = tk.Entry(frame_dados_gestor)
    entry_nr_gestor.grid(row=1, column=1)

    # Estado
    lbl_estado = tk.Label(frame_dados_gestor, text="Estado:")
    lbl_estado.grid(row=2, column=0, sticky="w")
    entry_estado = tk.Entry(frame_dados_gestor)
    entry_estado.grid(row=2, column=1)

    # Contacto
    lbl_contacto = tk.Label(frame_dados_gestor, text="Contacto:")
    lbl_contacto.grid(row=3, column=0, sticky="w")
    entry_contacto = tk.Entry(frame_dados_gestor)
    entry_contacto.grid(row=3, column=1)

    # Admin
    lbl_admin = tk.Label(frame_dados_gestor, text="Admin:")
    lbl_admin.grid(row=4, column=0, sticky="w")
    entry_admin = tk.Entry(frame_dados_gestor)
    entry_admin.grid(row=4, column=1)

    # Botão para salvar alterações
    btn_salvar = tk.Button(config_window, text="Salvar Alterações", command=salvar_alteracoes)
    btn_salvar.pack(pady=10)

    # Rótulo de status
    label_status = tk.Label(config_window, text="", font=("Arial", 12))
    label_status.pack()

    # Atualizar a combobox com os nomes e números dos gestores
    gestores_ids = []
    atualizar_combobox()

# Criar janela principal
root = tk.Tk()
root.title("Dashboard de Gestão de Deteção")
root.attributes('-fullscreen', True)  # Definir para tela cheia

# Frame para as opções da Dashboard
frame_opcoes = tk.Frame(root, width=200, bg="lightgray")
frame_opcoes.pack(side=tk.LEFT, fill=tk.Y)

# Botões para as opções
btn_deteccao = tk.Button(frame_opcoes, text="Deteção em Tempo Real")
btn_deteccao.pack(pady=5, fill=tk.X)

btn_analise = tk.Button(frame_opcoes, text="Análise de Dados")
btn_analise.pack(pady=5, fill=tk.X)

btn_alertas = tk.Button(frame_opcoes, text="Alertas e Notificações")
btn_alertas.pack(pady=5, fill=tk.X)

btn_configuracao = tk.Button(frame_opcoes, text="Configuração", command=mostrar_configuracao)
btn_configuracao.pack(pady=5, fill=tk.X)

# Frame para o conteúdo da Dashboard
frame_conteudo = tk.Frame(root, bg="white")
frame_conteudo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Rótulo de status
label_status = tk.Label(frame_conteudo, text="Selecione uma opção...", font=("Arial", 14))
label_status.pack(pady=10)

# Rodar aplicação
root.mainloop()
