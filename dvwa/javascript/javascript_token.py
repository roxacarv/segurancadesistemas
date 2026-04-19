import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def generate_token(phrase: str) -> str:
    # Part 1 > reverse
    token = phrase[::-1]

    # Part 2 > sha256("XX" + token)
    token = sha256("XX" + token)

    # Part 3 > sha256(token + "ZZ")
    token = sha256(token + "ZZ")

    return token


# Testing with the expected value
phrase = "success"
token = generate_token(phrase)

print("Phrase:", phrase)
print("Token:", token)
