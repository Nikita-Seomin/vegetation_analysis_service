import socket
import sys
s = socket.socket()
s.bind(("localhost",8000))
s.listen(10) # Acepta hasta 10 conexiones entrantes.


while True:
    sc, address = s.accept()


    while (True):
        # recibimos y escribimos en el fichero
        l = sc.recv(1024)

        if not l:
            break

    sc.close()
    print('copied the file.')

s.close()