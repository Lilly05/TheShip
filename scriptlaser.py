import requests
import time
import json

angle = 360

for x in range(0, 200):
    requests.put('http://192.168.100.17:2004/thruster', json={"thrust_percent": 100})
    requests.post('http://192.168.100.17:2009/set_target', json={"target": {"x": -9650, "y": 20500}})
    time.sleep(35)
    requests.put('http://192.168.100.17:2018/angle', json={"angle": 160})
    time.sleep(10)
    for y in range (0, 12):
        requests.post("http://192.168.100.17:2018/activate")
        time.sleep(10)
    requests.post('http://192.168.100.17:2009/set_target', json={"target": "Core Station"})
    requests.put('http://192.168.100.17:2004/thruster', json={"thrust_percent": 100})
    time.sleep(35)
    for z in range (0, 24):
        r = requests.post('http://192.168.100.17:2011/sell', json={"station": "Core Station", "what": "GOLD", "amount": 1})
        print(r.json())
        r = requests.post('http://192.168.100.17:2011/sell', json={"station": "Core Station", "what": "STONE", "amount": 1})
        print(r.json())
    print(x)
    