import requests
import json
import datetime
import time as t
import os
from argparse import ArgumentParser
import sys

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
    
    # HARDCODING FOR TESTING!
    # upperB = lowerB + 100
    
    while iterator <= lowerB + 2:
    # while iterator <= upperB:

        # sleep used to control the amount of requests over time since the endpoint response is 429 if too frequent
        t.sleep(1)
        
        # HARDCODING FOR TESTING! REMOVE!
        # r = requests.get('https://cosmos-rpc.quickapi.com/tx_search?query="tx.height%3D14286301"')
        print('Fetch transactions from block: ' + str(iterator))
        try:
            r = requests.get('https://cosmos-rpc.quickapi.com/tx_search?query="tx.height%3D{}"'.format(iterator))
        except:
            iterator += 1
            continue
            return tx_data
        
        if r.status_code == 200:
            print(str(r.status_code) + ' ' + r.reason)
            r_json = r.json()
        else:
            print("Unknown Error ({}), interrupting.".format(r.status_code))
            iterator += 1
            continue
            #return tx_data
        
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
    
    curr_time = ''
    step = 10000
    descending = True
    while step > 0 or curr_time < timeBound:
        
        try:
            print("try: index=" + str(index))
            t.sleep(1)
            print("after sleep")
            # time = datetime.datetime.fromtimestamp(requests.get('https://sochain.com/api/v2/get_block/' + str(crypto) + '/' + str(index)).json()['data']['time']).strftime('%Y-%m-%d %H:%M:%S')
            r = requests.get('https://cosmos-rpc.quickapi.com/block?height=' + str(index))
            print(str(r.status_code) + ' ' + str(r.reason))
            
            # retrieving timestamp of the block
            timestamp = r.json()['result']['block']['header']['time']
            curr_time = datetime.datetime.strptime(timestamp.split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
            print("block_time: " + str(curr_time) + " timeBound: " + str(timeBound) + " curr_index: " + str(index))
            
        except Exception as e:
            print(e)
            index += 1
            continue
            
        if curr_time < timeBound:
            index = index + step
            if descending is True:
                step = int(step / 2)
                descending = False
        else:
            index = index - step
            if descending is False:
                step = int(step / 2)
                descending = True
        
        if curr_time == timeBound:
            print("inside ==")
            return index + 1

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
    curr_time = ''
    
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
        elif r.status_code >= 500:
            # Internal server error
            continue
        else:
            # retrieving timestamp of the block
            timestamp = r.json()['result']['block']['header']['time']
            curr_time = datetime.datetime.strptime(timestamp.split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
            print("block_time: " + str(curr_time) + " timeBound: " + str(timeBound) + " curr_index: " + str(index))
            exceed = curr_time > timeBound

        if exceed:
            step = int(step / 2)
        else:
            index = index + step
            
    return index

# -------------------------------------------------------

if __name__ == '__main__':
        
    parser = ArgumentParser()
    parser.add_argument("-d", "--date", dest="date", type=str, help="date")
    args = parser.parse_args()
    
    if args.date:
        date = args.date
    else:
        sys.exit("Please give a date")
    
    # date = "2023-04-01"
    
    # 13679694 --> this is the lowest height available for this endpoint
    # 14150000 --> up to now, approximately first block containing transactions in archive for this endpoint
    # starting_block = 14150000 # tunable
    starting_block = 14750000
    
    #for hh in range(0, 24):
    for hh in range(0,3):
        
        # set hour string
        hh_str = lambda hh: "0" + str(hh) if hh <= 9 else str(hh)
        
        # e.g start = '2023-04-01T00:00:00Z'
        start = date + "T" + hh_str(hh) + ":00:00Z"
        start = datetime.datetime.strptime(start[:-1], '%Y-%m-%dT%H:%M:%S')
        
        # e.g. end = '2023-04-01T00:59:59Z'
        end = date + "T" + hh_str(hh) + ":59:59Z"
        end = datetime.datetime.strptime(end[:-1], '%Y-%m-%dT%H:%M:%S')

        # FIND FIRST BLOCK
        print('Finding the index of the first block...')
        lowerB = findFirstBlock(start, starting_block)
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
        res_dir = "Cosmos-" + date
        if not os.path.exists("data/" + res_dir):
            os.makedirs("data/" + res_dir)
        
        res_file = "data/" + res_dir + "/" + hh_str(hh) + ".txt"
        
        with open(res_file, 'w') as f:
            print('Saving the graph in ' + res_file)

            print('Key-sender Key-receiver', file=f)
            for t in transList:
                print(str(t[0]) + ' ' + str(t[1]), file=f)
                
        # starting_block = upperB + 1
            
