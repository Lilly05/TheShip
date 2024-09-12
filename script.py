import requests
import time


for x in range(0, 197):
    requests.put('http://192.168.100.17:2004/thruster', json={"thrust_percent": 100})
    requests.post('http://192.168.100.17:2009/set_target', json={"target": "Vesta Station"})
    time.sleep(30)
    r = requests.post('http://192.168.100.17:2011/buy', json={"station": "Vesta Station", "what": "IRON", "amount": 24})
    print(r.json())
    requests.post('http://192.168.100.17:2009/set_target', json={"target": "Core Station"})
    requests.put('http://192.168.100.17:2004/thruster', json={"thrust_percent": 100})
    time.sleep(30)
    r = requests.post('http://192.168.100.17:2011/sell', json={"station": "Core Station", "what": "IRON", "amount": 24})
    print(r.json())
    print(x)
