#!/bin/python3
"""Generate password hashes for basic auth using scrypt for deterministic hashes."""

import binascii
import hashlib
import json


def generate_password_hash(
    password: str,
    salt: str = "fixedsalt",
    n: int = 16384,
    r: int = 8,
    p: int = 1,
    dklen: int = 64,
) -> str:
    """Generate a Werkzeug-compatible scrypt hash deterministically.

    Format: scrypt:<n>:<r>:<p>$<salt>$<hash>
    """
    password_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    key = hashlib.scrypt(password_bytes, salt=salt_bytes, n=n, r=r, p=p, dklen=dklen)
    hex_hash = binascii.hexlify(key).decode("ascii")
    return f"scrypt:{n}:{r}:{p}${salt}${hex_hash}"


users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2"),
}

with open("../users.json", "w") as f:
    json.dump(users, f, indent=4)
