# server.py
import json
import socket
import threading
import time
from typing import Dict, Set, Tuple

from cryptography.fernet import Fernet

# Global variables for managing clients and chatrooms
clients: Dict[str, Tuple[socket.socket, str, str]] = {}  # {client_id: (socket, username, room)}
chatrooms: Dict[str, Set[str]] = {"general": set()}  # {room_name: set(client_ids)}
client_lock = threading.Lock()
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not text:
        return ""
    # Remove potentially dangerous characters and limit length
    text = text.replace("\x00", "").replace("\r", "").replace("\n", " ")
    return text[:500]  # Limit message length


def broadcast_to_room(message: str, room: str, sender_id: str = None):
    """Send a message to all clients in a specific room."""
    with client_lock:
        if room not in chatrooms:
            return

        for client_id in chatrooms[room]:
            if client_id != sender_id and client_id in clients:
                try:
                    client_socket = clients[client_id][0]
                    encrypted_msg = cipher.encrypt(message.encode("utf-8"))
                    # Send length prefix followed by encrypted message
                    msg_length = len(encrypted_msg)
                    client_socket.sendall(msg_length.to_bytes(4, "big") + encrypted_msg)
                except Exception as e:
                    print(f"[ERROR] Failed to send to {client_id}: {e}")


def send_to_client(client_id: str, message: str):
    """Send a message to a specific client."""
    with client_lock:
        if client_id in clients:
            try:
                client_socket = clients[client_id][0]
                encrypted_msg = cipher.encrypt(message.encode("utf-8"))
                msg_length = len(encrypted_msg)
                client_socket.sendall(msg_length.to_bytes(4, "big") + encrypted_msg)
            except Exception as e:
                print(f"[ERROR] Failed to send to {client_id}: {e}")


def remove_client(client_id: str):
    """Remove a client from the server."""
    with client_lock:
        if client_id in clients:
            client_socket, username, room = clients[client_id]

            # Remove from chatroom
            if room in chatrooms:
                chatrooms[room].discard(client_id)

            # Remove from clients
            del clients[client_id]

            # Notify room
            broadcast_to_room(f"[SYSTEM] {username} has left the room", room)

            try:
                client_socket.close()
            except Exception:
                pass

            print(f"[DISCONNECT] {username} ({client_id}) left. Active clients: {len(clients)}")


def handle_client(client_socket: socket.socket, client_address: Tuple[str, int]):
    """Handle communication with a connected client."""
    client_id = f"{client_address[0]}:{client_address[1]}:{time.time()}"
    username = f"User_{client_address[1]}"
    current_room = "general"

    try:
        # Send encryption key to client
        client_socket.sendall(encryption_key)

        # Receive username
        try:
            username_length = int.from_bytes(client_socket.recv(4), "big")
            encrypted_username = client_socket.recv(username_length)
            username = sanitize_input(cipher.decrypt(encrypted_username).decode("utf-8"))

            if not username or len(username) < 2:
                username = f"User_{client_address[1]}"
        except Exception:
            username = f"User_{client_address[1]}"

        # Register client
        with client_lock:
            clients[client_id] = (client_socket, username, current_room)
            chatrooms[current_room].add(client_id)

        print(f"[CONNECT] {username} ({client_id}) joined {current_room}")

        # Send welcome message and room list
        welcome_msg = json.dumps(
            {
                "type": "welcome",
                "message": f"Welcome to the Cyberpunk Chat, {username}!",
                "room": current_room,
                "rooms": list(chatrooms.keys()),
            }
        )
        send_to_client(client_id, welcome_msg)

        # Notify room
        broadcast_to_room(
            json.dumps({"type": "system", "message": f"{username} has entered the room"}), current_room, client_id
        )

        # Main message loop
        while True:
            # Receive message length
            length_bytes = client_socket.recv(4)
            if not length_bytes:
                break

            msg_length = int.from_bytes(length_bytes, "big")
            if msg_length > 10000:  # Prevent memory attacks
                break

            # Receive encrypted message
            encrypted_data = b""
            while len(encrypted_data) < msg_length:
                chunk = client_socket.recv(min(msg_length - len(encrypted_data), 4096))
                if not chunk:
                    break
                encrypted_data += chunk

            if len(encrypted_data) != msg_length:
                break

            # Decrypt and process message
            try:
                message = cipher.decrypt(encrypted_data).decode("utf-8")
                message = sanitize_input(message)

                # Check for commands
                if message.startswith("/"):
                    parts = message.split(maxsplit=1)
                    command = parts[0].lower()

                    if command == "/quit" or command == "/exit":
                        break
                    elif command == "/rooms":
                        room_list = json.dumps({"type": "room_list", "rooms": list(chatrooms.keys())})
                        send_to_client(client_id, room_list)
                    elif command == "/join" and len(parts) > 1:
                        new_room = sanitize_input(parts[1])

                        # Leave current room
                        with client_lock:
                            if current_room in chatrooms:
                                chatrooms[current_room].discard(client_id)

                            # Join new room
                            if new_room not in chatrooms:
                                chatrooms[new_room] = set()
                            chatrooms[new_room].add(client_id)

                            # Update client info
                            clients[client_id] = (client_socket, username, new_room)
                            current_room = new_room

                        send_to_client(
                            client_id,
                            json.dumps(
                                {"type": "room_change", "room": new_room, "message": f"Joined room: {new_room}"}
                            ),
                        )

                        broadcast_to_room(
                            json.dumps({"type": "system", "message": f"{username} joined the room"}),
                            current_room,
                            client_id,
                        )
                    elif command == "/help":
                        help_msg = json.dumps(
                            {"type": "help", "message": "Commands: /rooms, /join <room>, /quit, /help"}
                        )
                        send_to_client(client_id, help_msg)
                else:
                    # Regular message - broadcast to room
                    msg_data = json.dumps(
                        {"type": "message", "username": username, "message": message, "timestamp": time.time()}
                    )
                    broadcast_to_room(msg_data, current_room, client_id)
                    print(f"[{current_room}] {username}: {message}")

            except Exception as e:
                print(f"[ERROR] Message processing error for {username}: {e}")
                break

    except Exception as e:
        print(f"[ERROR] Connection error with {client_address}: {e}")
    finally:
        remove_client(client_id)


def start_server():
    """Start the chat server and listen for incoming connections."""
    HOST = "0.0.0.0"
    PORT = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("[STARTING] Cyberpunk Chat Server initializing...")
    print("[KEY] Encryption enabled with Fernet")

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f"[LISTENING] Server active on {HOST}:{PORT}")
        print("[READY] Waiting for connections...")

        while True:
            client_socket, client_address = server_socket.accept()

            # Create and start client handler thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            client_thread.start()

            print(f"[ACTIVE] Connections: {len(clients)} | Rooms: {len(chatrooms)}")

    except socket.error as e:
        print(f"[SOCKET ERROR] {e}")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server shutting down...")
    finally:
        # Close all client connections
        with client_lock:
            for client_id in list(clients.keys()):
                try:
                    clients[client_id][0].close()
                except Exception:
                    pass

        server_socket.close()
        print("[STOPPED] Server stopped")


if __name__ == "__main__":
    start_server()
