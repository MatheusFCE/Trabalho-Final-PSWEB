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
    connect_db = mysql.connector.connect(host='localhost', database='ProfEduDB', user='root', password='senha')

    if connect_db.is_connected():
        cursor = connect_db.cursor()
        cursor.execute("INSERT INTO Professores (nome, email, telefone) VALUES (%s, %s, %s);", (nome, email, telefone))
    if connect_db.is_connected():
        cursor.close()
        connect_db.close()


    flash(f'{nome} cadastrado !!')

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)