import sys
import socket
import threading # To permit concurrent client connections


def requestHandler():
    pass


def main():
    """
    Basic web server implementing  GET, POST, PUT, DELETE, and CONNECT
    with the basic error reporting codes and a scripting language.
    Return:
        None
    """
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        print("usage: ./webserver.py <IP of interface> <port>")
        print("defaulting to 0.0.0.0:8080.")
        host = "0.0.0.0"
        port = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set up shop
    s.bind((host, port))
    s.listen(10)  # concurrent connections possible

    try:
        while(True):
            # Client is an object representing the client
            # adr is an array of information about the client
            client, adr = s.accept()  # Accept is a blocking call
            print(adr[0], adr[1])
    except:
        s.close()

    # example send data
    # s.send("GET / HTTP/{0}\n\n".format(version))

    # example get data
    # result = s.recv(2048)


if __name__ == "__main__":
    main()
