# Basic Blockchain Implementation

This project is a basic implementation of a blockchain system using Python and MongoDB. The code provides functionalities for managing the blockchain, nodes, transactions, and achieving consensus among network nodes.

## Features

- **Chain Class**: Represents the blockchain and provides functionalities for managing the chain, nodes, and transactions.
- **Mempool Consensus**: Achieves mempool consensus among network nodes to update the local mempool based on the consensus with other nodes.
- **Chain Consensus**: Achieves chain consensus among network nodes to update the local chain based on the consensus with other nodes.
- **Sorting**: Sorts the mempool based on gas fees to prioritize transactions for block inclusion.
- **Flask Web Application**: Exposes endpoints to interact with the blockchain, including retrieving blockchain data, accessing the mempool, and adding new transactions.
- **Mining**: Implements a basic proof-of-work (PoW) mining algorithm to generate new blocks for the blockchain.
- **Validation**: Provides functionality for verifying different aspects of blockchain data format, including new node addresses, node removal, and proof of work.

## Getting Started

1. Install the required packages by running:
   ```
   pip install pymongo flask aiohttp ecdsa
   ```

2. Set up a MongoDB server and configure the connection details in the `config.json` file.

3. To start the blockchain node, run the following command:
   ```
   python threads.py
   ```

4. Access the blockchain endpoints through the Flask web application, as defined in `endpoints.py`.

## How it Works

1. The `Chain` class represents the blockchain and manages the chain, nodes, and transactions.
2. The `mempool_consensus` class achieves mempool consensus among network nodes to update the local mempool.
3. The `chain_consensus` class achieves chain consensus among network nodes to update the local chain.
4. The `sorting` class sorts the mempool based on gas fees to prioritize transactions.
5. The Flask web application exposes endpoints to interact with the blockchain.
6. The mining algorithm generates new blocks using a basic proof-of-work (PoW) mechanism.

## Future Enhancements

This implementation serves as a basic foundation for a blockchain system. Further enhancements could include:

- Improved consensus algorithms (e.g., Proof of Stake).
- Enhanced transaction validation and security measures.
- Integration with smart contracts and more complex transactions.
- and etc.

## Contributions

Contributions to this project are welcome! Feel free to open issues or submit pull requests for bug fixes, improvements, or additional features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
Note: This blockchain is still under development and is currently in the release and debugging phase. Encountering errors is not unexpected.