import sys
sys.path.append('..')
from blockchain_parser.blockchain import Blockchain

# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blockchain = Blockchain(sys.argv[1])


def is_mutual_closing(t):
    if not (t.version == 2 and t.locktime == 0):
        return False
    if not (len(t.inputs) > 0):
        return False
    for i in t.inputs:
        if not (i.sequence_number == 4294967295 and len(i.script.hex) == 0
                and len(i.witnesses) > 0):
            return False
    return True


def is_unilateral_closing(t):
    if not (t.version == 2):
        return False
    if not (hex(t.locktime).startswith('0x20')):
        return False
    for i in t.inputs:
        if not (hex(i.sequence_number).startswith('0x80')
                and len(i.script.hex) == 0 and len(i.witnesses) > 0):
            return False
    return True


start_block = 552084

num_mutual_closings = 0
num_unilateral_closings = 0
for block in blockchain.get_ordered_blocks(
        sys.argv[1] + '/index',
        cache='./cache.txt',
        start=start_block,
        end=start_block + 10):
    print("height=%d, block=%s, block timestamp=%s" %
          (block.height, block.hash, str(block.header.timestamp)))
    for transaction in block.transactions:
        is_mutual = is_mutual_closing(transaction)
        is_unilateral = is_unilateral_closing(transaction)
        if is_mutual:
            assert not is_unilateral
            num_mutual_closings += 1
        if is_unilateral:
            assert not is_mutual
            num_unilateral_closings += 1

print(num_mutual_closings)
print(num_unilateral_closings)
