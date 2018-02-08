import subprocess
import sys
import socket
import threading  # To permit concurrent client connections
import json  # To read config files


def getResponse(request):
    """
    Generates HTTP response for a request
    Params:
        request: an un-sanitized string containing the user's request.
    Return:
        String containing response code
    Potential returns:
        200, 400, 401, 403, 404, 411, 500, 505
    """
    return "HTTP/1.1 200 OK\r\n"


def getHeaders(request):
    """
    Isolates headers in un-sanitized input
    Params:
        request: an un-sanitized string containing the user's request.
    Return:
        Dictionary of headers
    """
    return "\r\n"


def getPhp(page):
    """
    Isolates headers in un-sanitized input
    Params:
        page: a file that the web server is hosting.
    Return:
        The whole file as a string
    """
    # with open(page) as p:
    #    output = p.readlines()
    result = subprocess.check_output(["php", page])
    return result


def parseRequest(request):
    """
    Generates HTTP response for a request
    Params:
        request: an un-sanitized string containing the user's request.
    """
    response = getResponse(request)
    headers = getHeaders(request)
    return response + headers


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
    response = parseRequest(client.recv(2048))

    body = getPhp("basic.php") + "\r\n\r\n"
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
