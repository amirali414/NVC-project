import hashlib
def calculate_merkle_root(transactions:list): # Tnxs Hashes , not tnxs dict
    if len(transactions) == 0:
        return ""

    if len(transactions) == 1:
        return transactions[0]

    while len(transactions) > 1:
        new_transactions = []
        if len(transactions) % 2 != 0:
            transactions.append(transactions[-1])

        for i in range(0, len(transactions), 2):
            hash_pair = hashlib.sha256(
                hashlib.sha256(transactions[i].encode()).digest() +
                hashlib.sha256(transactions[i + 1].encode()).digest()
            ).hexdigest()
            new_transactions.append(hash_pair)

        transactions = new_transactions

    return transactions[0]
