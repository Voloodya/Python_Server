import socket
import os
import sys


def mysend (client_socket, msg):
	totalsend=0
	while totalsend<len(msg):
		sent=client_socket.send(msg[totalsend:])
		if sent==0:
			raise RuntimeError('broken')
		totalsend=totalsend+sent

		
server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0',2222))
server_socket.listen(10)

while True:
	client_socket, remote_address=server_socket.accept()
	child_pid=os.fork() 
	if child_pid==0:
		while True:
			data_request=client_socket.recv(1024)
			if not data_request or data_request.decode('utf8').strip()=='close': break
			mysend (client_socket,data_request)
		client_socket.close()
		sys.exit()
	else: 
		client_socket.close()
		
server_socket.close()	