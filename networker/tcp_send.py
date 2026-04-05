import socket



target_source = "0.0.0.0"
target_port = 9998



client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_source, target_port))

client.send("hellow there!".encode())

response = client.recv(4096)

print(response)

