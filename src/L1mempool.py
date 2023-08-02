import pymongo
import asyncio
from sorter import sorting
import aiohttp
from config import *
import time

class mempool_consensus():
    """
    This class provides functionality for achieving mempool consensus among network nodes.
    """    

    def __init__(self) -> None: 
        """
        Initializes a new instance of the mempool_consensus class.

        Args:
            nodes (list): A list of nodes in the network.
        """        
        self.mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
        self.chain_data = self.mongo_client["chain"]
        self.pending_tnxs = self.chain_data["pending"]
        self.verified_tnxs = self.chain_data["verified"]
        self.nodes = self.chain_data["nodes"]
        self.host = mongo_host
        self.port = mongo_port

    async def fetch_mempool(session, url:str) -> dict:
        """
        a side function for reach_mempool_consensus function, that sends requests to nodes.

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
        
    async def reach_mempool_consensus(self) -> None:
        """
        Performs the mempool consensus algorithm.
        Fetches mempool data from each node in the network and updates the local mempool accordingly
        """        
        if len(list(self.nodes.find())) != 0:
            async with aiohttp.ClientSession() as session:
                tasks = []
                for node in self.nodes.find({}, {"_id": 0}):
                    url = f"http://{node['address']}:{node['port']}/mempool"
                    tasks.append(self.fetch_mempool(session, url))
                
                mempool_responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                for response in mempool_responses:
                    if isinstance(response, dict):
                        local_mempool = self.pending_tnxs.find({},{"_id": 0})
                        for tnx in response:
                            if tnx not in local_mempool:
                                self.pending_tnxs.insert_one(tnx)
            if self.sort_again():
                return True
        else:
            time.sleep(1)
            pass
    
    def sort_again(self) -> bool:
        """
        a function for sort the L2 pool again

        Returns:
            bool: True
        """        
        S = sorting(self.host, self.port)
        S.sort()
        return True