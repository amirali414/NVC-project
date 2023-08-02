from operator import itemgetter
import pymongo
from config import *

class sorting:
    """
    This class provides functionality for sorting the mempool based on gas fees.
    """

    def __init__(self, block_capacity=100) -> None:
        """
        Initializes a new instance of the sorting class.

        Args:
            mongo_host (str): A string representing the MongoDB server host.
            mongo_port (int): An integer representing the MongoDB server port.
            block_capacity (int, optional): An integer representing the maximum number of transactions to include in a block. Default is 100.
        """        
        self.mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
        self.chain_data = self.mongo_client["chain"]
        self.verified_tnxs = self.chain_data["verified"]
        self.pending_tnxs = self.chain_data["pending"]
        self.block_capacity = block_capacity

    def sort(self) -> bool:
        """
        An integer representing the maximum number of transactions to include in a block. Default is 100.

        Returns:
            bool: True if successfully updated, Flase otherwise
        """        
        mempool = self.pending_tnxs.find()
        sorted_raw_mempool = sorted(mempool, key=itemgetter('gas'), reverse=True)

        verified = sorted_raw_mempool[:self.block_capacity]
        
        if self.update(verified):
            return True
        return False
    
    def update(self, lst:list) -> bool:
        """
        update L2 mempool

        Args:
            lst (list): list of sorted tnxs

        Returns:
            bool: True
        """        
        self.verified_tnxs.drop()
        for tnx in lst:
            self.verified_tnxs.insert_one(tnx)
        return True