#!/bin/python3
"""Generate password hashes for basic auth."""

import json

from werkzeug.security import generate_password_hash

users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2"),
}

with open("../users.json", "w") as f:
    json.dump(users, f, indent=4)
