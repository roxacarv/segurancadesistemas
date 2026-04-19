import requests
from javascript_token import generate_token

url = "http://localhost:8080/vulnerabilities/javascript/"

phrase = "success"
token = generate_token(phrase)

data = {
    "phrase": phrase,
    "token": token,
    "send": "Submit"
}

cookies = {
    "PHPSESSID": "ee65fro1u01cgc0flakkq4ct44",
    "security": "high"
}

r = requests.post(url, data=data, cookies=cookies)

print(r.text)
