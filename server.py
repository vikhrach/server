import logging
import socket
import sys
import threading

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

HOST = "localhost"
PORT = 8080
DOCUMENT_ROOT = "./www"


def handle_request(client_socket):
    try:
        # 1. get request
        request_data = client_socket.recv(4096).decode("utf-8")
        # 2. get hedares
        # Split the request into the request line, headers, and body
        request_lines = request_data.split("\r\n")
        request_line = request_lines[0]  # First line is the request line

        # Extract the request method, path, and HTTP version from the request line
        request_method, path, http_version = request_line.split(" ", 2)
        logger.info(f"\nRequest Method: {request_line}")
        logger.info(f"Path: {path}")
        logger.info(f"HTTP Version: {http_version}")
        # 3. split headers to methoods
        # 4. give back response
        if request_method in ["GET", "HEAD"]:
            # Prepare a simple HTTP response
            response_body = f"Hello, client! You used the {request_method} method."
            response_headers = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "Connection: close\r\n\r\n"
            )
        response = response_headers + response_body
        client_socket.send(response.encode("utf-8"))
    except ValueError as e:
        logger.exception(f"ValueError {e}")
    except socket.error as e:
        logger.exception(f"Socket error {e}")
    finally:
        client_socket.close()


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    server_socket.listen(5)
    logging.info("Server started")

    # 3. in while loop create threads with fucntion for handle_request
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
