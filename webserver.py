import sys
import socket
import threading  # To permit concurrent client connections
import json  # To read config files


def getConfig(configfile):
    """
    Retrieve configuration from settings file
    Params:
        configfile: String containing config file name
    Return:
        Dictionary linking settings keywords to definitions
    """
    with open(configfile) as f:
        data = json.load(f)
    return data


def requestHandler(client):
    """
    A thread used to parse and respond to a particular HTTP request.
    Params:
        client - a socket object representing the client.
    Return:
        None
    """
    print("Received: {}".format(client.recv(2048)))
    response = "HTTP/1.1 200 OK\r\n\r\n"
    body = "Hello World!"
    client.send(response + body)
    # Because HTTP is connectionless we close it at the end of every action
    client.close()


def main():
    """
    Basic web server implementing  GET, POST, PUT, DELETE, and CONNECT
    with the basic error reporting codes and a scripting language.
    Return:
        None
    """
    try:
        conf = getConfig(sys.argv[1])
    except IndexError:
        print("usage: ./webserver.py <configfile>")
        print("Defaulting to \"webserver.cfg\"")
        conf = getConfig("webserver.cfg")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set up shop
    s.bind((conf["host"], int(conf["port"])))
    s.listen(10)  # concurrent connections possible

    try:
        while(True):
            # Client is an object representing the client
            # adr is an array of information about the client
            client, adr = s.accept()  # Accept is a blocking call

            # requestHandler is the function being run in the thread
            # args are the parameters it takes
            # Yes you need the dumb comma because it needs to be iterable
            threading.Thread(target=requestHandler, args=(client,)).start()

    except socket.error, exc:
        print("Caught exception socket.error : {}".format(exc))


if __name__ == "__main__":
    main()
