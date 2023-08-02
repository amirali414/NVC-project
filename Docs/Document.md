# Full Code Documentation

This document provides detailed documentation for the code you provided. It explains the purpose, functionalities, and dependencies of each class and function in the codebase.

![Base flowchart](/node/Docs/images/flowchart.png "How it works")

## Dependencies
The code relies on the following external libraries and modules:

- `time`: A module providing various time-related functions.
- `hashlib`: A module providing hash functions, including SHA-256.
- `pymongo`: A Python driver for MongoDB, used for database operations.
- `asyncio`: A module for writing asynchronous code using coroutines.
- `aiohttp`: An asynchronous HTTP client and server library.
- `operator.itemgetter`: A function for item-based sorting.
- `urllib.parse.urlparse`: A function for parsing URLs.
- `ecdsa`: A library for implementing the Elliptic Curve Digital Signature Algorithm (ECDSA).
- `mercle`: A module for calculating the Merkle root.

## Class: Chain
This class represents the blockchain and provides functionalities for managing the chain, nodes, and transactions.

### Constructor `__init__(self, mongo_host: str, mongo_port: int)`
- Initializes a new instance of the `Chain` class.
- Parameters:
  - `mongo_host`: A string representing the MongoDB server host.
  - `mongo_port`: An integer representing the MongoDB server port.
- Initializes instance variables for MongoDB connection and various collections.

### Method: `add_new_node(self, address: str, port: int) -> bool`
- Adds a new node to the network.
- Parameters:
  - `address`: A string representing the address of the new node.
  - `port`: An integer representing the port of the new node.
- Returns `True` if the node is added successfully, `False` otherwise.

### Method: `remove_node(self, node: dict) -> bool`
- Removes a node from the network.
- Parameters:
  - `node`: A dictionary representing the node to be removed.
- Returns `True` if the node is removed successfully, `False` otherwise.

### Method: `generate_new_block(self, proof: int) -> dict`
- Generates a new block for the blockchain.
- Parameters:
  - `proof`: An integer representing the proof of work for the block.
- Returns a dictionary representing the newly generated block.

### Method: `format_tnxs_for_block(self) -> list`
- Formats the verified transactions for inclusion in a new block.
- Returns a list of transaction hashes.

### Method: `new_tnx(self, sender: str, recepient: str, amount: float, sign: str, gas:float)`
- Adds a new transaction to the pending transactions.
- Parameters:
  - `sender`: A string representing the sender of the transaction.
  - `recepient`: A string representing the recipient of the transaction.
  - `amount`: A float representing the amount of the transaction.
  - `sign`: A string representing the signature of the transaction.
  - `gas`: A float representing the gas fee of the transaction.

## Class: mempool_consensus
This class provides functionality for achieving mempool consensus among network nodes.

### Constructor `__init__(self, mongo_host, mongo_port, nodes)`
- Initializes a new instance of the `mempool_consensus` class.
- Parameters:
  - `mongo_host`: A string representing the MongoDB server host.
  - `mongo_port`: An integer representing the MongoDB server port.
  - `nodes`: A list of nodes in the network.

### Method: `reach_mempool_consensus(self) -> None`
- Performs the mempool consensus algorithm.
- Fetches mempool data from each node in the network and updates the local mempool accordingly.

## Class: chain_consensus
This class provides functionality for achieving chain consensus among network nodes.

### Constructor `__init__(self, mongo_host, mongo_port, nodes, index)`
- Initializes a new instance of the `chain_consensus` class.
- Parameters:
  - `mongo_host`: A string representing the MongoDB server host.
  - `mongo_port`: An integer representing the MongoDB server port.
  - `nodes`: A list of nodes in the network.
  - `index`: The current index of the local chain.

### Method: `reach_consensus(self) -> None`
- Performs the chain consensus algorithm.
- Fetches chain data from each node in the network and updates the local chain accordingly.

## Class: sorting
This class provides functionality for sorting the mempool based on gas fees.

![Why we need to sort pool?](/node/Docs/images/flowchart-2.png "How it works")

### Constructor `__init__(self, mongo_host:str, mongo_port:int, block_capacity=100)`
- Initializes a new instance of the `sorting` class.
- Parameters:
  - `mongo_host`: A string representing the MongoDB server host.
  - `mongo_port`: An integer representing the MongoDB server port.
  - `block_capacity`: An integer representing the maximum number of transactions to include in a block. Default is 100.

### Method: `sort(self) -> bool`
- Sorts the transactions in the mempool based on the gas fee in descending order.

## Class: verify_format
This class provides functionality for verifying the format and validity of different blockchain aspects.

### Method: `verify_new_node_address(address: str, port

: int) -> bool`
- Verifies the format of a new node's address and port.

### Method: `verify_node_remove(nodes: list, node: dict) -> bool`
- Verifies the validity of removing a node from the network.

### Method: `verify_proof(proof: int, pv_hash: str, root: str, diff: int) -> str`
- Verifies the proof of work for a block.

## Class: verify_tnxs
This class provides functionality for verifying transaction-related data and updating the blockchain.

### Constructor `__init__(self, mongo_host: str, mongo_port: int)`
- Initializes a new instance of the `verify_tnxs` class.
- Parameters:
  - `mongo_host`: A string representing the MongoDB server host.
  - `mongo_port`: An integer representing the MongoDB server port.

### Method: `verify_tnxs_for_add_to_block(self, tnx: dict) -> bool`
- Verifies the validity of a transaction before adding it to a block.

### Method: `remove_tnx_sort_again(self, tnx)`
- Removes a transaction from the verified transactions collection and triggers mempool sorting.

### Method: `transfer(self, tnx_sender: str, tnx_recepient: str, tnx_amount: float, tnx_sender_balance: float) -> bool`
- Transfers funds between sender and recipient accounts.

### Method: `verify_tnx_sign(sender: str, sign: str, msg: str) -> bool`
- Verifies the digital signature of a transaction.

## Class: verify_block
This class provides functionality for validating blocks in the blockchain.

### Constructor `__init__(self, diff) -> None`
- Initializes a new instance of the `verify_block` class.
- Parameters:
  - `diff`: The network difficulty for validating blocks.

#### TODO: network dificullity
#### TODO: halving
#### TODO: give gas of mined tnxs to miner