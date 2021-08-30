import requests
import time

while True:
    api_url = 'http://localhost:80/nodes/resolve'
    response = requests.get(api_url)
    time.sleep(2)