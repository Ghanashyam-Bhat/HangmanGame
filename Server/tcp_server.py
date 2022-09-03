from socket import AF_INET, SOCK_STREAM, socket

def get(conn, filename):
    try:

        with open(filename, 'r') as infile:
            for line in infile:
                conn.sendall(line.encode('utf-8'))    

        end_message = "EOF-STOP"
        conn.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        conn.sendall("ERROR".encode('utf-8'))

def server():
    command_list = ["QUIT","GET"]

    HOST = '127.0.0.1'
    PORT = 12000

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))

    while True:
        sock.listen()
        conn, addr = sock.accept()
        print("Connected to " , addr)

        remainder = ""
        while (True):
            command = ""
            if remainder == "":
                # if there's no leftover message, recieve a new one
                data = conn.recv(1024).decode("utf-8")
                command = data.split(' ')[0].upper()
            else:
                # if there is a leftover message then execute it
                data = remainder
                space = remainder.find(' ')
                command = remainder[:space].upper()
                remainder = ""

            if command in command_list:
                if command == "QUIT":
                    print("Client quitting")
                    conn.sendall(command.encode("utf-8"))
                    conn.close()
                    break
                
                
                if command == "GET":
                    filename = data.split(' ')[1]
                    get(conn, filename)
            else:
                print(f"'{data}' is not a valid command")
                conn.sendall(data.encode("utf-8"))

        print("Disconnected from:", addr)

    sock.close()
if __name__ == "__main__":
    server()