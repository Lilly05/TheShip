const websocket = require("websocket").w3cwebsocket;

const ws = new websocket("ws://192.168.100.17:2026/api");
const receivedMessages = new Set(); // Set zum Verfolgen empfangener Nachrichten

ws.onmessage = (event) => {
    try {
        const receivedMessage = JSON.parse(event.data); 
        const dest = receivedMessage.destination; 
        const msg = receivedMessage.msg; 

        const messageId = receivedMessage.id; 

        if (receivedMessages.has(messageId)) {
            console.log("Nachricht wurde bereits empfangen:", messageId);
            return; 
        }

        const binary_data = Buffer.from(msg, 'base64'); 
        const binary_array = Array.from(binary_data); 

        console.log("Received msg:", msg); 
        console.log("Destination:", dest); 
        console.log("Binary Array:", binary_array); 

        const response = {
            kind: "success",
            messages: [
                {
                    destination: dest,
                    data: binary_array
                }
            ]
        };
        ws.send(JSON.stringify(response)); 

        receivedMessages.add(messageId);
    } catch (error) {
        console.error("Fehler beim Verarbeiten der Nachricht:", error);
    }
};

ws.onopen = () => {
    console.log("connected");
    const data = { source: "Artemis Station", msg: [1, 2, 3, 4].map(x => x.toString(2)).join('') }; // Beispiel-Daten
    console.log("client -> server: " + JSON.stringify(data));
    ws.send(JSON.stringify(data));
};


