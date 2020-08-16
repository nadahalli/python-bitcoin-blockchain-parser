import collections
import os
import sys
import random
sys.path.append('..')
sys.path.append('.')
from blockchain_parser.blockchain import Blockchain

# Instantiate the Blockchain by giving the path to the directory 
# containing the .blk files created by bitcoind
blockchain = Blockchain(os.path.expanduser('~/.bitcoin/blocks'))

utxo_set = {}

ONE_DAY_IN_BLOCKS = 6 * 24
ONE_MONTH_IN_BLOCKS = ONE_DAY_IN_BLOCKS * 30
ONE_YEAR_IN_BLOCKS = ONE_DAY_IN_BLOCKS * 365

start = 500000
end = start + 2 * ONE_YEAR_IN_BLOCKS

print('txid;index;created_block;value;fanin;fanout;fanout_share;spent_block;life;label')

for block in blockchain.get_ordered_blocks(os.path.expanduser('~/.bitcoin/blocks/index'), start=start, end=end):
    for txn in block.transactions:
        for input in txn.inputs:
            utxo_key = '.'.join([input.transaction_hash, str(input.transaction_index)])
            if utxo_key in utxo_set:
                utxo = utxo_set[utxo_key]
                utxo['spent_block'] = block.height
                utxo['life'] = block.height - utxo['created_block']
                label = '-1'
                if utxo['life'] <= ONE_DAY_IN_BLOCKS:
                    label = '0'
                elif utxo['life'] >= ONE_MONTH_IN_BLOCKS:
                    label = '1'

                if label in ['0', '1']:
                    print(';'.join([input.transaction_hash,
                                    str(input.transaction_index),
                                    str(utxo['created_block']),
                                    str(utxo['value']),
                                    str(utxo['fanin']),
                                    str(utxo['fanout']),
                                    str(utxo['fanout_share']),
                                    str(utxo['txn_value']),
                                    str(utxo['spent_block']),
                                    str(utxo['life']),
                                    label
                    ]))
                del utxo_set[utxo_key]
                
        txn_value = sum([output.value for output in txn.outputs])

        if txn_value == 0:
            continue
        
        for i, output in enumerate(txn.outputs):
            if random.randint(1, 250) != 1:
                continue
            utxo_key = '.'.join([txn.hash, str(i)])
            utxo = {}
            utxo['created_block'] = block.height
            utxo['value'] = output.value
            utxo['fanin'] = txn.n_inputs
            utxo['fanout'] = txn.n_outputs
            utxo['fanout_share'] = output.value * 1.0/txn_value
            utxo['txn_value'] = txn_value
            utxo_set[utxo_key] = utxo



                    

