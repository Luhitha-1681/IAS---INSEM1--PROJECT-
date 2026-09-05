import socket


HOST = "127.0.0.1"
PORT = 5003


print("======================================")
print("     DIFFIE-HELLMAN SERVER")
print("======================================")


# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")
print("Waiting for client connection...")


# Accept client
conn, address = server_socket.accept()

print(f"\nClient connected: {address}")


# ---------------------------------------------------------
# Public parameters
# ---------------------------------------------------------
p = 23
g = 5

print("\n========== PUBLIC PARAMETERS ==========")
print("Prime number (p):", p)
print("Generator (g)  :", g)


# ---------------------------------------------------------
# Server private key
# ---------------------------------------------------------
private_key = 6

print("\nServer Private Key:", private_key)


# ---------------------------------------------------------
# Server public key
# A = g^a mod p
# ---------------------------------------------------------
public_key = pow(g, private_key, p)

print("Server Public Key :", public_key)


# Send p, g and server public key to client
message = f"{p}|{g}|{public_key}"

conn.send(message.encode())


# ---------------------------------------------------------
# Receive client public key
# ---------------------------------------------------------
client_public_key = int(conn.recv(4096).decode())

print("\n========== RECEIVED FROM CLIENT ==========")
print("Client Public Key:", client_public_key)


# ---------------------------------------------------------
# Calculate shared secret
# Secret = B^a mod p
# ---------------------------------------------------------
shared_secret = pow(client_public_key, private_key, p)

print("\n========== SHARED SECRET ==========")
print("Server Shared Secret:", shared_secret)


# Send shared secret to client for demonstration
conn.send(str(shared_secret).encode())


print("\n======================================")
print(" DIFFIE-HELLMAN KEY EXCHANGE COMPLETED")
print("======================================")


conn.close()
server_socket.close()