from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wallet')
def wallet():
    return render_template('wallet.html')
