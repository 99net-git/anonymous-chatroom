import json, bcrypt

username = input("Enter new username: ")
password = input("Enter password: ")

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

try:
    with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = {}

users[username] = hashed.decode()

with open("users.json", "w") as f:
    json.dump(users, f, indent=4)

print(f"User '{username}' added successfully.")