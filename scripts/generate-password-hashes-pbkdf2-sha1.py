#!/bin/python3
"""Generate password hashes for basic auth using pbkdf2 and sha1 for deterministic hashes."""

import binascii
import hashlib
import json


def generate_password_hash(
    password: str, salt: str = "fixedsalt", iterations: int = 150000
) -> str:
    """Generate a deterministic pbkdf2:sha1 hash in the same format as Werkzeug's generate_password_hash."""
    password_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    dk = hashlib.pbkdf2_hmac("sha1", password_bytes, salt_bytes, iterations, dklen=20)
    hex_hash = binascii.hexlify(dk).decode("ascii")
    return f"pbkdf2:sha1:{iterations}${salt}${hex_hash}"


users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2"),
}

with open("../users.json", "w") as f:
    json.dump(users, f, indent=4)
