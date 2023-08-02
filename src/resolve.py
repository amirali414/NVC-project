import pymongo
import hashlib
import asyncio
import aiohttp
from config import *
import time
from validate import *

class chain_consensus:
    """
    This class provides functionality for achieving chain consensus among network nodes.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the chain_consensus class.

        """        
        
        self.mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
        self.chain_data = self.mongo_client["chain"]
        self.nodes = self.nodes = self.chain_data["nodes"]  
        self.chain = self.chain_data["chain"]
        self.balances = self.chain_data["balance"]
        self.index = len(list(self.chain.find()))
        self.host = mongo_host
        self.port = mongo_port
        self.address = address
    

    async def fetch_chain(session, url:str) -> dict:
        """
        a side function for reach_consensus function, that sends requests to nodes.

        Args:
            session (object): an object from another function
            url (str): url of node

        Returns:
            dict: response from node
        """  
        try:
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            return None

    async def reach_consensus(self) -> bool:
        """
        Performs the chain consensus algorithm.
        Fetches chain data from each node in the network and updates the local chain accordingly.

        Returns:
            bool: True if a longer chain exist, False otherwise
        """        
        if len(self.nodes.find()) != 0:
            longest_chain = None
            current_length = self.index
            async with aiohttp.ClientSession() as session:
                tasks = []
                for node in self.nodes.find({}, {"_id": 0}):
                    url = f"http://{node['address']}:{node['port']}/chain"
                    tasks.append(self.fetch_chain(session, url))
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                for response in responses:
                    if isinstance(response, dict) and 'length' in response and 'chain' in response:
                        length = response['length']
                        chain = response['chain']
                        if length > current_length and self.verify_chain(chain):
                            current_length = length
                            longest_chain = chain

            if longest_chain != None:
                if self.verify_chain(longest_chain):
                    if self.replace_chain(longest_chain):
                        return True
                
                return False
        else:
            time.sleep(1)
            print("there is no node...")
            pass
    
    def replace_chain(self, new_chain:dict) -> bool:
        """
        add new blocks to chain and process their transactions

        Args:
            new_chain (dict): the longest chain - from node consensus

        Returns:
            bool: True
        """        
        Verify_tnxs = verify_tnxs(self.host, self.port)
        new_blocks = new_chain[self.index:]
        for block in new_blocks:
            tnxs = block["transactions"]
            finder = block["finder"]
            finder_query = {"address": finder}
            finder_balance = float(self.balances.find({"address": finder_query})[0]["balance"])
            new_value = {"balance": finder_balance + 10.0}
            self.balances.update_one(finder_query, new_value)
            for tnx in tnxs:
                Verify_tnxs.verify_tnxs_for_add_to_block(tnx)
        self.chain.insert_many(new_blocks)
        return True

    
    def verify_chain(self, chain:list) -> bool:
        """
        Validate chain

        Args:
            chain (list): longest chain from node consensus

        Returns:
            bool: True if valid, False otherwise
        """        
        prev_block = chain[0]
        index = 1
        while index < len(chain):
            block = chain[index]
            if block['pv_hash'] != hashlib.sha256(str(prev_block).encode()).hexdigest():
                return False
            if not verify_format.verify_proof(block['proof'], block['pv_hash'], block['mercle'], block["address"], self.network_diff):
                return False
            prev_block = block
            index += 1
        
        return True
    
c = chain_consensus()
print(c.index)