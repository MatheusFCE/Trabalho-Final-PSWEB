from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matheusfce'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadprof', methods=['POST'])
def cadastrar_professores():
    return redirect(url_for('home'))

@app.route('/caddisc', methods=['POST'])
def cadastrar_disciplinas():
    return redirect(url_for('home')) 

@app.route('/vincprofdisc', methods=['POST'])
def vincular_professores_disciplinas():
    return redirect(url_for('home')) 

@app.route('/turmas', methods=['POST'])
def turmas():
    return redirect(url_for('home')) 

if __name__ == "__main__":
    app.run(debug=True)
