import sqlite3

caminho_db = "agendamentos.db"

conn = sqlite3.connect(caminho_db)

cursor = conn.cursor()
 
# ID da linha que você quer deletar

id_para_deletar = 104
 
# Executa o comando DELETE

cursor.execute("DELETE FROM agendamentos WHERE id = ?", (id_para_deletar,))

conn.commit()
 
# Mostra quantas linhas foram afetadas

print(f"{cursor.rowcount} linha(s) deletada(s).")

conn.close()
 