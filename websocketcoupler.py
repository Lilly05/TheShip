from flask import Flask, request, jsonify
import requests
import base64
import json
import websocket

app = Flask(__name__)
global_response = {}

def on_open(ws):
    print("connected")
    data = {
        "source": "Artemis Station",
        "msg": ''.join(format(x, 'b') for x in [1, 2, 3, 4])
    }
    print("client -> server:", json.dumps(data))
    ws.send(json.dumps(data))

def on_message(ws, message):
    print("Nachricht empfangen:", message)
    try:
        received_message = json.loads(message)
        dest = received_message['destination']
        msg = received_message['msg']

        binary_array = ''.join(format(x, 'b') for x in msg)

        print("Destination:", dest)
        print("Binary Array:", binary_array)

        global_response = {
            "kind": "success",
            "messages": [
                {
                    "destination": dest,
                    "data": binary_array
                }
            ]
        }

    except Exception as e:
        print("Fehler beim Verarbeiten der Nachricht:", e)

def on_error(ws, error):
    print("WebSocket Fehler:", error)

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    ws_url = "ws://192.168.100.17:2026/api"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()


@app.route('/<station>/receive', methods=['POST'])
def download(station):
    try:
        msg = global_response
        print(msg)

        return msg, 200

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

        requests.post('http://192.168.100.17:2030/put_message', json={"sending_station": source, "base64data": base64_encoded_data})

        return jsonify({"kind": "success"}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)