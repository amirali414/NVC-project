from flask import *
import pymongo
import main
from config import *

mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
C = main.Chain()

app = Flask(__name__)
chain_data = mongo_client["chain"]

@app.route("/chain", methods=["GET"])
def chain_endpoint():
    chain = chain_data["chain"]
    chain = chain.find({}, {"_id": 0})
    return jsonify(chain), 200

@app.route("/mempool", methods=["GET"])
def l1pool():
    pending_tnxs = chain_data["pending"]
    pending_tnxs = pending_tnxs.find({}, {"_id": 0})
    return jsonify(pending_tnxs), 200

@app.route("/sorted", methods=["GET"])
def l2pool():
    verified_tnxs = chain_data["verified"]
    verified_tnxs = verified_tnxs.find({}, {"_id": 0})
    return jsonify(verified_tnxs), 200

@app.route("/ledger", methods=["GET"])
def accounts():
    balances = chain_data["balance"]
    balances = balances.find({}, {"_id": 0})
    return jsonify(balances)

@app.route("/newtnx", methods=["POST"])
def new_tnx():
    sender = request.args.get("sender")
    recepient = request.args.get("recepient")
    amount = request.args.get("amount")
    sign = request.args.get("sign")
    gas = request.args.get("gas")
    response = dict()
    status_code = None
    trasnaction = C.new_tnx(sender, recepient, amount, sign, gas)
    if type(trasnaction) == dict:
        response = {
            "status": "success",
            "message": "transaction added to L1 mempool successfully",
            "transaction": trasnaction,
            "optional-data": {
                "msg": sender + recepient + str(amount)
            }
        }
        status_code = 201
    else:
        response = {
            "status": "Failed",
            "message": "failed to add the transaction to L1 mempool",
            "reason": "sign is incorrect"
        }
        status_code = 400

    return jsonify(response), status_code

@app.route("/nodes/add", methods=["GET"])
def add_node(): 
    scheme_and_netloc = request.args.get("address")
    port = request.args.get("port")
    response = dict()
    status_code = None
    if C.add_new_node(scheme_and_netloc, port):
        response = {
            "status": "successful",
            "message": "node added to nodes db successfully",
            "caution": "this node is only added for node that you requested - [" + flask_host + "]",
            "value": {
                "address": scheme_and_netloc,
                "port": port
            }
        }
        status_code = 201
    else: 
        response = {
            "status": "Failed",
            "message": "Failed to add node address to nodes db",
            "reason": "make sure you entred the scheme(http / https), netloc and port correctly and try again",
            "value": {
                "address": scheme_and_netloc,
                "port": port
            }
        }
        status_code = 400

    return jsonify(response), status_code

@app.route("/nodes/remove", methods=["DELETE"])
def remove_node():
    scheme_and_netloc = request.args.get("address")
    port = request.args.get("port")
    to_check = {"address": scheme_and_netloc, "port": port}
    response = dict()
    status_code = None
    if C.remove_node(to_check):
        response = {
            "status": "success",
            "message": "the node successfully removed from nodes db",
            "value": to_check
        }
        status_code = 200
    else:
        response = {
            "status": "Failed",
            "message": "failed to remove the node from db",
            "reason": [
                "make sure you have entred the correct information, like scheme(http / https), netloc and port",
                "make sure that node you want to delete exist in the db"
            ],
            "value": to_check
        }
        status_code = 400
    
    return jsonify(response), status_code

def run_flask():
    app.run(flask_host, flask_port)