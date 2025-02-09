from flask import Flask, render_template, redirect, request, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matheusfce'

DB_CONFIG = {
    'host': 'localhost',
    'database': 'ProfEduDB',
    'user': 'root',
    'password': 'senha'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/professores', methods=['GET'])
def professores():
    return render_template('professores.html')

@app.route('/disciplinas', methods=['GET'])
def disciplinas():
    try:
        connect_db = get_db_connection()
        cursor = connect_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Habilitacoes")
        habilitacoes = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Erro ao buscar habilitações: {err}", 'danger')
        habilitacoes = []
    finally:
        if cursor:
            cursor.close()
        if connect_db.is_connected():
            connect_db.close()

    return render_template('disciplinas.html', habilitacoes=habilitacoes)

@app.route('/cadastrardisciplina', methods=['POST'])
def cadastrardisciplina():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    carga_horaria = request.form.get('carga_horaria')
    habilitacao_necessaria_id = request.form.get('habilitacao_necessaria')

    try:
        connect_db = get_db_connection()
        cursor = connect_db.cursor()
        cursor.execute(
            "INSERT INTO Disciplinas (codigo, nome, CH, habilitacao_necessaria) VALUES (%s, %s, %s, %s);",
            (codigo, nome, carga_horaria, habilitacao_necessaria_id)
        )
        connect_db.commit()
        flash(f'Disciplina {nome} cadastrada com sucesso!', 'success')

    except mysql.connector.Error as err:
        flash(f"Erro ao cadastrar disciplina: {err}", 'danger')

    finally:
        if cursor:
            cursor.close()
        if connect_db.is_connected():
            connect_db.close()

    return redirect('/disciplinas')

if __name__ == "__main__":
    app.run(debug=True)