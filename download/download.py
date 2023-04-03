import requests
import json
import datetime
import time as t

def download(lowerB, upperB):
    '''
        args:
            - lowerB: first block of the sequence
            - upperB: last block of the sequence
        return:
            - tx_data: a list of pairs (tuples) in the form sender-receiptor
    '''
    
    tx_data = []
    iterator = lowerB
    
    # HARDCODING FOR TESTING! REMOVE!
    # upperB = lowerB + 100
    
    while iterator <= upperB:

        # sleep used to control the amount of requests over time since the endpoint response is 429 if too frequent
        t.sleep(2)
        
        # HARDCODING FOR TESTING! REMOVE!
        # r = requests.get('https://cosmos-rpc.quickapi.com/tx_search?query="tx.height%3D14286301"')
        print('Fetch transactions from block: ' + str(iterator))
        try:
            r = requests.get('https://cosmos-rpc.quickapi.com/tx_search?query="tx.height%3D{}"'.format(iterator))
        except:
            return tx_data
        
        if r.status_code == 200:
            print(str(r.status_code) + ' ' + r.reason)
            r_json = r.json()
        else:
            print("Unknown Error ({}), interrupting.".format(r.status_code))
            return tx_data
        
        # extracting transactions list
        txs = r_json["result"]["txs"]

        # Extract the sender and recipient addresses for each transaction
        for tx in txs:
            
            log = tx["tx_result"]["log"]
            try:    
                log_json = json.loads(log)
            except:
                continue
            events = log_json[0]["events"] #[-1]["attributes"]
            
            # for each "event" of the transaction, we retrieve sender and recipient from attributes
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
                    
                    # finally appending the pair sender-recipient 
                    if sender != None and recipient != None:
                        tx_data.append((sender, recipient))

        # incrementing block counter 
        iterator += 1   
    
    return tx_data
    
# --------------------------------------------------------

def findFirstBlock(timeBound, index):
    '''
        args:
            - timeBound: datetime in the format YYYY-MM-DDTHH:MM:SS
            - index: first block to use as a reference (integer)
        return:
            - index of the first block of the sequence in the desired interval of time specified
    '''
    
    step = 10000
    descending = True
    while step > 0 or time < timeBound:
        
        try:
            t.sleep(1)
            # time = datetime.datetime.fromtimestamp(requests.get('https://sochain.com/api/v2/get_block/' + str(crypto) + '/' + str(index)).json()['data']['time']).strftime('%Y-%m-%d %H:%M:%S')
            r = requests.get('https://cosmos-rpc.quickapi.com/block?height=' + str(index))
            print(str(r.status_code) + ' ' + str(r.reason))
            
            # retrieving timestamp of the block
            timestamp = r.json()['result']['block']['header']['time']
            time = datetime.datetime.strptime(timestamp.split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
            print("block_time: " + str(time) + " timeBound: " + str(timeBound) + " curr_index: " + str(index))
            
        except:
            #print(str(r.status_code) + str(r.reason))
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
    '''
        args:
            - timeBound: datetime in the format YYYY-MM-DDTHH:MM:SS
            - index: first block to use as a reference (integer)
        return:
            - index of the last block of the sequence in the desired interval of time specified
    '''
    
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
        elif r.status_code == 429:
            # too many requests
            continue
        else:
            # retrieving timestamp of the block
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
    start = '2023-02-16T23:00:00Z'
    start = datetime.datetime.strptime(start[:-1], '%Y-%m-%dT%H:%M:%S')
    end = '2023-02-16T23:59:59Z'
    end = datetime.datetime.strptime(end[:-1], '%Y-%m-%dT%H:%M:%S')
    
    # 13679694 --> this is the lowest height available for this endpoint
    # 14150000 --> up to now, approximately first block containing transactions in archive
    
    # FIND FIRST BLOCK
    print('Finding the index of the first block...')
    lowerB = findFirstBlock(start, 14150000)
    print('First block found: ' + str(lowerB))
    
    # FIND LAST BLOCK
    print('Finding the index of the last block...')    
    upperB = findLastBlock(end, lowerB)
    print('Last block found: ' + str(upperB))
    
    # DOWNLOAD TRANSACTIONS
    print('\nStart reading the blocks')
    transList = download(lowerB, upperB)
    print("N of transactions found: " + str(len(transList)))

    # SAVING RESULTS
    fileRes = "data/test/23.txt"
    
    with open(fileRes, 'w') as f:
        print('Saving the graph in ' + fileRes)

        print('Key-sender Key-receiver', file=f)
        for t in transList:
            print(str(t[0]) + ' ' + str(t[1]), file=f)
