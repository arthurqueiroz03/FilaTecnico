import sqlite3

conn = sqlite3.connect('agendamentos.db')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO usuarios (nome, senha, tipo)
    VALUES (?, ?, ?)
''', ('arthur.souza', '1234', 'editor')) #CRIAR USUÁRIOS POR AQUI. TROCAR SOMENTE O NOME E DIGITAR 
                                        #'python criar_usuarios.py' no terminal

conn.commit()
conn.close()

print("Usuário criado com sucesso.")