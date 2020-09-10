from collections import defaultdict
from tabulate import tabulate
import binascii
import operator
import os
import sys

patterns = []
patterns.append(['/Bitfury/', 'BitFury'])
patterns.append(['Mined by AntPool', 'AntPool'])
patterns.append(['AntPooleN', 'AntPool'])
patterns.append(['ViaBTC', 'ViaBTC'])
patterns.append(['/BTC.COM/', 'BTC.com'])
patterns.append(['/bytepool.com/', 'BytePool'])
patterns.append(['HuoBi', 'Huobi'])
patterns.append(['Huobi', 'Huobi'])
patterns.append(['BTC.TOP', 'BTCTOP'])
patterns.append(['poolin.com', 'PoolIn'])
patterns.append(['nckpool', 'NCKPool'])
patterns.append(['/slush/', 'SlushPool'])
patterns.append(['SpiderPool', 'SpiderPool'])
patterns.append(['NovaBlock', 'NovaBlock'])
patterns.append(['/pool.bitcoin.com/', 'Bitcoin.com'])
patterns.append(['58COIN', '58COIN'])
patterns.append(['CN/TTTTTT', 'CN6T'])
patterns.append(['btccom', 'BTC.com'])
patterns.append(['/BitClub Network/', 'BitclubNetwork'])
patterns.append(['KanoPool', 'KanoPool'])
patterns.append(['www.okpool.top', 'OKPool'])
patterns.append(['www.okex.com', 'OKEX'])
patterns.append(['Ukrpool.com', 'UkrPool'])
patterns.append(['taal.com', 'Taal.com'])
patterns.append(['Mined by ', 'F2Pool'])


miner_share = defaultdict(int)
blocks = 0

for line in sys.stdin:
    blocks += 1
    coinbase = bytearray(line.strip().split('|')[1], encoding = 'utf-8')
    pool_found = False
    for pattern, miner in patterns:
        if bytes(pattern, encoding='utf-8') in coinbase:
            miner_share[miner] += 1
            pool_found = True
            break
    if not pool_found:
        print(coinbase.decode('utf8', errors='ignore'))
        miner_share['Unknown'] += 1

printables = []
for item in sorted(miner_share.items(), key=operator.itemgetter(1), reverse=True):
    share = '{:.4f}%'.format(round(item[1] * 100.0/blocks, 4))
    printables.append([item[0], share])
    
print(tabulate(printables, tablefmt="latex", floatfmt=".4f"))


printables = []
sorted_shares = sorted(miner_share.items(), key=operator.itemgetter(1), reverse=True)
sorted_range = int(len(sorted_shares)/2) if len(sorted_shares) % 2 == 0 else int(len(sorted_shares)/2) + 1
for i in range(0, sorted_range):
    item0 = sorted_shares[i]
    share0 = '{:.4f}%'.format(round(item0[1] * 100.0/blocks, 4))
    if i + sorted_range < len(sorted_shares):
        item1 = sorted_shares[i+sorted_range]
        share1 = '{:.4f}%'.format(round(item1[1] * 100.0/blocks, 4))
        printables.append([item0[0], share0, item1[0], share1])
    else:
        printables.append([item0[0], share0, '', ''])
    
print(tabulate(printables, tablefmt="latex", floatfmt=".4f"))

total = sum(miner_share.values())

percents = [x * 1.0/total for x in sorted(miner_share.values())]

print(percents)
print(sum([x if x < 0.01 else 0 for x in percents]))
