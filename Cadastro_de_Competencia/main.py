from flask import Flask, render_template, redirect, request, flash

app = Flask(__name__)
app.config['SECRET KEY'] = 'matheusfce'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadprof', methods=['GET'])
def cadprof():
    return render_template('cadprof.html')

@app.route('/caddisc', methods=['GET'])
def caddisc():
    return render_template('caddisc.html')

@app.route('/vincprofdisc', methods=['GET'])
def vincprofdisc():
    return render_template('vincprofdisc.html')

@app.route('/turmas', methods=['GET'])
def turmas():
    return render_template('turmas.html')

if __name__ in "__main__":
    app.run(debug=True)