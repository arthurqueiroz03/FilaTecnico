import sqlite3

# Cria o banco (ou conecta, se já existir)
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

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")