import sqlite3

conn = sqlite3.connect('agendamentos.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

for u in usuarios:
    print(f"ID: {u[0]} | Nome: {u[1]} | Senha: {u[2]} | Tipo: {u[3]}")

conn.close()
