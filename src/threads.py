from main import *
from validate import *
from L1mempool import *
from sorter import *
from resolve import *
from endpoints import *
import threading
from config import *
import logging
from logging.handlers import SocketHandler
# import cutelog
import asyncio

log = logging.getLogger('Root logger')
log.setLevel(1)
socket_handler = SocketHandler('127.0.0.1', 19996)
log.addHandler(socket_handler)

"""
Threads:
    1. chain done
    2. tnxs done
    3. sorting done 
    4. endpoint done
    5. cutelog logging
    6. mining
"""

def chain_consensus_thread():
    instance = chain_consensus()
    while True:
        if asyncio.run(instance.reach_consensus()):
            logging.info("a new longer chain found! replaced successfully")
        else:
            logging.error("there is a problem for validating a new longer chain")
        
def transactions_consensus_thread():
    instance = mempool_consensus()
    while True:
        if asyncio.run(instance.reach_mempool_consensus()):
            logging.info("found new transactions by intracting with other nodes")
        else:
            logging.error("there is a problem with validating transactions, or the nodes list is empty")

def sorting_thread():
    instance = sorting()
    while True:
        if instance.sort():
            logging.info("sorted successfully! break for a moment")
        else:
            logging.error("there is a problem for update the L2 mempool!")

def endpoint_thread():
    logging.info("starting flask and endpoints...")
    run_flask()

def mining_thread():
    if mine_status == True:
        while True:
            instance = Chain()
            prf = 0
            while True:
                pv_h = instance.get_pv_hash()
                mer = instance.get_hashes_for_mercle()
                mer = mercle.calculate_merkle_root(mer)
                obj = str(prf) + pv_h + mer + address
                obj = hashlib.sha256(obj.encode()).hexdigest()
                if type(verify_format.verify_proof(prf, pv_h, mer, address, 1)) == dict:
                    print("a new block mined! [" + prf + "]")
                prf += 1


# def cutelog_thread():
#     time.sleep(1)
#     cutelog.main()

C = Chain()
C.generate_new_block(0)

def run_node():
    t1 = threading.Thread(target=chain_consensus)
    t2 = threading.Thread(target=transactions_consensus_thread)
    t3 = threading.Thread(target=sorting_thread)
    t4 = threading.Thread(target=endpoint_thread)
    t5 = threading.Thread(target=mining_thread)
    print("thread 1 started")
    t1.start()
    print(C.get_pv_hash())
    print("thread 2 started")
    t2.start()
    print(C.get_pv_hash())
    print("thread 3 started")
    t3.start()
    print(C.get_pv_hash())
    print("thread 4 started")
    t4.start()
    print(C.get_pv_hash())
    print("thread 5 started")
    #t5.start()

    
    #t6 = threading.Thread(target=cutelog_thread).start()

run_node()