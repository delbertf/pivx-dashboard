from flask import Flask, render_template, jsonify
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
import time

app = Flask(__name__, static_url_path='')
RPC_USER = os.environ.get("RPC_USER")
RPC_KEY = os.environ.get("RPC_KEY")

if not RPC_USER:
    raise ValueError("No RPC_USER set for Flask application")
if not RPC_KEY:
    raise ValueError("No RPC_KEY set for Flask application")


@app.route('/')
def index():
    ts = time.gmtime()
    return render_template('index.html', get_info=pivx_get_info(), staking_status=pivx_get_staking_status(), last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))


@ app.route('/wallet')
def wallet():
    return render_template('wallet.html')


"""
 Application API
"""


@ app.route('/control/getinfo', methods=['POST'])
def control_getinfo():
    ts = time.gmtime()
    return jsonify({'data': render_template('index_getinfo.html', get_info=pivx_get_info(), last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))})


@ app.route('/control/getstakingstatus', methods=['POST'])
def control_getstakingstatus():
    ts = time.gmtime()
    return jsonify({'data': render_template('index_getstakinginfo.html', staking_status=pivx_get_staking_status(), last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))})


"""
PIVX wrapper API functions
"""


def pivx_get_info():
    access = AuthServiceProxy(
        "http://%s:%s@127.0.0.1:51473" % (RPC_USER, RPC_KEY))

    include_properties = ["version", "walletversion",
                          "services", "balance", "staking status", "zerocoinbalance", "blocks", "connections", "testnet", "errors"]
    get_info = {key: value
                for (key, value) in access.getinfo().items()
                if key in include_properties}
    return get_info


def pivx_get_staking_status():
    access = AuthServiceProxy(
        "http://%s:%s@127.0.0.1:51473" % (RPC_USER, RPC_KEY))

    include_properties = ["staking_status", "staking_enabled",
                          "coldstaking_enabled", "haveconnections", "mnsync", "walletunlocked", "stakeablecoins", "stakingbalance", "stakesplitthreshold"]
    print(access.getstakingstatus())
    get_info = {key: value
                for (key, value) in access.getstakingstatus().items()
                if key in include_properties}
    return get_info
