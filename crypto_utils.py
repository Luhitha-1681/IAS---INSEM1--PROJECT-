from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# 32-byte key = AES-256
KEY = b'12345678901234567890123456789012'


def encrypt_message(message):
    cipher = AES.new(KEY, AES.MODE_EAX)

    ciphertext, tag = cipher.encrypt_and_digest(
        message.encode('utf-8')
    )

    data = cipher.nonce + tag + ciphertext

    return base64.b64encode(data)


def decrypt_message(data):
    data = base64.b64decode(data)

    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)

    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    return plaintext.decode('utf-8')