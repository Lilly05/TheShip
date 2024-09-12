from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

# S3 Konfiguration (hardcodiert)
S3_HOST = 'http://192.168.100.17:2016'
S3_BUCKET = 'theship-permastore'
S3_ACCESS_KEY = 'theship'
S3_SECRET_KEY = 'theship1234'

# S3 Client
s3_client = boto3.client('s3', 
                         endpoint_url=S3_HOST,
                         aws_access_key_id=S3_ACCESS_KEY,
                         aws_secret_access_key=S3_SECRET_KEY)

def save_message_to_s3(destination, message):
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=f'{destination}/messages.json',
        Body=message
    )

def get_messages_from_s3(station):
    response = s3_client.get_object(Bucket=S3_BUCKET, Key=f'{station}/messages.json')
    data = response['Body'].read().decode('utf-8')
    return data

# API für Empfangen von Nachrichten
@app.route('/<station>/receive', methods=['POST'])
def receive(station):
    try:
        messages = get_messages_from_s3(station)
        return jsonify({"kind": "success", "messages": messages}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

# API für Senden von Nachrichten
@app.route('/<station>/send', methods=['POST'])
def send(station):
    try:
        data = request.json
        destination = data['destination']
        message = data['data']
        save_message_to_s3(destination, str(message))
        return jsonify({"kind": "success"}), 200
    except Exception as e:
        return jsonify({"kind": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023)
