from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'matheusfce'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Cadprof')

def login():
    return render_template()


if __name__ in "__main__":
    app.run(debug=True)