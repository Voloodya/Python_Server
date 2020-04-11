import socket
import os
import sys

#Открывается сокет server_socket, на который принимается соединение. После получения соединения
#ему выделяется дескриптор client_socket. Дескриптор из главного процесса передается во вновь созданный
#дочерний процесс. В главном процессе соединение закрывается и он продолжает слушать server_socket.

def mysend (client_socket, msg):
	totalsend=0
	while totalsend<len(msg):
		sent=client_socket.send(msg[totalsend:])
		if sent==0:
			#Вызов исключения с типом RuntimeError('broken')
			raise RuntimeError('broken')
		totalsend=totalsend+sent

		
server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Связывание порта с адресом. Если ip пустой, то будет слушать со всех адрессов
server_socket.bind(('0.0.0.0',2222))
#Говорим, что нужно слушать и устанавливаем объем входящей очереди
# (превышающие будут отбрасываться)
server_socket.listen(10)

while True:
	#Получение у ОС файлового (сокет) дескриптора (родительского) (Когда создается новый поток ввода-вывода,
	#ядро возвращает процессу, создавшему поток ввода-вывода, его файловый дескриптор) на открытый сокет, 
	#для конкретного соединения. На 1-н сокет создается 1-н дескриптор, на дискриптор будет ссылаться 2 процесса
	# - родительский и дочерний
	client_socket, remote_address=server_socket.accept()
	# Создание дочернего процесса (в него копируются вся память, структуры, ...). Создается копия выполняемого процесса
	# и запускает его с тчк., где мы вызвали fork(). fork() вернет либо 0, либо pid  процесса
	child_pid=os.fork() 
	if child_pid==0: #Работа в дочернем процессе
		while True:
			data_request=client_socket.recv(1024)
			if not data_request or data_request.decode('utf8').strip()=='close': break
			mysend (client_socket,data_request)
		client_socket.close()
		sys.exit()
	else: # Продолжается выполнение родительского процесса. 
		# Закрытие соединения в родительском процессе после передачи соединения дочерн. проц-су. После закрытия продолжает слушать
		# переменную server_socket
		client_socket.close()
		
server_socket.close()	
