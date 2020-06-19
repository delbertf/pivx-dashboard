from flask import Flask, render_template, jsonify
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import os
import time

app = Flask(__name__, static_url_path='')
RPC_USER = os.environ.get("RPC_USER")
RPC_KEY = os.environ.get("RPC_KEY")
RPC_URL = os.environ.get("RPC_URL")

if not RPC_USER:
    raise ValueError("No RPC_USER set for Flask application")
if not RPC_KEY:
    raise ValueError("No RPC_KEY set for Flask application")
if not RPC_URL:
    raise ValueError("No RPC_URL set for Flask application")


@app.route('/')
def index():
    ts = time.gmtime()
    get_info = pivx_get_info()
    staking_status = pivx_get_staking_status()
    wallet_info = pivx_get_wallet_info()
    mnsync_status = pivx_get_mnsync_status()
    return render_template('index.html', get_info=get_info, staking_status=staking_status, wallet_info=wallet_info, mnsync_status=mnsync_status, last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))


@ app.route('/wallet')
def wallet():
    return render_template('wallet.html')


"""
 Application API layer
"""


@app.route('/control/getinfo', methods=['POST'])
def control_getinfo():
    ts = time.gmtime()
    return jsonify({'data': render_template('index_getinfo.html', get_info=pivx_get_info(), last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))})


@app.route('/control/getstakingstatus', methods=['POST'])
def control_getstakingstatus():
    ts = time.gmtime()
    return jsonify({'data': render_template('index_getstakinginfo.html', staking_status=pivx_get_staking_status(), last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))})


@app.route('/control/getwalletinfo', methods=['POST'])
def control_getwalletinfo():
    ts = time.gmtime()
    return jsonify({'data': render_template('index_getwalletinfo.html', wallet_info=pivx_get_wallet_info(), last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))})


@app.route('/control/getmnsyncstatus', methods=['POST'])
def control_getmnsyncstatus():
    ts = time.gmtime()
    return jsonify({'data': render_template('index_getmnsyncstatus.html', mnsync_status=pivx_get_mnsync_status(), last_update=time.strftime("%Y-%m-%d %H:%M:%S", ts))})


"""
Decorators
"""


def access_pivxd(func):
    """
    Decorator function to access the pivxd server and create an access object
    """
    def inner(*args, **kwargs):
        pivxd = AuthServiceProxy("http://%s:%s@%s" %
                                 (RPC_USER, RPC_KEY, RPC_URL))
        return func(pivxd)
    return inner


"""
PIVX wrapper API functions to query the Pivx Server with json RPC
"""


@access_pivxd
def pivx_get_info(pivxd):
    """
    This function gets the basic information about the pivx wallet
    """
    include_properties = ["version", "walletversion",
                          "services", "balance", "staking status", "zerocoinbalance", "blocks", "connections", "testnet", "errors"]
    return {key: value
            for (key, value) in pivxd.getinfo().items()
            if key in include_properties}


@access_pivxd
def pivx_get_staking_status(pivxd):

    include_properties = ["staking_status", "staking_enabled",
                          "coldstaking_enabled", "haveconnections", "mnsync", "walletunlocked", "stakeablecoins", "stakingbalance", "stakesplitthreshold"]

    return {key: value
            for (key, value) in pivxd.getstakingstatus().items()
            if key in include_properties}


@access_pivxd
def pivx_get_wallet_info(pivxd):

    include_properties = ["balance", "delegated_balance", "cold_staking_balance", "unconfirmed_balance",
                          "immature_balance", "immature_delegated_balance", "immature_cold_staking_balance", "txcount", "paytxfee"]

    return {key: value
            for (key, value) in pivxd.getwalletinfo().items()
            if key in include_properties}


@access_pivxd
def pivx_get_mnsync_status(pivxd):

    include_properties = ["IsBlockchainSynced", "lastMasternodeList",
                          "lastMasternodeWinner", "lastFailure", "nCountFailures", "countMasternodeList"]

    return {key: value
            for (key, value) in pivxd.mnsync("status").items()
            if key in include_properties}
