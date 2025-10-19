# client_gui.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import json
from cryptography.fernet import Fernet


# Global variables
client_socket = None
cipher = None
username = "User"
current_room = "general"


class CyberpunkChat:
    """Cyberpunk-themed chat client with GUI."""

    # Cyberpunk color scheme
    COLORS = {
        "bg_dark": "#0a0e27",
        "bg_medium": "#1a1f3a",
        "bg_light": "#2a2f4a",
        "neon_cyan": "#00fff9",
        "neon_pink": "#ff006e",
        "neon_purple": "#8b00ff",
        "neon_green": "#39ff14",
        "text": "#e0e0e0",
        "text_dim": "#808080",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("CYBERPUNK CHAT")
        self.root.geometry("900x700")
        self.root.configure(bg=self.COLORS["bg_dark"])

        # Configure custom fonts
        try:
            self.font_title = ("Courier New", 16, "bold")
            self.font_normal = ("Consolas", 11)
            self.font_button = ("Courier New", 10, "bold")
        except Exception:
            self.font_title = ("TkDefaultFont", 16, "bold")
            self.font_normal = ("TkDefaultFont", 11)
            self.font_button = ("TkDefaultFont", 10, "bold")

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Create and layout all GUI widgets with cyberpunk styling."""

        # Title frame
        title_frame = tk.Frame(self.root, bg=self.COLORS["bg_dark"], height=60)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="╔══ CYBERPUNK CHAT ══╗",
            font=self.font_title,
            fg=self.COLORS["neon_cyan"],
            bg=self.COLORS["bg_dark"],
        )
        title_label.pack(pady=10)

        # Info frame (room and user info)
        info_frame = tk.Frame(self.root, bg=self.COLORS["bg_medium"], height=40)
        info_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        info_frame.pack_propagate(False)

        self.room_label = tk.Label(
            info_frame,
            text="ROOM: general",
            font=self.font_normal,
            fg=self.COLORS["neon_green"],
            bg=self.COLORS["bg_medium"],
        )
        self.room_label.pack(side=tk.LEFT, padx=10)

        self.user_label = tk.Label(
            info_frame,
            text=f"USER: {username}",
            font=self.font_normal,
            fg=self.COLORS["neon_pink"],
            bg=self.COLORS["bg_medium"],
        )
        self.user_label.pack(side=tk.RIGHT, padx=10)

        # Chat area frame
        chat_frame = tk.Frame(self.root, bg=self.COLORS["neon_cyan"], bd=2)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=self.font_normal,
            bg=self.COLORS["bg_light"],
            fg=self.COLORS["text"],
            insertbackground=self.COLORS["neon_cyan"],
            selectbackground=self.COLORS["neon_purple"],
            selectforeground=self.COLORS["text"],
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.configure(state="disabled")

        # Input frame
        input_frame = tk.Frame(self.root, bg=self.COLORS["bg_dark"])
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.message_entry = tk.Entry(
            input_frame,
            font=self.font_normal,
            bg=self.COLORS["bg_light"],
            fg=self.COLORS["text"],
            insertbackground=self.COLORS["neon_cyan"],
            relief=tk.FLAT,
            bd=0,
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=8)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame,
            text=">> SEND",
            command=self.send_message,
            font=self.font_button,
            bg=self.COLORS["neon_cyan"],
            fg=self.COLORS["bg_dark"],
            activebackground=self.COLORS["neon_green"],
            activeforeground=self.COLORS["bg_dark"],
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
        )
        self.send_button.pack(side=tk.RIGHT)

        # Button frame
        button_frame = tk.Frame(self.root, bg=self.COLORS["bg_dark"])
        button_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.rooms_button = tk.Button(
            button_frame,
            text="ROOMS",
            command=self.list_rooms,
            font=self.font_button,
            bg=self.COLORS["neon_purple"],
            fg=self.COLORS["text"],
            activebackground=self.COLORS["neon_pink"],
            activeforeground=self.COLORS["text"],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
        )
        self.rooms_button.pack(side=tk.LEFT, padx=2)

        self.join_button = tk.Button(
            button_frame,
            text="JOIN ROOM",
            command=self.join_room,
            font=self.font_button,
            bg=self.COLORS["neon_purple"],
            fg=self.COLORS["text"],
            activebackground=self.COLORS["neon_pink"],
            activeforeground=self.COLORS["text"],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
        )
        self.join_button.pack(side=tk.LEFT, padx=2)

        self.help_button = tk.Button(
            button_frame,
            text="HELP",
            command=self.show_help,
            font=self.font_button,
            bg=self.COLORS["neon_purple"],
            fg=self.COLORS["text"],
            activebackground=self.COLORS["neon_pink"],
            activeforeground=self.COLORS["text"],
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
        )
        self.help_button.pack(side=tk.LEFT, padx=2)

        # Initial message
        self.append_to_chat("╔═══════════════════════════════════════╗", self.COLORS["neon_cyan"])
        self.append_to_chat("║  WELCOME TO CYBERPUNK CHAT          ║", self.COLORS["neon_cyan"])
        self.append_to_chat("║  Connect to server to begin...      ║", self.COLORS["neon_cyan"])
        self.append_to_chat("╚═══════════════════════════════════════╝", self.COLORS["neon_cyan"])

    def append_to_chat(self, message, color=None):
        """Append a message to the chat area with optional color."""
        self.chat_area.configure(state="normal")

        if color:
            tag_name = f"color_{color}"
            self.chat_area.tag_config(tag_name, foreground=color)
            self.chat_area.insert(tk.END, message + "\n", tag_name)
        else:
            self.chat_area.insert(tk.END, message + "\n")

        self.chat_area.see(tk.END)
        self.chat_area.configure(state="disabled")

    def send_message(self, event=None):
        """Send a message to the server."""
        if not client_socket:
            messagebox.showerror("Error", "Not connected to server!")
            return

        message = self.message_entry.get().strip()
        if not message:
            return

        try:
            # Encrypt and send
            encrypted_msg = cipher.encrypt(message.encode("utf-8"))
            msg_length = len(encrypted_msg)
            client_socket.sendall(msg_length.to_bytes(4, "big") + encrypted_msg)

            # Clear entry
            self.message_entry.delete(0, tk.END)

            # Display own message
            if not message.startswith("/"):
                self.append_to_chat(f"[{username}] {message}", self.COLORS["neon_green"])

        except Exception as e:
            self.append_to_chat(f"[ERROR] Failed to send: {e}", self.COLORS["neon_pink"])

    def list_rooms(self):
        """Request list of available rooms."""
        if client_socket:
            try:
                msg = "/rooms"
                encrypted_msg = cipher.encrypt(msg.encode("utf-8"))
                client_socket.sendall(len(encrypted_msg).to_bytes(4, "big") + encrypted_msg)
            except Exception as e:
                self.append_to_chat(f"[ERROR] {e}", self.COLORS["neon_pink"])

    def join_room(self):
        """Join a different chat room."""
        room_name = simpledialog.askstring("Join Room", "Enter room name:", parent=self.root)
        if room_name and client_socket:
            try:
                msg = f"/join {room_name}"
                encrypted_msg = cipher.encrypt(msg.encode("utf-8"))
                client_socket.sendall(len(encrypted_msg).to_bytes(4, "big") + encrypted_msg)
            except Exception as e:
                self.append_to_chat(f"[ERROR] {e}", self.COLORS["neon_pink"])

    def show_help(self):
        """Display help information."""
        if client_socket:
            try:
                msg = "/help"
                encrypted_msg = cipher.encrypt(msg.encode("utf-8"))
                client_socket.sendall(len(encrypted_msg).to_bytes(4, "big") + encrypted_msg)
            except Exception as e:
                self.append_to_chat(f"[ERROR] {e}", self.COLORS["neon_pink"])

    def on_closing(self):
        """Handle window closing."""
        if client_socket:
            try:
                msg = "/quit"
                encrypted_msg = cipher.encrypt(msg.encode("utf-8"))
                client_socket.sendall(len(encrypted_msg).to_bytes(4, "big") + encrypted_msg)
                client_socket.close()
            except Exception:
                pass
        self.root.destroy()


def receive_messages(gui):
    """Receive messages from server and display in GUI."""
    global current_room

    try:
        while True:
            # Receive message length
            length_bytes = client_socket.recv(4)
            if not length_bytes:
                gui.append_to_chat("[DISCONNECTED] Server closed connection", gui.COLORS["neon_pink"])
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
                break

            # Decrypt and parse
            try:
                message = cipher.decrypt(encrypted_data).decode("utf-8")
                data = json.loads(message)

                msg_type = data.get("type", "message")

                if msg_type == "welcome":
                    gui.append_to_chat("═" * 60, gui.COLORS["neon_cyan"])
                    gui.append_to_chat(data["message"], gui.COLORS["neon_cyan"])
                    gui.append_to_chat(f"Room: {data['room']}", gui.COLORS["neon_green"])
                    gui.append_to_chat(f"Available: {', '.join(data['rooms'])}", gui.COLORS["text_dim"])
                    gui.append_to_chat("═" * 60, gui.COLORS["neon_cyan"])
                    current_room = data["room"]
                    gui.room_label.config(text=f"ROOM: {current_room}")

                elif msg_type == "system":
                    gui.append_to_chat(f"[SYSTEM] {data['message']}", gui.COLORS["neon_purple"])

                elif msg_type == "message":
                    user = data.get("username", "Unknown")
                    msg = data.get("message", "")
                    gui.append_to_chat(f"[{user}] {msg}", gui.COLORS["text"])

                elif msg_type == "room_list":
                    rooms = ", ".join(data["rooms"])
                    gui.append_to_chat(f"[ROOMS] {rooms}", gui.COLORS["neon_purple"])

                elif msg_type == "room_change":
                    current_room = data["room"]
                    gui.room_label.config(text=f"ROOM: {current_room}")
                    gui.append_to_chat(f"[ROOM] {data['message']}", gui.COLORS["neon_green"])

                elif msg_type == "help":
                    gui.append_to_chat(f"[HELP] {data['message']}", gui.COLORS["neon_cyan"])

            except json.JSONDecodeError:
                gui.append_to_chat(message, gui.COLORS["text"])
            except Exception as e:
                gui.append_to_chat(f"[ERROR] {e}", gui.COLORS["neon_pink"])

    except Exception as e:
        if gui.root.winfo_exists():
            gui.append_to_chat(f"[ERROR] Connection error: {e}", gui.COLORS["neon_pink"])


def start_client_gui(gui):
    """Connect to the chat server."""
    global client_socket, cipher, username

    # Get server details
    server_host = simpledialog.askstring("Server Connection", "Enter server IP (default: localhost):", parent=gui.root)
    if not server_host:
        server_host = "localhost"

    user_input = simpledialog.askstring("Username", "Enter your username:", parent=gui.root)
    if user_input:
        username = user_input

    SERVER_PORT = 65432

    try:
        gui.append_to_chat(f"[CONNECTING] Connecting to {server_host}:{SERVER_PORT}...", gui.COLORS["neon_cyan"])

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, SERVER_PORT))

        # Receive encryption key
        encryption_key = client_socket.recv(32)
        cipher = Fernet(encryption_key)
        gui.append_to_chat("[SECURITY] Encrypted connection established", gui.COLORS["neon_green"])

        # Send username
        encrypted_username = cipher.encrypt(username.encode("utf-8"))
        client_socket.sendall(len(encrypted_username).to_bytes(4, "big") + encrypted_username)

        # Update GUI
        gui.user_label.config(text=f"USER: {username}")
        gui.append_to_chat("[CONNECTED] Successfully connected!", gui.COLORS["neon_green"])

        # Start receive thread
        receive_thread = threading.Thread(target=receive_messages, args=(gui,), daemon=True)
        receive_thread.start()

    except Exception as e:
        gui.append_to_chat(f"[ERROR] Connection failed: {e}", gui.COLORS["neon_pink"])
        messagebox.showerror("Connection Error", f"Failed to connect: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = CyberpunkChat(root)

    # Auto-connect on startup
    root.after(500, lambda: start_client_gui(gui))

    root.mainloop()
