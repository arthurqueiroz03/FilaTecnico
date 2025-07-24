from flask import Flask, render_template, request, redirect, url_for, session, make_response
from datetime import datetime, timedelta, date
from collections import defaultdict
import sqlite3
import os
from collections import OrderedDict


def obter_semanas_disponiveis():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT data FROM agendamentos")
    datas = cursor.fetchall()
    conn.close()

    semanas_set = set()

    for (data_str,) in datas:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
        segunda = data_obj - timedelta(days=data_obj.weekday())
        semanas_set.add(segunda)

    if not semanas_set:
        hoje = date.today()
        semana_base = hoje - timedelta(days=hoje.weekday())
        return [semana_base]

    semanas = sorted(semanas_set)
    ultima_semana = semanas[-1]
    semanas.append(ultima_semana + timedelta(days=7))

    return list(reversed(semanas)) 


app = Flask(__name__)

app.secret_key = 'arthur2207'
app.permanent_session_lifetime = timedelta(days=30)

def conectar_bd():
    return sqlite3.connect('agendamentos.db')

from datetime import datetime, date


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']

        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session['usuario'] = nome
            session['tipo'] = usuario[1]
            session.permanent = True  # Isso ativa a expiração mais longa
            return redirect(url_for('agendar'))
        else:
            return 'Usuário ou senha inválidos'

    return render_template('login.html')

@app.template_filter('strftime')
def _jinja2_filter_datetime(value, fmt='%d/%m'):
    if isinstance(value, (datetime, date)):
        return value.strftime(fmt)
    return value

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    nome_usuario = session.get('usuario')
    if request.method == 'POST':
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

        return render_template('agendar.html', sucesso=True, nome_usuario=nome_usuario)
    return render_template('agendar.html', nome_usuario = nome_usuario)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def mostrar_agendamentos():
    semanas_disponiveis = obter_semanas_disponiveis()

    semana_str = request.args.get("semana")
    if not semana_str:
        hoje = date.today()
        segunda = hoje - timedelta(days=hoje.weekday())  # segunda-feira da semana atual
        semana_str = segunda.strftime("%Y-%m-%d")

    inicio_semana = datetime.strptime(semana_str, "%Y-%m-%d")
    dias_semana = [inicio_semana.date() + timedelta(days=i) for i in range(5)]  # segunda a sexta

    tecnicos = [
        "RONEY PASSOS",
        "LUCAS QUEIROZ",
        "JONATAS JESUS",
        "MARCELO GARANDY",
        "FABRICIO PIMENTEL",
        "JONAS SOARES"
    ]

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, tecnico, data, hora, cliente, modelo, os, tipo FROM agendamentos
        WHERE data BETWEEN ? AND ?
    ''', (dias_semana[0], dias_semana[-1]))
    rows = cursor.fetchall()
    conn.close()

    agendamentos = defaultdict(lambda: defaultdict(list))
    for id_, tecnico, data, hora, cliente, modelo, os, tipo in rows:
        data = datetime.strptime(data, '%Y-%m-%d').date()
        agendamentos[tecnico][data].append({
            'id': id_,
            'tecnico': tecnico,
            'data': data,
            'hora': hora,
            'cliente': cliente,
            'modelo': modelo,
            'os': os,
            'tipo': tipo
        })

    return render_template(
        'index.html',
        tecnicos=tecnicos,
        agendamentos=agendamentos,
        dias_semana=dias_semana,
        semana=semana_str,
        semanas_disponiveis=semanas_disponiveis,
        timedelta=timedelta
    )


@app.route('/apagar/<int:id>', methods=['POST'])
def apagar_agendamento(id):
    if session.get('tipo') != 'editor':
        return "Acesso restrito", 403
    conn = sqlite3.connect('agendamentos.db')
    c = conn.cursor()
    c.execute('DELETE FROM agendamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/editar/<int:id>', methods=['POST'])
def editar_agendamento(id):
    if session.get('tipo') != 'editor':
        return "Acesso restrito", 403
    data = request.get_json()
    campo = data.get('campo')
    valor = data.get('valor')

    campos_validos = {'cliente', 'modelo', 'hora', 'tecnico', 'data', 'os', 'tipo'}
    if campo not in campos_validos:
        return "Campo inválido", 400

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE agendamentos SET {campo} = ? WHERE id = ?
    ''', (valor, id))
    conn.commit()
    conn.close()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True, threaded=True)