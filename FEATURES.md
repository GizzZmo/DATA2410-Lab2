# Cyberpunk Chat Application - Feature Updates

## 🎨 New Features

### 1. Cyberpunk Aesthetics (client_gui.py)
- **Neon color scheme**: Cyan (#00fff9), Pink (#ff006e), Purple (#8b00ff), Green (#39ff14)
- **Custom fonts**: Courier New and Consolas for that authentic terminal feel
- **Glowing borders**: All UI elements feature neon-style glowing effects
- **ASCII art decorations**: Box-drawing characters for authentic cyberpunk style
- **Dark theme**: Deep space colors (#0a0e27, #1a1f3a, #2a2f4a)

### 2. Multi-Client Support (server.py)
- Server now supports **unlimited concurrent connections** (previously limited to 1)
- Each client gets a **unique ID** based on IP, port, and timestamp
- **Thread-safe client management** using locks
- **Broadcast messaging** to all clients in a room
- Automatic cleanup when clients disconnect

### 3. Chatroom Functionality
- **Multiple chatrooms**: Users can create and join different rooms
- **Default room**: "general" room created automatically
- **Room commands**:
  - `/rooms` - List all available rooms
  - `/join <room>` - Join or create a room
  - `/help` - Display available commands
  - `/quit` or `/exit` - Disconnect from server
- **Room notifications**: Users are notified when others join/leave

### 4. Security Enhancements
- **End-to-end encryption**: All messages encrypted using Fernet (AES-128)
- **Key exchange**: Server generates and shares encryption key with clients
- **Input sanitization**: Prevents injection attacks
  - Removes null bytes, control characters
  - Limits message length to 500 characters
  - Sanitizes usernames and room names
- **Message validation**: Checks message length to prevent memory attacks

### 5. Performance Improvements
- **Message framing**: Length-prefixed messages for reliable boundaries
- **Chunked reading**: Handles large messages efficiently
- **Non-blocking I/O**: Better responsiveness
- **Error handling**: Graceful disconnection and reconnection
- **Resource cleanup**: Proper socket and thread management

## 🔧 Technical Details

### Architecture
```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Client    │◄───────►│   Server    │◄───────►│   Client    │
│  (GUI/CLI)  │ Encrypt │             │ Encrypt │  (GUI/CLI)  │
│             │ Messages│ Broadcast   │ Messages│             │
└─────────────┘         └─────────────┘         └─────────────┘
       │                       │                        │
       └───────────────────────┴────────────────────────┘
              Encrypted Channel (Fernet/AES)
```

### Message Protocol
- **Format**: `[4-byte length][encrypted JSON payload]`
- **JSON Structure**:
  ```json
  {
    "type": "message|system|welcome|room_change|help",
    "username": "string",
    "message": "string",
    "room": "string",
    "timestamp": 1234567890.123
  }
  ```

### Dependencies
- `cryptography` - For Fernet encryption (AES-128 CBC mode)
- `tkinter` - For GUI (built-in with Python)

## 📋 Commands

### Client Commands
- `/rooms` - List all available chatrooms
- `/join <room>` - Join or create a chatroom
- `/help` - Show available commands
- `/quit` or `/exit` - Disconnect from server

### Usage Examples

**Command Line Client:**
```bash
python3 client.py
# Enter server IP: localhost
# Enter username: CyberNinja
# Type messages or commands
```

**GUI Client:**
```bash
python3 client_gui.py
# Dialog prompts for server IP and username
# Click buttons or type commands
```

**Server:**
```bash
python3 server.py
# Server starts on 0.0.0.0:65432
# Displays connection status and messages
```

## 🔒 Security Features

1. **Encryption**: All messages encrypted with Fernet (symmetric encryption)
2. **Input Validation**: Prevents code injection and buffer overflow
3. **Authentication**: Username-based identification
4. **Safe Defaults**: Secure configuration out of the box

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Tests cover:
- Module imports
- Function existence
- Input sanitization
- Encryption functionality
- Chatroom initialization
- Socket creation

## 📝 Code Quality

All code passes:
- ✅ flake8 (syntax and style checks)
- ✅ black (code formatting)
- ✅ isort (import sorting)
- ✅ bandit (security scanning)
- ✅ pytest (unit tests)

## 🎯 Future Enhancements

Potential improvements:
- File transfer support
- User authentication with passwords
- Message history persistence
- Voice/video chat integration
- Custom themes and colors
- Rate limiting and spam protection
- Admin commands and moderation tools
