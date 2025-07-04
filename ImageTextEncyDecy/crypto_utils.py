# File: crypto_utils.py

import os
import base64
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PIL import Image
import numpy as np

def generate_key():
    return AESGCM.generate_key(bit_length=128)

def save_key_hex(key):
    return key.hex()

def load_key_hex(key_hex):
    return bytes.fromhex(key_hex)

def encrypt_text(plain_text, key):
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ct = aesgcm.encrypt(nonce, plain_text.encode(), None)
    return base64.b64encode(nonce + ct).decode()

def decrypt_text(encrypted_text, key):
    aesgcm = AESGCM(key)
    data = base64.b64decode(encrypted_text.encode())
    nonce = data[:12]
    ct = data[12:]
    try:
        pt = aesgcm.decrypt(nonce, ct, None)
        return pt.decode()
    except Exception:
        return "[Decryption Failed]"

def encrypt_image(image_path, key):
    image = Image.open(image_path).convert('RGB')
    data = np.array(image)
    flat = data.flatten()
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    enc_data = aesgcm.encrypt(nonce, flat.tobytes(), None)
    return nonce + enc_data, data.shape

def decrypt_image(encrypted_data, shape, key):
    aesgcm = AESGCM(key)
    nonce = encrypted_data[:12]
    ct = encrypted_data[12:]
    try:
        dec_bytes = aesgcm.decrypt(nonce, ct, None)
        array = np.frombuffer(dec_bytes, dtype=np.uint8).reshape(shape)
        return Image.fromarray(array, 'RGB')
    except Exception:
        return None
