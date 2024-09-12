import requests
import time

for x in range(0, 100):
    requests.post('http://192.168.100.17:2009/set_target', json={"target": {"x": 4296, "y": -5278}})
    time.sleep(20)
    requests.post('http://192.168.100.17:2011/buy', json={"station": "Shangris Station", "what": "GOLD", "amount": 12})
    time.sleep(3)
    requests.post('http://192.168.100.17:2009/set_target', json={"target": "Core Station"})
    time.sleep(20)
    requests.post('http://192.168.100.17:2011/sell', json={"station": "Core Station", "what": "GOLD", "amount": 12})


