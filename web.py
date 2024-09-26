from flask import Flask, request, jsonify
import asyncio
import websockets
import base64
import json

app = Flask(__name__)

# Funktion zum Herunterladen von Daten über WebSockets von Elyse Terminal
async def download_data_from_elyse(station_data):
    uri = "ws://192.168.100.17:2026/api"
    try:
        async with websockets.connect(uri) as websocket:
            # Dynamisches Senden der Daten, die von der Anfrage kommen
            await websocket.send(json.dumps(station_data))

            # Antwort von Elyse Terminal empfangen
            response = await websocket.recv()
            print(f"Empfangen von Elyse Terminal: {response}")

            # Verarbeitung der empfangenen Nachricht
            received_message = json.loads(response)
            msg = received_message['msg']
            dest = received_message['destination']

            # Dekodieren der Base64-kodierten Nachricht
            binary_data = base64.b64decode(msg)
            binary_array = list(binary_data)  # Konvertiere die binäre Nachricht in ein Array
            return {"destination": dest, "data": binary_array}
    except Exception as e:
        return {"error": str(e)}

# Funktion zum Hochladen von Daten über WebSockets zu Azura Station
async def upload_data_to_azura(data):
    uri = "ws://azura.station:1000/api"
    try:
        async with websockets.connect(uri) as websocket:
            # Senden der dynamisch erhaltenen Daten
            await websocket.send(json.dumps(data))
            print(f"Daten an Azura Station gesendet: {data}")

            # Empfang der Bestätigung von Azura Station
            confirmation = await websocket.recv()
            print(f"Bestätigung von Azura Station: {confirmation}")
            return confirmation
    except Exception as e:
        return {"error": str(e)}

# Flask-Endpunkt zum Herunterladen von Daten von Elyse Terminal
@app.route('/<station>/receive', methods=['POST'])
def download(station):
    try:
        # Daten aus der Anfrage abrufen
        station_data = request.get_json(force=True)

        # Starte die WebSocket-Kommunikation zum Herunterladen von Daten
        data = asyncio.run(download_data_from_elyse(station_data))
        if "error" in data:
            raise Exception(data["error"])

        # Erfolgreiche Rückgabe der empfangenen Daten
        return jsonify({
            "kind": "success",
            "messages": [
                {
                    "destination": data['destination'],
                    "data": data['data']
                }
            ]
        }), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

# Flask-Endpunkt zum Hochladen von Daten zu Azura Station
@app.route('/<station>/send', methods=['POST'])
def upload(station):
    try:
        # JSON-Daten von der Anfrage abrufen
        data = request.get_json(force=True)
        source = data.get('source')
        data_array = data.get('data')

        # Konvertiere die Liste der Daten in binäres Format und kodiert sie in Base64
        binary_data = bytes(data_array)
        base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')

        # Bereite die Nachricht vor, um sie zu Azura Station zu senden
        message = {
            "sending_station": source,
            "base64data": base64_encoded_data
        }

        # Starte die WebSocket-Kommunikation zum Hochladen von Daten
        confirmation = asyncio.run(upload_data_to_azura(message))
        if "error" in confirmation:
            raise Exception(confirmation["error"])

        return jsonify({"kind": "success"}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
