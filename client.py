import socket
import threading

def receive_messages(client_socket):
    """
    Funksjon for å motta meldinger fra serveren og skrive dem ut til terminalen.
    """

    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            # Hvis noe går galt med mottakelsen, antar vi at det er fordi serveren har lukket tilkoblingen.
            # Vi lukker klientsocketen og avslutter funksjonen.
            client_socket.close()
            break

def send_message(client_socket):
    """
    Funksjon for å la brukeren sende meldinger til alle andre tilkoblede klienter.
    """
    while True:
        message = input()
        client_socket.sendall(message.encode())

def connect_to_server():
    """
    Funksjon for å koble til serveren på gitt adresse og port.
    """
    # Definer serveradresse og portnummer
    SERVER_ADDRESS = 'localhost'
    SERVER_PORT = 50000

    # Opprett et socketobjekt og kobler til serveren
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    # Starter en separat thread for å motta meldinger fra serveren
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Lar brukeren skrive inn meldinger og sender dem til serveren
    send_message(client_socket)

if __name__ == '__main__':
    connect_to_server()
