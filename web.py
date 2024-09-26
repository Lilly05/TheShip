import asyncio
import websockets
import json

async def download_data():
    uri = "ws://192.168.100.17:2026/api"
    async with websockets.connect(uri) as websocket:
        # Sobald die Verbindung geöffnet ist
        print("Verbunden mit Elyse Terminal")

        # Sende eine Nachricht an den Server (Download-Daten-Anforderung)
        data = {"source": "Elyse Terminal", "msg": [1, 2, 3, 4]}
        await websocket.send(json.dumps(data))
        print(f"Client -> Server: {data}")

        # Empfange die Antwort vom Server
        response = await websocket.recv()
        print(f"Server <- Client: {response}")
        
        # Hier würdest du die Daten verarbeiten und in den "Permastore" speichern

        return response

async def upload_data_to_azura(data):
    uri = "ws://azura.station:1000/api"  # Fiktiver WebSocket-Endpunkt für Azura Station
    async with websockets.connect(uri) as websocket:
        print("Verbunden mit Azura Station")

        # Sende die heruntergeladenen Daten an Azura Station
        await websocket.send(json.dumps(data))
        print(f"Client -> Server: {data}")

        # Empfang der Bestätigung von Azura Station
        confirmation = await websocket.recv()
        print(f"Server <- Client: {confirmation}")

async def main():
    # Daten von Elyse Terminal herunterladen
    downloaded_data = await download_data()

    # Daten zu Azura Station hochladen
    await upload_data_to_azura(json.loads(downloaded_data))

# Starte den Event-Loop für die asynchrone WebSocket-Kommunikation
asyncio.run(main())
