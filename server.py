import socket
import threading

# Oppretter et socket-objekt og binder til den lokale hosten og porten
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 50000))

# Lytt etter klienter
server_socket.listen()

# Lagre klienter som en liste med par bestående av socket-objektet og adressen til klienten
clients = []

def broadcast(message, sender_client):
    """
    Sender en melding til alle tilkoblede klienter, unntatt senderen.

    """

    for client in clients:
        # Unngå å sende meldingen til senderen
        if client[0] != sender_client:
            client[0].send(message)

def handle_client(client_socket, client_address):
    """
    Funksjonen som håndterer kommunikasjon med klienten.

    """
    print(f'Ny tilkobling fra {client_address}')

    # Legger til klienten i listen med klienter
    clients.append((client_socket, client_address))

    # Sender en melding til alle klientene unntatt den nye klienten som blir med, om at en ny klient har blitt tilkoblet
    message = f'{client_address} har blitt med i chatten!\n'
    broadcast(message.encode(), client_socket)

    while True:
        try:
            # Motta meldingen fra klienten
            message = client_socket.recv(1024)
            # Send meldingen til alle klientene unntatt senderen
            broadcast(message, client_socket)
        except:
            # Hvis en feil oppstår, fjerner klienten fra listen over klienter
            # og sender en melding til de gjenværende klientene om at klienten har blitt frakoblet.
            print(f'{client_address} har blitt frakoblet')
            clients.remove((client_socket, client_address))
            message = f'{client_address} har blitt frakoblet fra chatten.\n'
            broadcast(message.encode(), client_socket)
            break

while True:
    # Aksepter nye klienter
    client_socket, client_address = server_socket.accept()

    # Opprett en ny thread for å håndtere klientens tilkobling
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

if __name__ == '__main__':
    start_server()