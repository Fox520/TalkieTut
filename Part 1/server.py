import socket,threading

s = socket.socket()
host = "0.0.0.0"
port = 5005
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(5)
client_sockets = []

def handle_client(conn):
    while True:
        try:
            data = conn.recv(512)
            for x in client_sockets:
                try:
                    x.send(data)
                except Exception as e:
                    print "Error:",e
        except:
            pass
print "Listening"

while True:
    conn, addr = s.accept()
    client_sockets.append(conn)
    conn.send("Creator says hello")
    print "Connection from",addr[0], "on port", addr[1]
    threading.Thread(target=handle_client, args=(conn,)).start()