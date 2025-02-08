from flask import Flask, render_template, redirect, request, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matheusfce'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/professores', methods=['GET'])
def cadprof():
    return render_template('professores.html')

@app.route('/disciplinas', methods=['GET'])
def caddisc():
    return render_template('disciplinas.html')

@app.route('/vprofessoresdisciplinas', methods=['GET'])
def vincprofdisc():
    return render_template('vprofessoresdisciplinas.html')

@app.route('/turmas', methods=['GET'])
def turmas():
    return render_template('turmas.html')

@app.route('/cadastrarprofessor', methods=['POST'])
def cadastrarprofessor():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    try:
        connect_db = mysql.connector.connect(
            host='localhost',
            database='ProfEduDB',
            user='root',
            password='senha')
        cursor = connect_db.cursor()
        cursor.execute("INSERT INTO Professores (nome, email, telefone) VALUES (%s,%s,%s);", (nome, email, telefone))
        connect_db.commit()

        flash(f'Professor {nome} cadastrado com sucesso!', 'sucess')

    except mysql.connector.Error as err:
        flash(f"Erro ao cadastrar professor: {err}", 'danger')
    
    finally:
        if cursor:
            cursor.close()
        if connect_db.is_connected():
            connect_db.close()
    return redirect('/professores')

if __name__ == "__main__":
    app.run(debug=True)