import socket


HOST = "127.0.0.1"
PORT = 5003


print("======================================")
print("     DIFFIE-HELLMAN CLIENT")
print("======================================")


# Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to server...")

client_socket.connect((HOST, PORT))

print("Connected to server.")


# ---------------------------------------------------------
# Receive public parameters and server public key
# ---------------------------------------------------------
data = client_socket.recv(4096).decode()

p, g, server_public_key = data.split("|")

p = int(p)
g = int(g)
server_public_key = int(server_public_key)


print("\n========== RECEIVED FROM SERVER ==========")
print("Prime number (p):", p)
print("Generator (g)  :", g)
print("Server Public Key:", server_public_key)


# ---------------------------------------------------------
# Client private key
# ---------------------------------------------------------
private_key = 15

print("\nClient Private Key:", private_key)


# ---------------------------------------------------------
# Client public key
# B = g^b mod p
# ---------------------------------------------------------
public_key = pow(g, private_key, p)

print("Client Public Key :", public_key)


# Send client public key to server
client_socket.send(str(public_key).encode())


# ---------------------------------------------------------
# Calculate shared secret
# Secret = A^b mod p
# ---------------------------------------------------------
shared_secret = pow(server_public_key, private_key, p)

print("\n========== SHARED SECRET ==========")
print("Client Shared Secret:", shared_secret)


# Receive server's shared secret
server_secret = int(client_socket.recv(4096).decode())

print("\n========== VERIFICATION ==========")
print("Client Shared Secret :", shared_secret)
print("Server Shared Secret :", server_secret)


if shared_secret == server_secret:
    print("SUCCESS: Both sides have the same secret key.")
else:
    print("ERROR: Shared keys do not match.")


print("\n======================================")
print(" DIFFIE-HELLMAN KEY EXCHANGE COMPLETED")
print("======================================")


client_socket.close()