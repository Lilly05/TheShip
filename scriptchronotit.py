import requests
import time

angle = 80
isactive = False

while True:
    angle = 80
    requests.post("http://192.168.100.17:2009/set_target", json={"target": {"x": -37500, "y": 44750}})
    time.sleep(60)

    r = requests.get('http://192.168.100.17:2018/state')
    isactive = r.json()['is_mining']

    while isactive is False:
        requests.put('http://192.168.100.17:2018/angle', json={"angle": angle})
        angle += 20

        requests.post("http://192.168.100.17:2018/activate")
        time.sleep(2)
        r = requests.get('http://192.168.100.17:2018/state')
        requests.post("http://192.168.100.17:2018/deactivate")
        isactive = r.json()['is_mining']

    requests.post("http://192.168.100.17:2018/activate")
    time.sleep(5)
    requests.post("http://192.168.100.17:2018/deactivate")
    requests.post("http://192.168.100.17:2009/set_target", json={"target": "Core Station"})
    time.sleep(45)
