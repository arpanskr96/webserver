import subprocess
import sys
import socket
import threading  # To permit concurrent client connections
import json  # To read config files
import logging


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
    version = "HTTP/1.1 "
    response = "200 OK"
    return version + response + "\r\n"


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
    print(request[:4])
    if request[:4] == "GET ":
        response = getResponse(request)
    elif request[:4] == "POST":
        response = getResponse(request)
    else:
        return "HTTP/1.1 400 Bad Request"
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


def requestHandler(client, logger):
    """
    A thread used to parse and respond to a particular HTTP request.
    Params:
        client - a socket object representing the client.
    Return:
        None
    """
    try:
        response = parseRequest(client.recv(2048))
    except:
        logger.error("Could not parse request.")

    # try:
    #    body = getPhp("basic.php") + "\r\n\r\n"
    # except:
    #    logger.error("Could not process PHP script.")
    client.send(response)
    # Because HTTP is connectionless we close it at the end of every action
    client.close()


def main():
    """
    Basic web server implementing  GET, POST, PUT, DELETE, and CONNECT
    with the basic error reporting codes and a scripting language.
    Return:
        None
    """
    logger = logging.getLogger('webserver') # set up logger for easy logging.
    hdlr = logging.FileHandler('server.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    try:
        conf = getConfig(sys.argv[1])
    except IndexError:
        print("Defaulting to \"webserver.cfg\"")
        conf = getConfig("webserver.cfg")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((conf["host"], int(conf["port"])))  # Bind to port
    s.listen(10)  # concurrent connections possible

    try:
        while(True):
            # Client is an object representing the client
            # adr is an array of information about the client
            client, adr = s.accept()  # Accept is a blocking call
            logger.info("New connection from {0}:{1}".format(adr[0], adr[1]))

            # requestHandler is the function being run in the thread
            # args are the parameters it takes
            # You need the comma because it needs to be iterable
            threading.Thread(target=requestHandler, args=(client, logger)).start()

    except socket.error, exc:
        logger.error("Caught exception socket.error: {}".format(exc))


if __name__ == "__main__":
    main()
