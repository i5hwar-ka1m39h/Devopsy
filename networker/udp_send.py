import socket


target_source = "127.0.0.1"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


client.sendto("AABBCCDDEE".encode(), (target_source, target_port))


repsonse = client.recvfrom(4096)

print(repsonse)