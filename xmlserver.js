const express = require('express');
const xmlrpc = require('xmlrpc');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.text({ type: '*/*' }));
 
const client = xmlrpc.createClient({ host: '192.168.100.17', port: 2024, path: '/RPC2' });
 
app.post('/:station/receive', async (req, res) => {
  try {
    console.log('Making XML-RPC request to receive messages');
 
 
    client.methodCall('receive', [], (error, value) => {
      if (error) {
        console.error('Error in XML-RPC request:', error);
        res.status(500).json({ kind: 'error', message: 'Failed to fetch messages' });
      } else {
        console.log('Received value:', JSON.stringify(value, null, 2));
        try {
          const receivedMessageData = value[0];
          const stationName = receivedMessageData[0];
          const byteArray = receivedMessageData[1];
 
          let resArray = [];
          byteArray.forEach((data) => {
            resArray.push(parseInt(data))
          })
          res.json(
            {
              kind: "success",
              messages: [{destination: stationName, data: resArray}]
            }
          );
        } catch (parseError) {
          console.error('Error parsing the response:', parseError);
          res.status(500).json({ kind: 'error', message: 'Failed to process message data' });
        }
      }
    });

  } catch (error) {
    console.error('Unexpected error:', error);
    res.status(500).json({ kind: "error", message: "Failed to forward request" });
  }
});
 
app.post('/:station/send', async (req, res) => {
  try {
    const parsedBody = JSON.parse(req.body);
    const { source, data } = parsedBody;
 
    const base64Data = Buffer.from(new Uint8Array(data)).toString('base64');
 
    const payload = {
      sending_station: source,
      base64data: base64Data
    };
 
    await axios.post('http://192.168.100.17:2030/put_message', payload);
 
    res.json({ kind: 'success', message: 'Data forwarded successfully' });
  } catch (error) {
    console.error('Unexpected error:', error);
    res.status(500).json({ kind: 'error', message: 'Failed to forward request' });
  }
});
 
app.listen(2023, () => {
  console.log('Universal Coupler Module running on port 2023');
});