# Projeto_Compras

Aplicação desktop em Python para cadastro e gerenciamento de produtos usando Tkinter e SQLite (acessado via ODBC/pyodbc).

Arquivos principais
- app_projeto_compras.py — aplicação principal (login + CRUD de produtos).
- requirements.txt — dependências.
- .gitignore — padrões para Python / excluir banco local.

Requisitos
- Python 3.8+
- Driver ODBC para SQLite (ou ajuste para usar sqlite3 nativo)
- Biblioteca pyodbc: pip install -r requirements.txt

Uso
1. Configure o ODBC para apontar para `Projeto_Compras.db` ou ajuste a string de conexão no código.
2. Crie as tabelas necessárias no banco (Produtos, Usuarios) se ainda não existirem. Exemplos:

   sqlite3 Projeto_Compras.db "CREATE TABLE Produtos (ID INTEGER PRIMARY KEY AUTOINCREMENT, NomeProduto TEXT NOT NULL, Descricao TEXT, Preco REAL);"
   sqlite3 Projeto_Compras.db "CREATE TABLE Usuarios (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOME TEXT NOT NULL, Senha TEXT NOT NULL);"
   sqlite3 Projeto_Compras.db "INSERT INTO Usuarios (NOME, Senha) VALUES ('admin','senha123');"

3. Execute:
   python app_projeto_compras.py

Licença
- Licença a definir (se desejar, adicione um arquivo LICENSE)