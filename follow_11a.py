import pika
import json
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.100.17", port=2014))
channel = connection.channel()

channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)

for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
    detected_objects = json.loads(body.decode('utf-8'))
    for obj in detected_objects:
        if obj['name'] == 'Station 17-A':
            position = obj['pos']
            print(f"Position von Station 17-A: x={position['x']}, y={position['y']}")
            url = "http://192.168.100.17:2009/set_target"
            data = {"target": {"x": position['x'], "y": position['y']}}
            response = requests.post(url, json=data)
            print("Response Status:", response.status_code)
