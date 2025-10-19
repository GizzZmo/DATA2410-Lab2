# client.py
import json
import socket
import threading

from cryptography.fernet import Fernet


def receive_messages(client_socket, cipher):
    """
    Listen for and display messages received from the server.
    Runs in a separate thread.
    """
    try:
        while True:
            # Receive message length
            length_bytes = client_socket.recv(4)
            if not length_bytes:
                print("\n[CONNECTION] Server closed the connection.")
                break

            msg_length = int.from_bytes(length_bytes, "big")

            # Receive encrypted message
            encrypted_data = b""
            while len(encrypted_data) < msg_length:
                chunk = client_socket.recv(min(msg_length - len(encrypted_data), 4096))
                if not chunk:
                    break
                encrypted_data += chunk

            if len(encrypted_data) != msg_length:
                print("\n[ERROR] Incomplete message received")
                break

            # Decrypt and parse message
            try:
                message = cipher.decrypt(encrypted_data).decode("utf-8")
                data = json.loads(message)

                msg_type = data.get("type", "message")

                if msg_type == "welcome":
                    print(f"\n{'=' * 60}")
                    print(f"  {data['message']}")
                    print(f"  Current room: {data['room']}")
                    print(f"  Available rooms: {', '.join(data['rooms'])}")
                    print(f"{'=' * 60}")
                elif msg_type == "system":
                    print(f"\n[SYSTEM] {data['message']}")
                elif msg_type == "message":
                    username = data.get("username", "Unknown")
                    msg = data.get("message", "")
                    print(f"\n[{username}] {msg}")
                elif msg_type == "room_list":
                    print(f"\n[ROOMS] Available: {', '.join(data['rooms'])}")
                elif msg_type == "room_change":
                    print(f"\n[ROOM] {data['message']}")
                elif msg_type == "help":
                    print(f"\n[HELP] {data['message']}")
                else:
                    print(f"\n{message}")

            except json.JSONDecodeError:
                # Plain message (backward compatibility)
                print(f"\n{message}")
            except Exception as e:
                print(f"\n[ERROR] Failed to process message: {e}")

    except ConnectionResetError:
        print("\n[CONNECTION] Connection was reset by server.")
    except ConnectionAbortedError:
        print("\n[CONNECTION] Connection was aborted.")
    except Exception as e:
        print(f"\n[ERROR] Receive error: {e}")
    finally:
        print("\n[CLOSING] Closing receive thread.")


def start_client():
    """
    Start the chat client and connect to the server.
    """
    print("\n" + "=" * 60)
    print("  CYBERPUNK CHAT CLIENT")
    print("=" * 60 + "\n")

    SERVER_HOST = input("Enter server IP (e.g., localhost or 192.168.1.10): ").strip()
    if not SERVER_HOST:
        SERVER_HOST = "localhost"

    SERVER_PORT = 65432

    username = input("Enter your username: ").strip()
    if not username or len(username) < 2:
        username = f"User_{socket.gethostname()}"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"\n[CONNECTING] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Receive encryption key from server
        encryption_key = client_socket.recv(32)
        cipher = Fernet(encryption_key)
        print("[SECURITY] Encrypted connection established")

        # Send username
        encrypted_username = cipher.encrypt(username.encode("utf-8"))
        client_socket.sendall(len(encrypted_username).to_bytes(4, "big") + encrypted_username)

        print("[CONNECTED] Successfully connected to server!")
        print("\nCommands: /rooms, /join <room>, /help, /quit")
        print("=" * 60 + "\n")

        # Start receive thread
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, cipher), daemon=True)
        receive_thread.start()

        # Main message loop
        while True:
            try:
                message_to_send = input()

                if not message_to_send:
                    continue

                # Encrypt and send message
                encrypted_msg = cipher.encrypt(message_to_send.encode("utf-8"))
                msg_length = len(encrypted_msg)
                client_socket.sendall(msg_length.to_bytes(4, "big") + encrypted_msg)

                # Check for quit command
                if message_to_send.lower() in ["/quit", "/exit"]:
                    print("\n[DISCONNECTING] Closing connection...")
                    break

            except EOFError:
                print("\n[DISCONNECTING] Input closed")
                break

    except socket.error as e:
        print(f"\n[SOCKET ERROR] Could not connect to server: {e}")
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Client interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
    finally:
        try:
            client_socket.close()
        except Exception:
            pass
        print("[CLOSED] Client closed\n")


if __name__ == "__main__":
    start_client()
