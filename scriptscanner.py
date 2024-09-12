import pika  
import json
import requests
 
# Verbindung zum AMQP-Broker herstellen
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.100.17:2000/', port=2000))
channel = connection.channel()
 
# Erstellen und Binden eines Exchange
channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)
 
# Empfange und verarbeite die Nachrichten
for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
    detected_objects = json.loads(body.decode('utf-8'))
    print(detected_objects)
    # Überprüfe, ob die Station 17-A unter den gefundenen Objekten ist
    for obj in detected_objects:
        if obj['name'] == 'Station 17-A':
            position = obj['pos']
            print(f"Station 17-A gefunden! Position: {position}")
            # Hier kannst du weiter mit der gefundenen Position arbeiten
            break
 
 
# Angenommene URL für das Speichern der Stationen-Position
url = 'http://192.168.100.17:2000//update_position'
 
# Beispiel-Daten
data = {
    'station': '17-A',
    'pos': position
}
 
response = requests.post(url, json=data)
print(response.json())