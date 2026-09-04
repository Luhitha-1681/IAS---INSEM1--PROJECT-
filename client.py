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
# ---------------------------------------------------------
def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text]


# ---------------------------------------------------------
# Convert numbers to text
# ---------------------------------------------------------
def numbers_to_text(numbers):
    return ''.join(chr(int(num) + ord('A')) for num in numbers)


# ---------------------------------------------------------
# Find inverse key matrix modulo 26
# ---------------------------------------------------------
def inverse_matrix_mod26(matrix):

    a, b = matrix[0]
    c, d = matrix[1]

    determinant = (a * d - b * c) % 26

    inverse_det = mod_inverse(determinant, 26)

    if inverse_det is None:
        raise ValueError("Key matrix has no modular inverse.")

    inverse_matrix = np.array([
        [d, -b],
        [-c, a]
    ])

    inverse_matrix = (inverse_det * inverse_matrix) % 26

    return inverse_matrix.astype(int)


# ---------------------------------------------------------
# Hill Cipher Decryption
# ---------------------------------------------------------
def hill_decrypt(ciphertext, key_matrix):

    inverse_key = inverse_matrix_mod26(key_matrix)

    numbers = text_to_numbers(ciphertext)

    plaintext = []

    for i in range(0, len(numbers), 2):

        block = np.array([
            [numbers[i]],
            [numbers[i + 1]]
        ])

        decrypted_block = np.dot(inverse_key, block) % 26

        plaintext.extend(decrypted_block.flatten())

    return numbers_to_text(plaintext)


# ---------------------------------------------------------
# Client
# ---------------------------------------------------------
print("======================================")
print("       HILL CIPHER CLIENT")
print("======================================")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to server...")

client_socket.connect((HOST, PORT))

print("Connected to server.")

# Enter plaintext
plaintext = input("\nEnter plaintext: ")

print("\n========== SENDING PLAINTEXT ==========")
print("Plaintext:", plaintext)

# Send plaintext to server
client_socket.send(plaintext.encode())

# Receive ciphertext
ciphertext = client_socket.recv(4096).decode()

print("\n========== RECEIVED CIPHERTEXT ==========")
print("Ciphertext:", ciphertext)

# Hill Cipher key
key_matrix = np.array([
    [3, 3],
    [2, 5]
])

print("\n========== KEY MATRIX ==========")
print(key_matrix)

# Decrypt
decrypted_text = hill_decrypt(ciphertext, key_matrix)

print("\n========== DECRYPTION ==========")
print("Ciphertext :", ciphertext)
print("Plaintext  :", decrypted_text)

print("\n======================================")
print("       HILL CIPHER COMPLETED")
print("======================================")

client_socket.close()