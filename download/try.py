import requests

class Transaction:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

# Testing values
lowerB = 14286301
upperB = 14286301

transList = []
nodeSet = set()

blockIterator = lowerB

output_file = "transactions.txt"
f = open(output_file, 'w')

while blockIterator <= upperB:

    # r = requests.get('https://rpc.cosmos.bh.rocks/block?height=' + str(blockIterator))
    
    r = requests.get('https://rpc.cosmos.bh.rocks/tx_search?query=_&prove=_&page=_&per_page=_&order_by=_')
    f.write(str(r.json()))

    if r.status_code == 200:
        r = r.json()
        #print(str(r))
    else:
        print("Unknown Error ({}), interrupting.".format(r.status_code))
        exit(1)

    for tx in r['result']['block']['data']['txs']:
        
        # PROBLEM HERE (tx contains encoded data, I need to retrieve the hash of the transaction)
        print(tx)
        tx = requests.get('https://rpc.cosmos.bh.rocks/tx?hash=' + tx)
        
        if tx.status_code == 200:
            tx = tx.json()
            for msg in tx['tx']['value']['msg']:
                inputs = msg['value'].get('inputs', [])
                for i in inputs:
                    nodeSet.add(i['address'])
                    outputs = msg['value'].get('outputs', [])
                    for o in outputs:
                        nodeSet.add(o['address'])
                        transList.append(Transaction(i['address'], o['address']))
        elif tx.status_code == 404:
            print('Error 404: invalid transaction id. Skipping it.')
            continue
        else:
            print("Unknown Error ({}), interrupting.".format(tx.status_code))
            break
        
        # JUST ONE FOR TESTING !!!!!!!!!!!!!!!!!!!!
        break

    blockIterator += 1

print(nodeSet)
print(transList)
