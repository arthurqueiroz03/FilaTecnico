from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def conectar_bd():
    caminho = os.path.abspath('agendamentos.db')
    print(f'>> Conectando ao banco em: {caminho}')
    return sqlite3.connect('agendamentos.db')

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/agendar', methods=['POST'])
def agendar():
    os = request.form['os']
    cliente = request.form['cliente']
    modelo = request.form['modelo']
    data = request.form['data']
    hora = request.form['hora']
    tipo = request.form['tipo']
    tecnico = request.form['tecnico']

    conn = sqlite3.connect('agendamentos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO agendamentos (os, cliente, modelo, data, hora, tipo, tecnico)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (os, cliente, modelo, data, hora, tipo, tecnico))
    conn.commit()
    conn.close()

    return render_template('index.html')

@app.route('/tabela')
def mostrar_agendamentos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agendamentos')
    agendamentos = cursor.fetchall()
    conn.close()

    return render_template('tabela.html', agendamentos=agendamentos)

@app.route('/apagar/<int:id>', methods=['POST'])
def apagar_agendamento(id):
    conn = sqlite3.connect('agendamentos.db')
    c = conn.cursor()
    c.execute('DELETE FROM agendamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
