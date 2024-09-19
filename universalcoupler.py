from flask import Flask, request, jsonify
import boto3
import json
import requests
import base64

app = Flask(__name__)

@app.route('/<station>/receive', methods=['POST'])
def download(station):
    try:
        response = requests.post('http://192.168.100.17:2029/receive')
        data = response.json()
    
        received_message = data['received_messages'][0]
        dest = received_message['dest']
        msg = received_message['msg']

        base64_bytes = base64.b64decode(msg)
        decoded_message = base64_bytes.decode('utf-8')

        decoded_json = json.loads(decoded_message)

        message = decoded_json['message']

        message_json = json.loads(message)
        data_array = [
            message_json['source'],       
            message_json['destination'],  
            message_json['data'],        
            message_json['ts']         
        ]

        return jsonify({"kind": "success", "messages": [{"destination": dest, "data": data_array}]}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": "Fehler"}), 500

@app.route('/<station>/send', methods=['POST'])
def upload(station):
    try:
        data = request.get_json()
        
        source = data.get('source')
        data_array = data.get('data')

        print(f"Empfangen von {source}: {data_array}")

        return jsonify({"kind": "success"}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": "Fehler"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
