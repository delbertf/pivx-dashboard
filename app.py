from flask import Flask, render_template, jsonify
import subprocess
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wallet')
def wallet():
    return render_template('wallet.html')


@app.route('/control/getinfo', methods=['POST'])
def control_getinfo():
    return jsonify({"info": "here your pivx"})
