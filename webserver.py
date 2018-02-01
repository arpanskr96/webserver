import sys
import socket


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
        port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get in there
    s.bind((host, port))
    s.listen(5)

    while(True):
        connection, address = s.accept()
        result = s.recv(2048)
        print(result)

    # example send data
    # s.send("GET / HTTP/{0}\n\n".format(version))

    # example get data
    # result = s.recv(2048)


if __name__ == "__main__":
    main()
