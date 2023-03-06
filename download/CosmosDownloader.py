import requests
import json

# Define the API endpoint and time range to query
# api_endpoint = 'https://lcd.nylira.net'
# api_endpoint = 'https://api.cosmos.network'
# api_endpoint = 'https://rest.cosmos.directory/cosmoshub'
# api_endpoint = 'https://api.cosmoscan.net/transactions'
# api_endpoint = 'https://api.cosmoscan.net/api#/Services/get_transactions'
# api_endpoint = 'https://rpc.cosmos.interbloc.org/status?'
api_endpoint = 'https://rpc.cosmos.bh.rocks/blockchain?minHeight=14286300&maxHeight=14286302'
# api_endpoint = 'https://rpc.cosmos.bh.rocks'

# Define period of time
start_time = '2022-01-01T00:00:00Z'
end_time = '2022-01-31T23:59:59Z'

# Define the path to the output file
output_file = 'transactions.txt'

# Define the query parameters for the /txs endpoint
# pagination.key=1&order_by=ORDER_BY_UNSPECIFIED
query_params = {
    'limit': 10
    # 'pagination.key': 1,
    # 'order_by': "ORDER_BY_UNSPECIFIED"
#     'page': 1,
#     'limit': 100,
#     'tx.minheight': 1,
#     'tx.maxheight': 99999999,
#     'tx.min_time': start_time,
#     'tx.max_time': end_time
 }

# Send the initial query to the /txs endpoint
# response = requests.get(api_endpoint + '/cosmos/tx/v1beta1/txs', params=query_params)
response = requests.get(api_endpoint)
# response = requests.get(api_endpoint + "?limit=10")
print(response.status_code)
print(response.reason)
#print(response.json())


# Write the results to the output file
with open(output_file, 'w') as f:
    # Loop over each page of results
    while response.status_code == 200:
        # Parse the JSON response into a Python object
        response_data = response.json()
        
        f.write(str(response_data))
        
        break

        # # Loop over each transaction in the current page of results
        # for tx in response_data['txs']:
        #     print(tx)
        #     # Extract the sender and recipient addresses from the transaction data
        #     sender = tx['tx']['value']['msg'][0]['value']['from_address']
        #     recipient = tx['tx']['value']['msg'][0]['value']['to_address']

        #     # Write the sender and recipient addresses to the output file
        #     f.write(sender + ',' + recipient + '\n')

        # # Check if there are more pages of results
        # if 'next' not in response.links:
        #     break

        # # Update the query parameters to retrieve the next page of results
        # next_url = response.links['next']['url']
        # query_params = dict(page=next_url.split('page=')[1])

        # # Send the next query to the /txs endpoint
        # response = requests.get(api_endpoint + '/cosmos/txs', params=query_params)

print('Transaction data written to ' + output_file)
