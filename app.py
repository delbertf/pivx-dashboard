from flask import Flask, render_template, jsonify
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os

app = Flask(__name__)
RPC_USER = os.environ.get("RPC_USER")
RPC_KEY = os.environ.get("RPC_KEY")

if not RPC_USER:
    raise ValueError("No RPC_USER set for Flask application")
if not RPC_KEY:
    raise ValueError("No RPC_KEY set for Flask application")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wallet')
def wallet():
    return render_template('wallet.html')


@app.route('/control/getinfo', methods=['POST'])
def control_getinfo():
    access = AuthServiceProxy(
        "http://%s:%s@127.0.0.1:51473" % (RPC_USER, RPC_KEY))
    print(access.getinfo())
    return jsonify(access.getinfo())
