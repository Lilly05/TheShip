from flask import Flask, request, jsonify
import base64
import json
import websocket

app = Flask(__name__)

# WebSocket-Adresse
WS_RECEIVE_URL = 'ws://192.168.100.17:2029/receive'
WS_SEND_URL = 'ws://192.168.100.17:2030/put_message'

@app.route('/<station>/receive', methods=['POST'])
def download(station):
    try:
        # WebSocket-Verbindung zum Empfang herstellen
        ws = websocket.WebSocket()
        ws.connect(WS_RECEIVE_URL)

        # Nachricht empfangen
        response = ws.recv()
        data = json.loads(response)

        received_message = data['received_messages'][0]
        dest = received_message['dest']
        msg = received_message['msg']
        print(msg)

        binary_data = base64.b64decode(msg)
        binary_array = list(binary_data)
        print(binary_array)

        # WebSocket-Verbindung schließen
        ws.close()

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
        data = request.get_json(force=True)
        print(data)

        source = data.get('source')
        data_array = data.get('data')
        binary_data = bytes(data_array)

        print(f"Empfangen von {source}: {data_array}")

        base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
        print(base64_encoded_data)

        # WebSocket-Verbindung zum Senden herstellen
        ws = websocket.WebSocket()
        ws.connect(WS_SEND_URL)

        # Nachricht senden
        ws.send(json.dumps({
            "sending_station": source,
            "base64data": base64_encoded_data
        }))

        # WebSocket-Verbindung schließen
        ws.close()

        return jsonify({"kind": "success"}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
