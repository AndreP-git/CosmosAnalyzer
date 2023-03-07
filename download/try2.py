import requests
import json
import datetime
import time as t

def download(lowerB, upperB):
    
    tx_data = []
    iterator = lowerB
    
    # HARDCODING UPPERB FOR TESTING! REMOVE!
    # upperB = lowerB + 100
    
    while iterator <= upperB:

        t.sleep(2)
        # r = requests.get('https://cosmos-rpc.quickapi.com/tx_search?query="tx.height%3D14286301"')
        print('Fetch transactions from block: ' + str(iterator))
        r = requests.get('https://cosmos-rpc.quickapi.com/tx_search?query="tx.height%3D{}"'.format(iterator))
        
        if r.status_code == 200:
            print(str(r.status_code) + ' ' + r.reason)
            r_json = r.json()
        else:
            print("Unknown Error ({}), interrupting.".format(r.status_code))
            return 0
        
        #print(r_json)
        
        txs = r_json["result"]["txs"]

        # Extract the sender and recipient addresses for each transaction
        for tx in txs:
            
            log = tx["tx_result"]["log"]
            try:    
                log_json = json.loads(log)
            except:
                continue
            events = log_json[0]["events"] #[-1]["attributes"]
            
            for e in events:
                if e["type"] == "transfer":
                    
                    attributes = e["attributes"] 
                    
                    for att in attributes:
                        if att["key"] == "recipient":
                            recipient = att["value"]
                        if att["key"] == "sender":
                            sender = att["value"]
                        # if att["key"] == "amount":
                        #     amount = att["value"]
                        
                    tx_data.append((sender, recipient))

        iterator += 1   
    
    return tx_data
    
# --------------------------------------------------------

def findFirstBlock(timeBound, index):
    step = 10000
    descending = True
    while step > 0 or time < timeBound:
        
        try:
            t.sleep(1)
            # time = datetime.datetime.fromtimestamp(requests.get('https://sochain.com/api/v2/get_block/' + str(crypto) + '/' + str(index)).json()['data']['time']).strftime('%Y-%m-%d %H:%M:%S')
            r = requests.get('https://cosmos-rpc.quickapi.com/block?height=' + str(index))
            print(str(r.status_code) + ' ' + str(r.reason))
            
            timestamp = r.json()['result']['block']['header']['time']
            time = datetime.datetime.strptime(timestamp.split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
            print("block_time: " + str(time) + " timeBound: " + str(timeBound) + " curr_index: " + str(index))
            
        except:
            #print(str(r.status_code) + str(r.reason))
            print("here")
            index += 1
            continue
            
        if time < timeBound:
            index = index + step
            if descending is True:
                step = int(step / 2)
                descending = False
        else:
            index = index - step
            if descending is False:
                step = int(step / 2)
                descending = True

    return index + 1

# -------------------------------------------------

def findLastBlock(timeBound, index):
    step = 10000
    time = ''
    
    while step > 0:
        
        t.sleep(2)
        # response = requests.get('https://sochain.com/api/v2/get_block/' + str(crypto) + '/' + str(index + step))
        r = requests.get('https://cosmos-rpc.quickapi.com/block?height=' + str(index + step))
        exceed = False
        
        print(str(r.status_code) + ' ' + str(r.reason))
        if r == '<Response [404]>':
            exceed = True
        elif r.status_code == 429: # too many requests
            continue
        else:
            timestamp = r.json()['result']['block']['header']['time']
            time = datetime.datetime.strptime(timestamp.split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
            print("block_time: " + str(time) + " timeBound: " + str(timeBound) + " curr_index: " + str(index))
            exceed = time > timeBound

        if exceed:
            step = int(step / 2)
        else:
            index = index + step
            
    return index

# -------------------------------------------------------

if __name__ == '__main__':
    
    # test values
    start = '2023-02-16T04:00:00Z'
    start = datetime.datetime.strptime(start[:-1], '%Y-%m-%dT%H:%M:%S')
    end = '2023-02-16T04:59:59Z'
    end = datetime.datetime.strptime(end[:-1], '%Y-%m-%dT%H:%M:%S')
    
    print('Finding the index of the first block...')
    # 13679694 --> this is the lowest height available for this endpoint
    lowerB = findFirstBlock(start, 14150000) # --> this is the lowest height available for this endpoint
    print('First block found: ' + str(lowerB))
    
    print('Finding the index of the last block...')    
    upperB = findLastBlock(end, lowerB)
    print('Last block found: ' + str(upperB))
    
    #lowerB = 13686596 --> lowerB of 2023-1-16T00:00:00Z - 2023-01-16T00:59:59Z
    #upperB = 13687163 -- upperB of 2023-1-16T00:00:00Z - 2023-01-16T00:59:59Z
    # lowerB = 14150000 # --> up to now, approximately first block containing transactions in archive
    # upperB = 14150000
    
    print('\nStart reading the blocks')
    transList = download(lowerB, upperB)
    print("N of transactions found: " + str(len(transList)))

    fileRes = "data/test/04.txt"
    
    with open(fileRes, 'w') as f:
        print('Saving the graph in ' + fileRes)

        print('Key-sender Key-receiver', file=f)
        for t in transList:
            print(str(t[0]) + ' ' + str(t[1]), file=f)
