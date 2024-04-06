import os
import json
from flask import Flask, request
import eth_abi

app = Flask(__name__)

from pyfiglet import Figlet

iexec_out = os.environ['IEXEC_OUT']


text = "Guild"
text = Figlet().renderText(text)
print(text)



@app.route('/process', methods=['POST'])
def process_request():
    request_data = request.json
    if 'data' in request_data:
        processed_data = process_data(request_data['data'])
        send_callback_data(processed_data)
        return {'status': 'success', 'message': 'Data processed and callback data sent to smart contract'}
    else:
        return {'status': 'error', 'message': 'Data is missing in the request'}

def process_data(data):
    return 'Processed: ' + data

def send_callback_data(data):
    iexec_out = os.environ.get('IEXEC_OUT', '/iexec_out')
    callback_data = eth_abi.encode_abi(['string'], [data]).hex()
    with open(os.path.join(iexec_out, 'computed.json'), 'w+') as f:
        json.dump({"callback-data": callback_data}, f)

def main():
    iexec_in = os.environ.get('IEXEC_IN', '/iexec_in')
    iexec_out = os.environ.get('IEXEC_OUT', '/iexec_out')
    with open(os.path.join(iexec_in, 'request.json'), 'r') as f:
        request_data = json.load(f)
    response = handle_api_request(request_data)

    with open(os.path.join(iexec_out, 'response.json'), 'w+') as f:
        json.dump(response, f)

if __name__ == '__main__':
    main()
