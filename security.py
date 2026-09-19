import base64
import hashlib
import hmac
import os


ITERATIONS = 180000
SALT_LENGTH = 32


def hash_password(password):
    """
    Create a salted PBKDF2-HMAC-SHA256 password hash.
    """

    if not isinstance(password, str):
        raise ValueError("Password must be text.")

    salt = os.urandom(SALT_LENGTH)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    encoded_salt = base64.b64encode(salt).decode("ascii")
    encoded_hash = base64.b64encode(password_hash).decode("ascii")

    return encoded_salt, encoded_hash


def verify_password(password, encoded_salt, encoded_hash):
    """
    Verify a password against a stored PBKDF2 hash.
    """

    try:
        salt = base64.b64decode(encoded_salt.encode("ascii"))
        expected_hash = base64.b64decode(
            encoded_hash.encode("ascii")
        )

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            ITERATIONS
        )

        return hmac.compare_digest(
            password_hash,
            expected_hash
        )

    except Exception:
        return False
