

import socket
import os
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1234
CHUNK_SIZE = 1024  # Size of each chunk for file transfer

def login(sock, username):
    """Send the LOGIN command with the username."""
    sock.send(f"LOGIN {username}".encode())
    response = sock.recv(1024)
    print(response.decode())

def send_command(sock, command):
    """Send a command to the server and print the response."""
    sock.send(command.encode())
    response = sock.recv(1024)
    print(response.decode())

def upload_file(sock, filename):
    """Upload a file to the server in chunks."""
    print(f"Uploading file: {filename}")

    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    try:

        # Get file size
        file_size = os.path.getsize(filename)

        # Send the UPLOAD command with the filename
        sock.send(f"PUSH {filename}".encode())
        print(sock.recv(1024))  # Receive the server's response

        # Send file size first
        sock.send(str(file_size).encode())

        done = False
        # Read and send the file in chunks
        with open(filename, "rb") as f:
            while not done:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    done = True
                else:
                    sock.send(chunk)

        # Receive the server's response
        print(sock.recv(1024).decode())
    except Exception as e:
        print(f"Error uploading file: {e}")

def download_file(sock, filename):
    """Download a file from the server in chunks."""
    try:
        # Send the DOWNLOAD command with the filename
        sock.sendall(f"GET {filename}".encode())

        # Receive the file size first
        file_size = int(sock.recv(1024).decode())
        received_size = 0
        sock.sendall(b"Ready to receive")

        with open(filename, "wb") as f:
            while received_size < file_size:
                chunk = sock.recv(min(CHUNK_SIZE, file_size - received_size))
                f.write(chunk)
                received_size += len(chunk)

        print(f"File {filename} downloaded.")
    except Exception as e:
        print(f"Error downloading file: {e}")

def change_directory(path):
    """Change the current working directory."""
    try:
        os.chdir(path)
        print(f"Changed directory to: {os.getcwd()}")
    except FileNotFoundError:
        print(f"Directory not found: {path}")
    except NotADirectoryError:
        print(f"Not a directory: {path}")
    except Exception as e:
        print(f"Error changing directory: {e}")

def list_directory():
    """List the contents of the current directory."""
    try:
        contents = os.listdir()
        print(f"Contents of {os.getcwd()}:")
        for item in contents:
            print(f"  {item}")
    except Exception as e:
        print(f"Error listing directory contents: {e}")

def main():
    """Main function to handle client interactions."""

    username = sys.argv[1]  # Get the username from command-line arguments
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Login automatically
    login(client_socket, username)

    print("Available commands: PUSH <file>, GET <file>, LIST, DELETE <file>, ls, cd <path>, QUIT")

    while True:
        command = input("Enter command: ").strip()
        if command.upper() == "QUIT":
            print("Exiting TreeDrive ...")
            break
        elif command.upper() == "LS":
            list_directory()
        elif command.upper().startswith("CD"):
            _, path = command.split(maxsplit=1)
            change_directory(path)
        elif command.upper().startswith("PUSH"):
            _, filename = command.split(maxsplit=1)
            upload_file(client_socket, filename)
        elif command.upper().startswith("GET"):
            _, filename = command.split(maxsplit=1)
            download_file(client_socket, filename)
        elif command.upper() == "LIST":
            send_command(client_socket, "LIST")
        else:
            send_command(client_socket, command.upper())

    client_socket.close()

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 4:
        print("Usage: python client.py <username> <server_host> <server_port>")
        sys.exit(1)
    elif len(args) == 4:
        USERNAME = args[1]
        SERVER_HOST = args[2]
        SERVER_PORT = int(args[3])
    main()