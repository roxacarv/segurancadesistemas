import hashlib

for i in range(0, 1000000):
    if hashlib.md5(str(i).encode()).hexdigest() == "9bf31c7ff062936a96d3c8bd1f8f2ff3":
        print("Found:", i)
        break
