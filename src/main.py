import time
import hashlib
import pymongo
from validate import verify_format, verify_tnxs
import mercle
from config import *
from bson import ObjectId


class Chain:
    """
    This class represents the blockchain 
    and provides functionalities for managing the chain,
    nodes, and transactions.
    """    
    
    def __init__(self) -> None:
        """Initializes a new instance of the Chain class.
        Initializes instance variables for MongoDB connection and various collections.

        Args:
            mongo_host (str): A string representing the MongoDB server host.
            mongo_port (int): An integer representing the MongoDB server port.
            address (str): device wallet address [For mining]
        """ 
        # setting up mongo client
        self.mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
        self.chain_data = self.mongo_client["chain"] 

        # full chain data, from genesis block to the last block
        self.chain = self.chain_data["chain"] 

        # [L1 mempool], tnxs that not sorted by gas
        self.pending_tnxs = self.chain_data["pending"] 

        # [L2 mempool], tnxs that sorted by gas
        self.verified_tnxs = self.chain_data["verified"] 

        # distributed ledger, for accounts balances
        self.balances = self.chain_data["balance"]

        # network difficulity 
        self.network_diff = 1


        # a list object from nodes
        self.nodes = self.chain_data["nodes"]

        # device wallet address
        self.address = address
        

    def add_new_node(self, address: str, port: int) -> bool:
        """Adds a new node to the network.

        Args:
            address (str): A string representing the address of the new node.
            port (int): An integer representing the port of the new node.
            wallet (str): Node wallet address, default value is None

        Returns:
            bool: Returns True if the node is added successfully, False otherwise.
        """        
        
        if verify_format.verify_new_node_address(address, port): # it must have scheme and netloc
            self.nodes.insert_one({"address": address, "port": port})
            return True
        
        return False

    def remove_node(self, node: dict) -> bool:
        """Removes a node from the network.

        Args:
            node (dict): A dictionary representing the node to be removed.

        Returns:
            bool: Returns True if the node is removed successfully, False otherwise.
        """        
        if verify_format.verify_node_remove(node):
            self.nodes.delete_one(node)
            return True
        
        return False

    def get_pv_hash(self) -> str:
        """return the last block hash

        Returns:
            str: last block hash
        """        
        last_document = self.chain.find_one({}, sort=[("_id", -1)])
        print(str(last_document["hash"]))
        time.sleep(1)
        return str(last_document["hash"])

    def generate_new_block(self, proof:int) -> dict:
        """Generates a new block for the blockchain.

        Block content:
            index: Block position and index in the chain
            time: Indicates the block mining time in UNIX format
            transactions: Processed transactions, transactions that have consumed more gas are prioritized for processing.
            proof: An integer representing the proof of work for the block.
            pv-hash: Hash of the previous block
            hash: Hash of this block
            mercle: Mercle root
            finder: block finder

        Args:
            proof (int): An integer representing the proof of work for the block.

        Returns:
            dict: Returns a dictionary representing the newly generated block.
        """        
        mercle_input = self.get_hashes_for_mercle()
        root = mercle.calculate_merkle_root(mercle_input)
        block = {
            "index": len(list(self.chain.find())),
            "time": time.time(),
            "transactions": list(self.verified_tnxs.find()),
            "proof": proof,
            "pv_hash": self.get_pv_hash(),
            "hash": verify_format.verify_proof(proof, self.get_pv_hash(), root, self.address, self.network_diff),
            "mercle": root,
            "finder": self.address
        }
        self.clear_after_new_block(block)
            
        

    def clear_after_new_block(self, block: dict) -> None:
        """Clear temp database for next block & add new block to chain
        Note: L1 tnxs still exist

        Args:
            block (dict): new block
        """        
        self.chain.insert_one(block)
        self.verified_tnxs.drop()

    def get_hashes_for_mercle(self) -> list:
        """Get a list of transaction hashes.

        Returns:
            list: Returns a list of transaction hashes.
        """        
        tnxs_hash_for_mercle = []
        for tnx in self.verified_tnxs.find({},{"_id": 0}):
            tnxs_hash_for_mercle.append(tnx["hash"])
        
        return tnxs_hash_for_mercle

    def new_tnx(self, sender: str, recepient: str, amount: float, sign: str, gas:float) -> bool:
        """Adds a new transaction to the pending transactions. [L1 mempool]

        Args:
            sender (str): A string representing the sender of the transaction.
            recepient (str): A string representing the recipient of the transaction.
            amount (float): A float representing the amount of the transaction.
            sign (str): A string representing the signature of the transaction.
            gas (float): A float representing the gas fee of the transaction.

        Returns:
            bool: True if successful adding, False otherwise
        """        
        msg = sender + recepient + str(amount)
        if verify_tnxs.verify_tnx_sign(sender, sign, msg):
            tnx = {
                "sender": sender,
                "gas": gas,
                "recepient": recepient,
                "amount": amount,
                "sign": sign,
                "TXID": hashlib.sha256((msg + str(time.time())).encode()).hexdigest(),
                "time": time.time()
            }
            self.pending_tnxs.insert_one(tnx)
            return tnx
        
        return False