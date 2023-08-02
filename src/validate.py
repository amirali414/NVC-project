from urllib.parse import urlparse
from ecdsa import NIST384p ,VerifyingKey
import hashlib
import pymongo
import mercle
from sorter import sorting
from config import *

mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
chain_data = mongo_client["chain"] 
nodes = chain_data["nodes"]

class verify_format:
    
    def verify_new_node_address(address: str, port: int) -> bool:
        if urlparse(address).scheme and urlparse(address).netloc:
            if port <= 2**16-1:
                return True
        return False
    
    def verify_node_remove(node: dict) -> bool:
        if node in nodes.find({}, {"_id": 0}):
            return True
        return False
    
    def verify_proof(proof: int, pv_hash: str, root: str, address:str, diff: int) -> str:
        diff_in_zeroes = diff * "0"
        obj = str(proof) + pv_hash + root + address
        hashed_obj = hashlib.sha256(obj.encode()).hexdigest()

        if hashed_obj[(len(hashed_obj)-len(diff_in_zeroes)):] == diff_in_zeroes:
            return hashed_obj
        return False
    
class verify_tnxs:

    def __init__(self) -> None:
        self.mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
        self.chain_data = self.mongo_client["chain"]
        self.chain = self.chain_data["chain"]
        self.pending_tnxs = self.chain_data["pending"]
        self.verified_tnxs = self.chain_data["verified"]
        self.balances = self.chain_data["balance"]
        self.host = mongo_host
        self.port = mongo_port

    def verify_tnxs_for_add_to_block(self, tnx: dict) -> bool:
        sender = tnx["sender"]
        recepient = tnx["recepient"]
        sign = tnx["sign"]
        amount = tnx["amount"]
        TXID = tnx["TXID"]
        time = tnx["time"]
        gas = tnx["gas"]
        msg = (sender + recepient + str(amount)).encode()

        if self.verify_tnx_sign(sender, sign, msg):
            sender_balance = self.balances.find({"address": sender})[0]["balance"]
            if sender_balance >= float(amount) + float(gas):
                if TXID == hashlib.sha256((msg + str(time)).encode()).hexdigest():
                    if self.transfer(sender, recepient, amount, sender_balance):
                        return True
                    else:
                        self.remove_tnx_sort_again(tnx)
                else:
                    self.remove_tnx_sort_again(tnx)
            else:
                self.remove_tnx_sort_again(tnx)
        else:
            self.remove_tnx_sort_again(tnx)

    def remove_tnx_sort_again(self, tnx):
        self.verified_tnxs.delete_one(tnx)
        S = sorting(self.host, self.port)
        S.sort()


    def transfer(self, tnx_sender: str, tnx_recepient: str, tnx_amount: float, tnx_sender_balance: float, gas:float) -> bool:
        sender_query = {"address": tnx_sender}
        recepient_balance = self.balances.find({"address": recepient_query})[0]["balance"]
        recepient_query = {"address": tnx_recepient}
        to_decrease_from_sender = float(tnx_amount) + float(gas)
        new_value_for_sender = {"$set":{"balance":(tnx_sender_balance - to_decrease_from_sender)}}
        new_value_for_recepient = {"$set":{"balance":(recepient_balance + tnx_amount)}}
        self.balances.update_one(sender_query, new_value_for_sender)
        self.balances.update_one(recepient_query, new_value_for_recepient)
        return True

    @staticmethod
    def verify_tnx_sign(sender: str, sign: str, msg: str) -> bool:
        public_key= VerifyingKey.from_string(sender, curve=NIST384p)
        msg = msg.encode()
        try :
            public_key.verify(sign, msg)
            return True
        except:
            return False
        
class verify_block:
    def __init__(self, diff) -> None:
        self.diff = diff
