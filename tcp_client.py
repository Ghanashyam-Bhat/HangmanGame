from socket import AF_INET, SOCK_STREAM, socket

def get(sock, filename):   
    try:
        # get data and write to file until recieve end signal
        data = sock.recv(1024).decode("utf-8")
        if data=="ERROR":
            print("File doesn't exits\n")
        else:
            with open(filename, 'w') as outfile:
                while(data):
                    outfile.write(data)
                    data = sock.recv(1024).decode("utf-8")
                    # if the data contains the end signal, stop
                    if "EOF-STOP" in data:
                        stop_point = data.find("EOF-STOP")
                        outfile.write(data[:stop_point])
                        print(f"recieved file {filename}")
                        return data[stop_point+8:]
                        
    except Exception as e:
        print(e)
        error_message = "There has been an error recieving the requested file."
        sock.sendall(error_message.encode('utf-8'))

def client(arg):
    command_list = ["QUIT","GET"]

    HOST = '127.0.0.1'
    PORT = 12000

    # set up the tcp socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))

    # read command from user and send to server
    s = "GET "+ arg+".txt"
    sock.sendall(s.encode("utf-8"))
    command = s.split(' ')[0].upper()

    if command in command_list:
        if command == "QUIT":
            # end the client connection.
            print("Goodbye :)")

        if command == "GET":
            filename = s.split(' ')[1]
            remainder = get(sock, filename)
            sock.sendall("QUIT".encode("utf-8"))
    else:
        # if it's not a command 
        data = sock.recv(1024).decode("utf-8")
        print ("Invalid command")

    sock.close()