from flask import Flask, request, jsonify
import requests
import base64
import json

app = Flask(__name__)

# Elyse Terminal Endpunkt (zum Herunterladen von Daten)
ELYSE_TERMINAL_URL = 'http://192.168.100.17:2029/receive'
# Azura Station Endpunkt (zum Hochladen von Daten)
AZURA_STATION_URL = 'http://192.168.100.17:2030/put_message'

# Endpunkt zum Herunterladen der Daten von Elyse Terminal und sie im Permastore zu speichern
@app.route('/elyse/download', methods=['POST'])
def download_from_elyse():
    try:
        # Anfrage an Elyse Terminal, um die Forschungsdaten herunterzuladen
        response = requests.post(ELYSE_TERMINAL_URL)
        response_data = response.json()

        # Extrahiere die empfangenen Nachrichten
        received_message = response_data['received_messages'][0]
        dest = received_message['dest']
        msg = received_message['msg']

        # Dekodiere die Base64-kodierten Daten
        binary_data = base64.b64decode(msg)
        binary_array = list(binary_data)  # Konvertiere sie in ein Array

        print(f"Daten von Elyse Terminal erhalten: {binary_array}")

        # Die empfangenen Daten erfolgreich zurückgeben
        return jsonify({
            "kind": "success",
            "message": "Daten erfolgreich von Elyse Terminal heruntergeladen",
            "data": binary_array,
            "destination": dest
        }), 200

    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

# Endpunkt zum Hochladen der Daten zu Azura Station
@app.route('/azura/upload', methods=['POST'])
def upload_to_azura():
    try:
        # JSON-Daten von der Anfrage abrufen
        request_data = request.get_json()
        source = request_data.get('source')
        data_array = request_data.get('data')

        # Konvertiere die Liste in binäre Daten
        binary_data = bytes(data_array)

        # Base64-kodiere die Daten
        base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')

        # Daten zu Azura Station hochladen
        upload_response = requests.post(AZURA_STATION_URL, json={
            "sending_station": source,
            "base64data": base64_encoded_data
        })

        print(f"Daten an Azura Station gesendet: {data_array}")

        # Bestätigung der erfolgreichen Übertragung
        return jsonify({"kind": "success", "message": "Daten erfolgreich zu Azura Station hochgeladen"}), 200

    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
