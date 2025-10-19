# Quick Start Guide - Cyberpunk Chat

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GizzZmo/DATA2410-Lab2.git
   cd DATA2410-Lab2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Running the Application

### Option 1: GUI Client (Recommended)

1. **Start the server** (in terminal 1):
   ```bash
   python3 server.py
   ```
   
   You should see:
   ```
   [STARTING] Cyberpunk Chat Server initializing...
   [KEY] Encryption enabled with Fernet
   [LISTENING] Server active on 0.0.0.0:65432
   [READY] Waiting for connections...
   ```

2. **Start the GUI client** (in terminal 2):
   ```bash
   python3 client_gui.py
   ```
   
   - Enter server IP (use `localhost` for local testing)
   - Enter your username
   - Start chatting!

3. **Start more clients** (optional):
   - Open additional terminals
   - Run `python3 client_gui.py` in each
   - Each client can join different rooms or chat together

### Option 2: Command-Line Client

1. **Start the server** (in terminal 1):
   ```bash
   python3 server.py
   ```

2. **Start the CLI client** (in terminal 2):
   ```bash
   python3 client.py
   ```
   
   Follow the prompts to enter:
   - Server IP address (e.g., `localhost`)
   - Your username

3. **Type messages or commands:**
   ```
   Hello everyone!
   /rooms
   /join tech-talk
   /help
   /quit
   ```

## 🎮 Using the Chat

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/rooms` | List all available chatrooms | `/rooms` |
| `/join <room>` | Join or create a chatroom | `/join tech-talk` |
| `/help` | Show available commands | `/help` |
| `/quit` | Disconnect from server | `/quit` |

### GUI Features

- **ROOMS button**: Click to see all available rooms
- **JOIN ROOM button**: Click to join a different room
- **HELP button**: Click to see available commands
- **>> SEND button**: Send your message (or press Enter)

### Tips

1. **Creating rooms**: Just `/join <new-room-name>` to create a new room
2. **Private conversations**: Create a unique room name and share it
3. **Multiple rooms**: Switch between rooms without reconnecting
4. **User identification**: Messages show who sent them
5. **System notifications**: Stay informed about joins/leaves

## 🔧 Troubleshooting

### Connection Issues

**Problem**: "Could not connect to server"
- **Solution**: Make sure the server is running first
- **Solution**: Check if using correct IP (localhost for same machine)
- **Solution**: Ensure port 65432 is not blocked by firewall

**Problem**: "Module 'tkinter' not found"
- **Solution** (Ubuntu/Debian): `sudo apt-get install python3-tk`
- **Solution** (macOS): tkinter comes with Python
- **Solution** (Windows): Reinstall Python with tkinter option

**Problem**: "No module named 'cryptography'"
- **Solution**: `pip install -r requirements.txt`
- **Solution**: `pip install cryptography`

### Server Issues

**Problem**: "Address already in use"
- **Solution**: Kill the existing server process
- **Solution** (Linux/Mac): `pkill -f server.py`
- **Solution** (Windows): Find and kill python.exe in Task Manager

## 🎨 Customization

### Changing Server Port

Edit `server.py` line 218:
```python
PORT = 65432  # Change to your preferred port
```

Also update in `client.py` line 90 and `client_gui.py` line 371.

### Changing Colors (GUI)

Edit `client_gui.py` COLORS dictionary (lines 21-30):
```python
COLORS = {
    'bg_dark': '#0a0e27',      # Background
    'neon_cyan': '#00fff9',    # Primary accent
    'neon_pink': '#ff006e',    # Secondary accent
    # ... customize other colors
}
```

## 📊 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

## 🔒 Security Notes

- All messages are encrypted using Fernet (AES-128)
- Server binds to 0.0.0.0 (all interfaces) by default
- For production: Configure firewall rules appropriately
- For private use: Change HOST to '127.0.0.1' in server.py

## 📚 More Information

- **Features**: See [FEATURES.md](FEATURES.md) for detailed feature documentation
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- **Workflows**: See [GITHUB_WORKFLOWS.md](GITHUB_WORKFLOWS.md) for CI/CD information

## 🆘 Getting Help

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review the error message carefully
3. Check server logs for connection errors
4. Ensure all dependencies are installed
5. Open an issue on GitHub with details

## 🎯 Next Steps

After getting familiar with the basics:
- Try creating multiple chatrooms
- Connect multiple clients
- Experiment with different usernames
- Explore the cyberpunk-themed GUI
- Check out the source code to learn how it works

Enjoy chatting in the cyberpunk underground! 🌃✨
