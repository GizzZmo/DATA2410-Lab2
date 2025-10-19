"""
Test suite for the cyberpunk chat application.
"""

import socket
import threading
import time
import unittest


class TestChatApplication(unittest.TestCase):
    """Test cases for the chat application."""

    def test_imports(self):
        """Test that all modules can be imported successfully."""
        try:
            import client
            import server

            self.assertIsNotNone(server)
            self.assertIsNotNone(client)

            # Try importing client_gui, but skip if tkinter not available
            try:
                import client_gui

                self.assertIsNotNone(client_gui)
            except ImportError as e:
                if "tkinter" in str(e).lower():
                    self.skipTest("tkinter not available in headless environment")
                else:
                    raise
        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")

    def test_server_functions_exist(self):
        """Test that server module has required functions."""
        import server

        self.assertTrue(hasattr(server, "start_server"))
        self.assertTrue(hasattr(server, "handle_client"))
        self.assertTrue(hasattr(server, "broadcast_to_room"))
        self.assertTrue(hasattr(server, "sanitize_input"))

    def test_client_functions_exist(self):
        """Test that client module has required functions."""
        import client

        self.assertTrue(hasattr(client, "start_client"))
        self.assertTrue(hasattr(client, "receive_messages"))

    def test_sanitize_input(self):
        """Test input sanitization function."""
        from server import sanitize_input

        # Test normal input
        self.assertEqual(sanitize_input("hello world"), "hello world")

        # Test input with newlines
        self.assertEqual(sanitize_input("hello\nworld"), "hello world")

        # Test input with null bytes
        self.assertEqual(sanitize_input("hello\x00world"), "helloworld")

        # Test empty input
        self.assertEqual(sanitize_input(""), "")

        # Test None input
        self.assertEqual(sanitize_input(None), "")

        # Test long input (should truncate to 500 chars)
        long_input = "a" * 1000
        result = sanitize_input(long_input)
        self.assertEqual(len(result), 500)

    def test_encryption_key_generation(self):
        """Test that server generates encryption keys properly."""
        from cryptography.fernet import Fernet

        from server import cipher, encryption_key

        # Verify key exists
        self.assertIsNotNone(encryption_key)
        self.assertEqual(len(encryption_key), 44)  # Fernet keys are 44 bytes in base64

        # Verify cipher works
        test_message = b"test message"
        encrypted = cipher.encrypt(test_message)
        decrypted = cipher.decrypt(encrypted)
        self.assertEqual(decrypted, test_message)

    def test_chatroom_initialization(self):
        """Test that chatrooms are initialized correctly."""
        from server import chatrooms

        # Verify default room exists
        self.assertIn("general", chatrooms)
        self.assertIsInstance(chatrooms["general"], set)

    def test_client_socket_creation(self):
        """Test basic socket creation for client."""
        # Test that we can create a socket
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertIsNotNone(test_socket)
        test_socket.close()


if __name__ == "__main__":
    unittest.main()
