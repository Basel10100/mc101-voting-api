import os
from typing import Tuple
from pydantic import SecretStr
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config import Settings

settings = Settings()

PBKDF_ITERATIONS = 390000
KEY_LENGTH = 32  # AES-256
NONCE_LENGTH = 12  # AESGCM standard
SALT_LENGTH = 16


def _derive_key(secret: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=PBKDF_ITERATIONS,
    )
    return kdf.derive(secret)


def encrypt_note(plaintext: str, personal_password: SecretStr | None) -> Tuple[bytes, bytes, bytes, bool]:
    """
    Encrypt note content using AES-GCM.
    - If personal_password is provided: derive key from it (user-level encryption)
    - Otherwise: derive key from app-level APP_ENCRYPTION_KEY
    Returns: (ciphertext, nonce, salt, personal_encryption_flag)
    """
    salt = os.urandom(SALT_LENGTH)
    nonce = os.urandom(NONCE_LENGTH)
    if personal_password is not None:
        secret = personal_password.get_secret_value().encode()
        personal = True
    else:
        secret = settings.APP_ENCRYPTION_KEY.get_secret_value().encode()
        personal = False
    key = _derive_key(secret, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return ciphertext, nonce, salt, personal


def decrypt_note(ciphertext: bytes, nonce: bytes, salt: bytes, personal_encryption: bool, provided_password: SecretStr | None) -> str:
    """
    Decrypt note content using AES-GCM.
    - If personal_encryption is True: provided_password must be present
    - Else: use app-level APP_ENCRYPTION_KEY
    """
    if personal_encryption:
        if provided_password is None:
            raise ValueError("Password required to decrypt personal note")
        secret = provided_password.get_secret_value().encode()
    else:
        secret = settings.APP_ENCRYPTION_KEY.get_secret_value().encode()

    key = _derive_key(secret, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()
