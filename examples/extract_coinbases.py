from collections import defaultdict
import operator
import os
from blockchain_parser.blockchain import Blockchain

blockchain = Blockchain(os.path.expanduser('~/.bitcoin/blocks'))

start = 625000
for block in blockchain.get_ordered_blocks(
        os.path.expanduser('~/.bitcoin/blocks/index'),
        start=start,
        end=start + 16000,
        cache='index-cache.pickle'):
    for transaction in block.transactions:
        if transaction.is_coinbase():
            coinbase_input = transaction.inputs[0].script()
            print(block.height, '|', coinbase_input,  flush=True)
            break

                    
