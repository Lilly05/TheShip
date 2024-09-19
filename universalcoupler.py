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
        print(msg)

        binary_data = base64.b64decode(msg)

        binary_array = list(binary_data)

        return jsonify({
            "kind": "success",
            "messages": [
                {
                    "destination": dest,
                    "data": binary_array
                }
            ]
        }), 200

    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

@app.route('/<station>/send', methods=['POST'])
def upload(station):
    try:

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form if request.form else json.loads(request.data.decode('utf-8'))

        source = data.get('source')
        data_array = data.get('data')

        print(f"Empfangen von {source}: {data_array}")

        return jsonify({"kind": "success"}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
