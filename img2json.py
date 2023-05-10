import json
import base64
import requests

data = {}
with open('upload/R.jpg', mode='rb') as file:
    img = file.read()
data['image'] = base64.b64encode(img).decode('utf-8')
r = requests.post('http://127.0.0.1:5000//upload', json=data)
print(r.text)