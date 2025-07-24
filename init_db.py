import sqlite3

conn = sqlite3.connect('agendamentos.db')

# Cria a tabela
conn.execute('''
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        os TEXT NOT NULL,
        cliente TEXT NOT NULL,
        modelo TEXT NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        tipo TEXT NOT NULL,
        tecnico TEXT NOT NULL
    )
''')

# Cria a tabela de usuários
conn.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL  -- 'usuario' ou 'editor'
    )
''')

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")