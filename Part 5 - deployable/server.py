import socket,threading,json

s = socket.socket()
host = "0.0.0.0"
port = 5005
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(5)
client_sockets = []
client_name_and_socket = {}

def handle_client(conn):
    while True:
        try:
            data = json.loads(conn.recv(512))
            msg_type = data["msg_type"]

            if msg_type == "broadcast":# send to everyone
                template = {} #send this to all clients
                template["msg_type"] = "broadcast"
                template["msg"] = data["msg"]
                template["from"] = data["from"]

                for x in client_sockets:
                    try:
                        x.send(json.dumps(template))
                    except Exception as e:
                        print "Error:",e
            elif msg_type == "private_message":
                template = {} #send this to one clients
                template["msg_type"] = "broadcast"
                template["msg"] = data["msg"]
                template["from"] = data["from"]
                name_to_send_to = data["pvt_receiver"]
                # try:
                print "1"
                connection_to_use = client_name_and_socket[name_to_send_to]
                print "2"
                connection_to_use.send(json.dumps(template))
                print "sent"
                # except Exception as e:
                #     print e


            elif msg_type == "image":
                template = {} #send this to all clients
                template["msg_type"] = "image"
                template["link"] = data["link"]
                template["from"] = data["from"]
                for x in client_sockets:
                    try:
                        x.send(json.dumps(template))
                    except Exception as e:
                        print "Error:",e

        except:
            pass
print "Listening"

while True:
    conn, addr = s.accept()
    client_sockets.append(conn)
    conn.send("Creator says hello")
    temp_data = json.loads(conn.recv(512))
    client_name = temp_data["name"]

    client_name_and_socket[client_name] = conn

    print "Connection from",addr[0], "on port", addr[1]
    threading.Thread(target=handle_client, args=(conn,)).start()