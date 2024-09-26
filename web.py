from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# Endpunkt zum Herunterladen von Daten von Elyse Terminal
@app.route('/<station>/receive', methods=['POST'])
def download(station):
    try:
        # Anfrage an Elyse Terminal, um Nachrichten zu erhalten
        response = requests.post('http://192.168.100.17:2029/receive')
        data = response.json()

        # Verarbeite die empfangene Nachricht
        received_message = data['received_messages'][0]
        dest = received_message['dest']
        msg = received_message['msg']

        # Dekodiere die Base64-nachricht in binäre Daten
        binary_data = base64.b64decode(msg)
        binary_array = list(binary_data)  # Konvertiere binäre Daten in eine Liste

        print(f"Empfangene Nachricht: {binary_array}")

        # Erfolgreiche Rückgabe der Nachricht und Zielstation
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
        # Fehlerbehandlung und Rückgabe der Fehlermeldung
        return jsonify({"kind": "error", "message": str(e)}), 500

# Endpunkt zum Hochladen von Daten zu Azura Station
@app.route('/<station>/send', methods=['POST'])
def upload(station):
    try:
        # JSON-Daten von der Anfrage abrufen
        data = request.get_json(force=True)
        print(f"Empfangen von {station}: {data}")

        source = data.get('source')
        data_array = data.get('data')
        binary_data = bytes(data_array)  # Konvertiere die Liste zurück in binäre Daten

        # Base64-kodierte Nachricht erstellen
        base64_encoded_data = base64.b64encode(binary_data).decode('utf-8')
        print(f"Base64-kodierte Nachricht: {base64_encoded_data}")

        # Sende die Base64-nachricht an Azura Station
        requests.post('http://192.168.100.17:2030/put_message', json={"sending_station": source, "base64data": base64_encoded_data})

        # Erfolgreiche Rückgabe
        return jsonify({"kind": "success"}), 200
    except Exception as e:
        # Fehlerbehandlung und Rückgabe der Fehlermeldung
        return jsonify({"kind": "error", "message": str(e)}), 500

# Starte die Flask-Anwendung
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
