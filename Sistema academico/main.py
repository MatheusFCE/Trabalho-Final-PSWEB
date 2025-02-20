from flask import Flask, jsonify, render_template, redirect, request, flash
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

    return render_template('professores.html', habilitacoes=habilitacoes)

@app.route('/cadastrarprofessor', methods=['POST'])
def cadastrarprofessor():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    id_habilitacao = request.form.get('habilitacao')

    try:
        connect_db = get_db_connection()
        cursor = connect_db.cursor()
        cursor.execute("INSERT INTO Professores (nome, email, telefone) VALUES (%s, %s, %s);", (nome, email, telefone))
        connect_db.commit()
        id_professor = cursor.lastrowid

        if id_habilitacao and id_habilitacao.strip():
            try:
                cursor.execute("INSERT INTO Professores_X_Habilitacoes (id_professor, id_habilitacao) VALUES (%s, %s);",
                (id_professor, id_habilitacao))
                connect_db.commit()
            except mysql.connector.Error as err:
                flash(f"Erro ao associar habilitação ao professor: {err}", 'danger')

        flash(f'Professor {nome} cadastrado com sucesso!', 'success')
    except mysql.connector.Error as err:
        flash(f"Erro ao cadastrar professor: {err}", 'danger')
    
    finally:
        if cursor:
            cursor.close()
        if connect_db.is_connected():
            connect_db.close()

    return redirect('/professores')

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
    habilitacao_necessaria = request.form.get('habilitacao_necessaria')

    try:
        connect_db = get_db_connection()
        cursor = connect_db.cursor()
        cursor.execute(
            "INSERT INTO Disciplinas (codigo, nome, CH, habilitacao_necessaria) VALUES (%s, %s, %s, %s);",
            (codigo, nome, carga_horaria, habilitacao_necessaria)
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

@app.route('/turmas')
def turmas():
    try:
        connect_db = get_db_connection()
        cursor = connect_db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Professores")
        professores = cursor.fetchall()
        cursor.execute("SELECT * FROM Disciplinas")
        disciplinas = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Erro ao buscar turmas: {err}", 'danger')
        professores = []
        disciplinas = []
    finally:
        if cursor:
            cursor.close()
        if connect_db.is_connected():
            connect_db.close()

    return render_template('turmas.html', professores=professores, disciplinas=disciplinas)

@app.route('/cadastrarturma', methods=['GET', 'POST'])
def cadastrarturma():
    if request.method == 'GET':
        connect_db = get_db_connection()
        cursor = connect_db.cursor(dictionary=True)
        cursor.execute("SELECT id_disciplina, nome FROM Disciplinas;")
        disciplinas = cursor.fetchall()

        cursor.execute("""
            SELECT Professores.id_professor, Professores.nome AS professor, Disciplinas.id_disciplina, Disciplinas.nome AS disciplina
            FROM Professores
            JOIN Professores_X_Habilitacoes ON Professores.id_professor = Professores_X_Habilitacoes.id_professor
            JOIN Disciplinas ON Professores_X_Habilitacoes.id_habilitacao = Disciplinas.habilitacao_necessaria;
        """)
        professores_habilitados = cursor.fetchall()

        cursor.close()
        connect_db.close()

        return render_template('cadastrarturma.html', disciplinas=disciplinas, professores=professores_habilitados)

    elif request.method == 'POST':
        id_professor = request.form.get('id_professor')
        id_disciplina = request.form.get('id_disciplina')
        ano = request.form.get('ano')
        periodo = request.form.get('periodo')
        horario = request.form.get('horario')

        try:
            connect_db = get_db_connection()
            cursor = connect_db.cursor()
            cursor.execute(
                "INSERT INTO Turmas (id_professor, id_disciplina, ano, periodo, horario) VALUES (%s, %s, %s, %s, %s);",
                (id_professor, id_disciplina, ano, periodo, horario)
            )
            connect_db.commit()
            flash(f'Turma cadastrada com sucesso!', 'success')
        except mysql.connector.Error as err:
            flash(f"Erro ao cadastrar turma: {err}", 'danger')
        finally:
            if cursor:
                cursor.close()
            if connect_db.is_connected():
                connect_db.close()

        return redirect('/turmas')

@app.route('/professores_habilitados')
def professores_habilitados():
    disciplina_id = request.args.get('disciplina_id')
    connect_db = get_db_connection()
    cursor = connect_db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Professores.id_professor, Professores.nome
        FROM Professores
        JOIN Professores_X_Habilitacoes ON Professores.id_professor = Professores_X_Habilitacoes.id_professor
        JOIN Disciplinas ON Professores_X_Habilitacoes.id_habilitacao = Disciplinas.habilitacao_necessaria
        WHERE Disciplinas.id_disciplina = %s;
    """, (disciplina_id,))
    professores = cursor.fetchall()
    cursor.close()
    connect_db.close()
    return jsonify(professores)


@app.route('/professores-consulta', methods=['GET'])
def professores_consulta():
    return render_template('professores-consulta.html')

@app.route('/disciplinas-consulta')
def disciplinas_consulta():
    return render_template('disciplinas-consulta.html')

@app.route('/turmas-consulta')
def turmas_consulta():
    return render_template('turmas-consulta.html')

if __name__ == "__main__":
    app.run(debug=True)