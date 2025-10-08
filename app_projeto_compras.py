# Projeto: Cadastro de Produtos (Tkinter + SQLite via ODBC)
# Arquivo: app_projeto_compras.py
import pyodbc
from tkinter import *
from tkinter import ttk

# --- Configurações Iniciais da Conexão (Variáveis globais) ---
dadosConexao = ("Driver={SQLite3 ODBC Driver};Server=localhost;Database=Projeto_Compras.db")

def abrir_tela_principal():
    try:
        conexao_app = pyodbc.connect(dadosConexao)
        cursor_app = conexao_app.cursor()
        cursor_app.execute("SELECT * FROM Produtos")
        print("App de Compras Conectado!")
    except pyodbc.Error as ex:
        print(f"Erro ao conectar com o BD do App de Compras: {ex.args[0]}")
        return

    janela = Tk()
    janela.title("Cadastro de Produtos")
    janela.configure(bg="#F5F5F5")
    janela.attributes("-fullscreen", True)

    def listar_dados():
        for i in treeview.get_children():
            treeview.delete(i)
        cursor_app.execute("SELECT * FROM Produtos")
        valores = cursor_app.fetchall()
        for valor in valores:
            treeview.insert("", "end", values=(valor[0], valor[1], valor[2], valor[3]))

    def cadastrar():
        janela_cadastrar = Toplevel(janela)
        janela_cadastrar.title("Cadastrar Produto")
        janela_cadastrar.configure(bg="#FFFFFF")
        largura_janela = 450
        altura_janela = 230
        largura_tela = janela_cadastrar.winfo_screenwidth()
        altura_tela = janela_cadastrar.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_cadastrar.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')

        estilo_borda = {"borderwidth": 2, "relief": "groove"}

        Label(janela_cadastrar, text="Nome do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="W")
        nome_produto_cadastrar = Entry(janela_cadastrar, font=("Arial", 12), **estilo_borda)
        nome_produto_cadastrar.grid(row=0, column=1, padx=10, pady=10)

        Label(janela_cadastrar, text="Descrição do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="W")
        descricao_produto_cadastrar = Entry(janela_cadastrar, font=("Arial", 12), **estilo_borda)
        descricao_produto_cadastrar.grid(row=1, column=1, padx=10, pady=10)

        Label(janela_cadastrar, text="Preço do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="W")
        preco_produto_cadastrar = Entry(janela_cadastrar, font=("Arial", 12), **estilo_borda)
        preco_produto_cadastrar.grid(row=2, column=1, padx=10, pady=10)

        def salvar_dados():
            nome = nome_produto_cadastrar.get()
            descricao = descricao_produto_cadastrar.get()
            preco = preco_produto_cadastrar.get()
            try:
                preco_float = float(preco)
            except ValueError:
                print("Erro: O preço deve ser um número válido.")
                return
            novo_produto = (nome, descricao, preco_float)
            cursor_app.execute("INSERT INTO Produtos (NomeProduto, Descricao, Preco) VALUES (?, ?, ?)", novo_produto)
            conexao_app.commit()
            print("Dados cadastrados com sucesso!")
            janela_cadastrar.destroy()
            listar_dados()

        Button(janela_cadastrar, text="Salvar", font=("Arial", 12), command=salvar_dados).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")
        Button(janela_cadastrar, text="Cancelar", font=("Arial", 12), command=janela_cadastrar.destroy).grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

    def limparDados():
        for i in treeview.get_children():
            treeview.delete(i)

    def filtrar_dados(event=None):
        nome_filtro = nome_produto.get()
        descricao_filtro = descricao_produto.get()
        if not nome_filtro and not descricao_filtro:
            listar_dados()
            return
        sql = "SELECT * FROM Produtos"
        params = []
        condicoes = []
        if nome_filtro:
            condicoes.append("NomeProduto LIKE ?")
            params.append('%' + nome_filtro + '%')
        if descricao_filtro:
            condicoes.append("Descricao LIKE ?")
            params.append('%' + descricao_filtro + '%')
        if condicoes:
            sql += " WHERE " + " AND ".join(condicoes)
        try:
            cursor_app.execute(sql, tuple(params))
            produtos = cursor_app.fetchall()
            limparDados()
            for dado in produtos:
                treeview.insert('', 'end', values=(dado[0], dado[1], dado[2], dado[3]))
        except pyodbc.Error as ex:
            print(f"Erro na consulta SQL: {ex}")

    def deletar():
        item_selecionado = treeview.selection()
        if item_selecionado:
            valores = treeview.item(item_selecionado, "values")
            if valores:
                produto_id = valores[0]
                cursor_app.execute("DELETE FROM Produtos WHERE ID = ?", (produto_id,))
                conexao_app.commit()
                print(f"Produto {produto_id} deletado com sucesso!")
                listar_dados()

    def editar_dados(event):
        item_selecionado = treeview.selection()
        if not item_selecionado:
            return
        valores = treeview.item(item_selecionado, "values")
        if not valores:
            return
        produto_id = valores[0]
        janela_edicao = Toplevel(janela)
        janela_edicao.title("Editar Produto")
        janela_edicao.configure(bg="#FFFFFF")
        largura_janela = 450
        altura_janela = 230
        largura_tela = janela_edicao.winfo_screenwidth()
        altura_tela = janela_edicao.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_edicao.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')
        estilo_borda = {"borderwidth": 2, "relief": "groove"}

        Label(janela_edicao, text="Nome do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="W")
        nome_produto_edicao = Entry(janela_edicao, font=("Arial", 12), **estilo_borda)
        nome_produto_edicao.insert(0, valores[1])
        nome_produto_edicao.grid(row=0, column=1, padx=10, pady=10)

        Label(janela_edicao, text="Descrição do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="W")
        descricao_produto_edicao = Entry(janela_edicao, font=("Arial", 12), **estilo_borda)
        descricao_produto_edicao.insert(0, valores[2])
        descricao_produto_edicao.grid(row=1, column=1, padx=10, pady=10)

        Label(janela_edicao, text="Preço do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="W")
        preco_produto_edicao = Entry(janela_edicao, font=("Arial", 12), **estilo_borda)
        preco_produto_edicao.insert(0, valores[3])
        preco_produto_edicao.grid(row=2, column=1, padx=10, pady=10)

        def salvar_edicao():
            novo_nome = nome_produto_edicao.get()
            nova_desc = descricao_produto_edicao.get()
            novo_preco = preco_produto_edicao.get()
            try:
                novo_preco_float = float(novo_preco)
            except ValueError:
                print("Erro: O preço deve ser um número válido.")
                return
            cursor_app.execute("UPDATE Produtos SET NomeProduto = ?, Descricao = ?, Preco = ? WHERE ID = ?",
                              (novo_nome, nova_desc, novo_preco_float, produto_id))
            conexao_app.commit()
            print(f"Produto {produto_id} atualizado com sucesso!")
            janela_edicao.destroy()
            listar_dados()

        Button(janela_edicao, text="Salvar", font=("Arial", 12), command=salvar_edicao).grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")
        Button(janela_edicao, text="Cancelar", font=("Arial", 12), command=janela_edicao.destroy).grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

    janela.grid_rowconfigure(3, weight=1)
    for i in range(1, 10):
        janela.grid_columnconfigure(i, weight=1)
    janela.grid_columnconfigure(0, weight=0)

    Label(janela, text="Produtos", font="Arial 16", fg="blue", bg="#F5F5F5").grid(row=0, column=0, columnspan=10, padx=10, pady=10)

    nome_produto = StringVar()
    descricao_produto = StringVar()

    Label(janela, text="Filtrar por Nome:", font=("Arial", 12), bg="#F5F5F5").grid(row=1, column=0, padx=10, pady=5, sticky="W")
    nome_entry_filtro = Entry(janela, textvariable=nome_produto, font=("Arial", 12))
    nome_entry_filtro.grid(row=1, column=1, columnspan=4, padx=10, pady=5, sticky="WE")

    Label(janela, text="Filtrar por Descrição:", font=("Arial", 12), bg="#F5F5F5").grid(row=1, column=5, padx=10, pady=5, sticky="W")
    descricao_entry_filtro = Entry(janela, textvariable=descricao_produto, font=("Arial", 12))
    descricao_entry_filtro.grid(row=1, column=6, columnspan=4, padx=10, pady=5, sticky="WE")

    style = ttk.Style(janela)
    style.theme_use("default")
    style.configure("mystyle.Treeview", font=("Arial", 14), rowheight=25)
    style.configure("mystyle.Treeview.Heading", font=('Arial', 14, 'bold'))

    treeview = ttk.Treeview(janela, style="mystyle.Treeview",
                             columns=("ID", "NomeProduto", "Descricao", "Preco"),
                             show="headings", height=20)

    treeview.heading("ID", text="ID")
    treeview.heading("NomeProduto", text="Nome do Produto")
    treeview.heading("Descricao", text="Descrição do Produto")
    treeview.heading("Preco", text="Preço do Produto")

    treeview.column("ID", width=100, stretch=NO, anchor='center')
    treeview.column("NomeProduto", minwidth=200, anchor='w')
    treeview.column("Descricao", minwidth=300, anchor='w')
    treeview.column("Preco", width=150, anchor='e')

    treeview.grid(row=3, column=0, columnspan=10, sticky="NSEW", padx=10, pady=10)

    Button(janela, text="Novo", command=cadastrar, font="Arial 16").grid(row=4, column=0, columnspan=5, sticky="NSEW", padx=20, pady=10)
    Button(janela, text="Deletar", command=deletar, font="Arial 16").grid(row=4, column=5, columnspan=5, sticky="NSEW", padx=20, pady=10)

    menu_barra = Menu(janela)
    janela.configure(menu=menu_barra)
    menu_arquivo = Menu(menu_barra, tearoff=0)
    menu_barra.add_cascade(label="Arquivo", menu=menu_arquivo)
    menu_arquivo.add_command(label="Cadastrar", command=cadastrar)
    menu_arquivo.add_separator()
    menu_arquivo.add_command(label="Sair", command=lambda: [cursor_app.close(), conexao_app.close(), janela.destroy()])

    listar_dados()

    nome_produto.trace_add('write', lambda name, index, mode: filtrar_dados())
    descricao_produto.trace_add('write', lambda name, index, mode: filtrar_dados())
    treeview.bind("<Double-1>", editar_dados)

    janela.mainloop()

def verificar_credenciais():
    conexao = None
    cursor = None
    try:
        conexao = pyodbc.connect(dadosConexao)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE NOME = ? AND Senha = ?", (nome_usuario_entry.get(), senha_usuario_entry.get()))
        usuario = cursor.fetchone()
        if usuario:
            janela_principal.destroy()
            abrir_tela_principal()
        else:
            for widget in janela_principal.grid_slaves():
                if int(widget.grid_info().get("row", -1)) == 3:
                    widget.destroy()
            mensagem_lbl = Label(janela_principal, text="Nome de usuário ou senha incorretos", fg="red", bg="#F5F5F5")
            mensagem_lbl.grid(row=3, column=0, columnspan=2)
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        for widget in janela_principal.grid_slaves():
            if int(widget.grid_info().get("row", -1)) == 3:
                widget.destroy()
        mensagem_erro_lbl = Label(janela_principal, text=f"Erro de Conexão/SQL: {sqlstate}", fg="orange", bg="#F5F5F5")
        mensagem_erro_lbl.grid(row=3, column=0, columnspan=2)
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

if __name__ == "__main__":
    janela_principal = Tk()
    janela_principal.title("Tela de Login")
    janela_principal.configure(bg="#F5F5F5")

    largura_janela = 450
    altura_janela = 300
    largura_tela = janela_principal.winfo_screenwidth()
    altura_tela = janela_principal.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    janela_principal.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')

    titulo_lbl = Label(janela_principal, text="Tela de Login", font="Arial 20", fg="blue", bg="#F5F5F5")
    titulo_lbl.grid(row=0, column=0, columnspan=2, pady=20)

    nome_usuario_lbl = Label(janela_principal, text="Nome de Usuário", font="Arial 14 bold", bg="#F5F5F5")
    nome_usuario_lbl.grid(row=1, column=0, sticky="e", padx=10)

    senha_usuario_lbl = Label(janela_principal, text="Senha", font="Arial 14 bold", bg="#F5F5F5")
    senha_usuario_lbl.grid(row=2, column=0, sticky="e", padx=10)

    nome_usuario_entry = Entry(janela_principal, font="Arial 14")
    nome_usuario_entry.grid(row=1, column=1, pady=10, padx=10)

    senha_usuario_entry = Entry(janela_principal, font="Arial 14", show="*")
    senha_usuario_entry.grid(row=2, column=1, pady=10, padx=10)

    entrar_btn = Button(janela_principal, text="Entrar", font="Arial 14", command=verificar_credenciais)
    entrar_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

    sair_btn = Button(janela_principal, text="Sair", font="Arial 14", command=janela_principal.destroy)
    sair_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="NSEW")

    for i in range(6):
        janela_principal.grid_rowconfigure(i, weight=1)
    for i in range(2):
        janela_principal.grid_columnconfigure(i, weight=1)

    janela_principal.mainloop()