import requests
import time
import json

angle = 360

for x in range(0, 200):
    requests.post("http://192.168.100.17:2018/activate")
    time.sleep(5)
    