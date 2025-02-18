# 🌲 TreeDrive - File Sharing Server

TreeDrive is a **stateful file-sharing server and client system** that enables multiple users to authenticate, upload, download, list, and delete files in a shared environment. The server maintains file and user metadata to ensure proper ownership and access control.

---

## 🚀 Features

- **🔒 Stateful File-Sharing Server**: File data and metadata persist between restarts.
- **🔑 Client Authentication**: Users must log in before performing file operations.
- **📂 File Operations**:
  - `PUSH <filename>` - Upload a file to the server (associated with the logged-in user).
  - `LIST` - List all files on the server, including metadata (owner, size, timestamp).
  - `GET <filename>` - Download a specified file.
  - `DELETE <filename>` - Remove a file (only the owner can delete their files).
- **⚡ Custom Protocol**: TreeDrive does not use HTTP and operates over a TCP connection.
- **👥 Multi-Client Support**: The server handles multiple clients concurrently using `select` (without multi-threading).
- **🗂️ Filesystem Navigation**:
  - Clients can navigate the local file system using `cd` and `ls` commands.
  - Allows users to upload (`PUSH`) and download (`GET`) files from different directories.

---

## 📥 Installation & Usage

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/Shivv10/File-Sharing-Server.git
cd File-Sharing-Server
```

### 2️⃣ Start the Server
Run the following command to start the TreeDrive server:
```sh
python3 server.py
```
By default, the server runs on `localhost` and a predefined port. To specify a different host and port, modify `server.py` accordingly.

### 3️⃣ Start a Client
Run the following command to connect as a client:
```sh
python3 client.py <username> <server_host> <server_port>
```
Example:
```sh
python3 client.py alice 127.0.0.1 8080
```

### 4️⃣ Available Client Commands
Once connected, you can use the following commands:

| Command              | Description                                  |
|----------------------|----------------------------------------------|
| `PUSH <filename>`   | Uploads a file to the server.                |
| `LIST`              | Lists all files with metadata.               |
| `GET <filename>`    | Downloads a file from the server.            |
| `DELETE <filename>` | Deletes a file (only if you are the owner).  |
| `cd <directory>`    | Change local directory.                      |
| `ls`                | List files in the current local directory.   |

---

## ⚙️ Server Configuration
- The server currently runs on `localhost` by default.
- To use a specific host and port, modify `server.py` accordingly.

---

## 📌 Notes
- The server and client communicate using a **TCP connection**.
- Clients **must authenticate** before using file-sharing features.
- **Metadata ensures** that only the file owner can delete their files.

---

## 📜 License
This project is open-source and available under the **MIT License**.

📌 *Feel free to contribute, report issues, or suggest improvements!* ✨
