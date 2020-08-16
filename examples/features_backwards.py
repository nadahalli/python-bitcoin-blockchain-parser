import requests
import json
import os
import sys
import sys

sys.path.append('.')

from blockchain_parser.blockchain import Blockchain
blockchain = Blockchain(os.path.expanduser('~/.bitcoin/blocks'))                                                                                                                                                                                                                                                              
utxo_set = {}                

URL = 'http://bitcoin:BfVSZsyf8UV34UEFxp8FCB2X@127.0.0.1:8332'

def pprint(x):
    print(json.dumps(x, indent=4, sort_keys=True))

def get_raw_transaction(txid):
    payload = {
        'method': 'getrawtransaction',
        'params': [txid, True],
    }
    response = requests.post(URL, json=payload).json()

    return(response['result'])

def get_block(blockhash):
    payload = {
        'method': 'getblock',
        'params': [blockhash],
    }
    response = requests.post(URL, json=payload).json()

    return(response['result'])    


ONE_DAY_IN_BLOCKS = 6 * 24
ONE_MONTH_IN_BLOCKS = ONE_DAY_IN_BLOCKS * 30
ONE_YEAR_IN_BLOCKS = ONE_DAY_IN_BLOCKS * 365

print('txid;index;created_block;value;fanin;fanout;fanout_share;total_value;spent_block;life;label')
for i, block in enumerate(blockchain.get_unordered_blocks()):
    if 1 == 100:
        break
    spent_block_hash = block.hash
    spent_block = get_block(spent_block_hash)['height']
    for tx in block.transactions:
        if tx.is_coinbase():
            continue
        raw_tx = get_raw_transaction(tx.hash)
        # Not sure why this happens. Needs more debugging.
        if raw_tx == None:
            continue
        for input in raw_tx['vin']:
            # Coinbase
            if 'txid' not in input:
                continue
            input_txid = input['txid']
            index = input['vout']
            raw_input_tx = get_raw_transaction(input_txid)
            created_block = get_block(raw_input_tx['blockhash'])['height']
            fanin = len(raw_input_tx['vin'])
            fanout = len(raw_input_tx['vout'])
            total_value = 0
            value = -1
            for output in raw_input_tx['vout']:
                total_value += output['value']
                if output['n'] == index:
                    value = output['value']
            assert (value != -1)
            assert (total_value != 0)
            fanout_share = value * 1.0/total_value
            life = spent_block - created_block
            label = '-1'
            if life <= ONE_DAY_IN_BLOCKS:
                label = '0'
            elif life >= ONE_YEAR_IN_BLOCKS:
                label = '1'
            if label in ['0', '1']:
                print(';'.join([str(input_txid),
                                str(index),
                                str(created_block),
                                str(value),
                                str(fanin),
                                str(fanout),
                                str(fanout_share),
                                str(total_value),
                                str(spent_block),
                                str(life),
                                label]))



