import socket
import numpy as np


HOST = "127.0.0.1"
PORT = 5000


# ---------------------------------------------------------
# Find modular inverse
# ---------------------------------------------------------
def mod_inverse(a, m):
    a = a % m

    for x in range(1, m):
        if (a * x) % m == 1:
            return x

    return None


# ---------------------------------------------------------
# Convert text to numbers
# A = 0, B = 1, ..., Z = 25
# ---------------------------------------------------------
def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text]


# ---------------------------------------------------------
# Convert numbers to text
# ---------------------------------------------------------
def numbers_to_text(numbers):
    return ''.join(chr(int(num) + ord('A')) for num in numbers)


# ---------------------------------------------------------
# Hill Cipher Encryption
# ---------------------------------------------------------
def hill_encrypt(plaintext, key_matrix):

    plaintext = plaintext.upper().replace(" ", "")

    # Padding if number of characters is odd
    if len(plaintext) % 2 != 0:
        plaintext += "X"

    numbers = text_to_numbers(plaintext)

    ciphertext = []

    for i in range(0, len(numbers), 2):

        block = np.array([
            [numbers[i]],
            [numbers[i + 1]]
        ])

        encrypted_block = np.dot(key_matrix, block) % 26

        ciphertext.extend(encrypted_block.flatten())

    return numbers_to_text(ciphertext)


# ---------------------------------------------------------
# Server
# ---------------------------------------------------------
print("======================================")
print("       HILL CIPHER SERVER")
print("======================================")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")
print("Waiting for client connection...")

conn, address = server_socket.accept()

print(f"\nClient connected: {address}")

# Receive plaintext
data = conn.recv(4096).decode()

print("\n========== RECEIVED PLAINTEXT ==========")
print(data)

# Hill Cipher key
key_matrix = np.array([
    [3, 3],
    [2, 5]
])

print("\n========== KEY MATRIX ==========")
print(key_matrix)

# Encrypt
ciphertext = hill_encrypt(data, key_matrix)

print("\n========== ENCRYPTION ==========")
print("Plaintext :", data.upper().replace(" ", ""))
print("Ciphertext:", ciphertext)

# Send ciphertext to client
conn.send(ciphertext.encode())

print("\nCiphertext sent to client.")

conn.close()
server_socket.close()

print("\n======================================")
print("       SERVER CLOSED")
print("======================================")