# DATA2410 Lab 2 - Chat Application

## 📚 Documentation

- [GitHub Workflows Documentation](GITHUB_WORKFLOWS.md) - Comprehensive guide to GitHub Actions and CI/CD workflows
- [Chat Application Guide](#chat-application) - How to use the chat application

---

## GitHub Actions & Workflows

This repository uses GitHub Actions for automation and continuous integration. For detailed information about:
- Setting up and configuring workflows
- Understanding the Copilot workflow system
- Common workflow patterns and examples
- Troubleshooting guide

**➡️ See the [GitHub Workflows Documentation](GITHUB_WORKFLOWS.md)**

---

## Chat Application

Jeg kan lage et enkelt eksempel på en tekstbasert chat-applikasjon i Python som lar to personer kommunisere med hverandre over et nettverk. Dette vil bestå av to separate skript: ett for serveren og ett for klienten.

Her er koden for server- og klientapplikasjonen:
Python Chat Server
9. mai, 14:58

Åpne
Python Chat Klient
9. mai, 14:58

Hvordan bruke applikasjonen:

Lagre kodene:

Lagre den første koden som server.py.
Lagre den andre koden som client.py.
Kjør serveren:

Åpne en terminal eller kommandolinje.
Naviger til mappen der du lagret server.py.
Kjør kommandoen: python server.py
Serveren vil starte og lytte etter tilkoblinger. Du vil se noe som: [LYTTER] Serveren lytter på 0.0.0.0:65432 (eller en spesifikk IP hvis du endret den).
Kjør klienten (for første person):

Åpne en ny terminal eller kommandolinje.
Naviger til mappen der du lagret client.py.
Kjør kommandoen: python client.py
Klienten vil spørre om serverens IP-adresse.
Hvis serveren kjører på samme maskin, skriv localhost.
Hvis serveren kjører på en annen maskin i samme nettverk, skriv IP-adressen til den maskinen (f.eks. 192.168.1.10). Du kan finne IP-adressen til servermaskinen ved å bruke kommandoer som ipconfig (Windows) eller ifconfig / ip addr (Linux/macOS).
Når klienten er koblet til, kan du begynne å skrive meldinger.
Kjør en annen klient (for andre person):

For at to personer skal kunne "prate", må serveren modifiseres til å håndtere to klienter og videresende meldinger mellom dem. Det nåværende servereksemplet er primært for en klient-server-interaksjon hvor serveren ser meldingene.

For en ekte to-personers chat: Serverkoden (server.py) må utvides betydelig. Den må:

Holde styr på to tilkoblede klienter.
Når en melding mottas fra Klient A, må den videresendes til Klient B, og vice versa.
Håndtere tilfeller der en av klientene kobler fra.
Med den nåværende enkle serveren: Du kan kjøre en andre klient på samme måte som den første. Begge klientene vil koble seg til serveren, og serverterminalen vil se meldinger fra begge. Men klientene vil ikke se hverandres meldinger direkte gjennom denne enkle serveren. Serveroperatøren kan manuelt videresende informasjon ved å skrive i serverterminalen (hvis send_messages-funksjonen i serveren er aktivert og modifisert for å velge hvilken klient den skal sende til).

Viktige merknader:

Nettverk: For at klienter på forskjellige maskiner skal kunne koble seg til, må de være på samme nettverk, og eventuelle brannmurer må konfigureres til å tillate trafikk på port 65432 (eller den porten du velger). Hvis du vil koble til over internett, trenger du portvideresending på ruteren din og serverens offentlige IP-adresse.
Enkelhet: Dette er en veldig grunnleggende implementasjon. En robust chat-applikasjon ville hatt mange flere funksjoner, som feilhåndtering, brukerautentisering, kryptering, støtte for flere brukere i et chatterom, osv.
Modifikasjon for to-veis chat mellom to klienter: Den medfølgende server.py er satt opp for å håndtere en klient om gangen i handle_client-funksjonen. For å lage en direkte to-personers chat, må server.py endres til å:
Akseptere to klienttilkoblinger.
Når en melding mottas fra klient 1, send den til klient 2.
Når en melding mottas fra klient 2, send den til klient 1. Dette krever mer kompleks logikk for å administrere klient-socketene.
Sikkerhet: Denne koden inkluderer ingen sikkerhetstiltak. Meldinger sendes som ren tekst. Ikke bruk dette for sensitiv kommunikasjon uten å legge til kryptering (f.eks. SSL/TLS).
Dette gir deg et utgangspunkt. Å bygge en fullverdig "telefonapp" (med lyd osv.) er et mye mer komplekst prosjekt som vanligvis involverer andre teknologier og biblioteker utover grunnleggende Python-sockets.

mports and Setup
# server_two_clients.py
import socket
import threading

# Liste for å holde styr på tilkoblede klienter (maks 2 for denne versjonen)
clients = []
client_lock = threading.Lock() # For trådsikker tilgang til klientlisten
Use code with caution
It starts by importing the necessary modules:
socket: This module provides functions for network communication, allowing the server to create and manage sockets.
threading: This module enables the server to handle multiple clients concurrently using threads.
clients: This is a list that will store the connected clients. Each element in the list is a tuple containing the client's socket and address.
client_lock: This is a threading lock used to synchronize access to the clients list, preventing race conditions when multiple threads try to modify it simultaneously.
Broadcasting Messages
def broadcast_message(message, sender_socket=None):
    """
    Sender en melding til alle tilkoblede klienter, unntatt avsenderen hvis spesifisert.
    """
    with client_lock:
        for client_sock, _ in clients:
            if client_sock != sender_socket:
                try:
                    client_sock.send(message.encode('utf-8'))
                except socket.error:
                    # Håndter feil ved sending, f.eks. klient har koblet fra uventet
                    remove_client(client_sock)
Use code with caution
The broadcast_message function sends a message to all connected clients except for the sender (if specified).
It acquires the client_lock to ensure thread safety when accessing the clients list.
It iterates through the connected clients and sends the message to each client socket that is not the sender's socket.
If there is a socket error during sending, it calls the remove_client function to handle the disconnection.
Removing a Client
def remove_client(client_socket_to_remove):
    """
    Fjerner en klient fra listen over tilkoblede klienter.
    """
    with client_lock:
        client_to_remove_tuple = None
        for client_tuple in clients:
            if client_tuple[0] == client_socket_to_remove:
                client_to_remove_tuple = client_tuple
                break
        if client_to_remove_tuple:
            clients.remove(client_to_remove_tuple)
            print(f"[{client_to_remove_tuple[1]}] Koblet fra. Antall klienter: {len(clients)}")
            broadcast_message(f"System: Bruker {client_to_remove_tuple[1][0]}:{client_to_remove_tuple[1][1]} har forlatt chatten.", None)
            try:
                client_socket_to_remove.close()
            except socket.error:
                pass # Socket kan allerede være lukket
Use code with caution
The remove_client function removes a client from the clients list.
It acquires the client_lock for thread safety.
It searches for the client's socket in the clients list.
If found, it removes the client from the list, prints a disconnection message, broadcasts a message to other clients informing them of the disconnection, and closes the client's socket.
Handling a Client
def handle_client(client_socket, client_address):
    """
    Håndterer kommunikasjonen med en enkelt tilkoblet klient.
    Mottar meldinger fra klienten og kringkaster dem til den andre klienten.
    """
    print(f"[NY TILKOBLING] {client_address} koblet til.")
    
    # Informer andre klienter (hvis noen) om ny tilkobling
    # Dette kan gjøres mer elegant med brukernavn senere
    broadcast_message(f"System: Bruker {client_address[0]}:{client_address[1]} har koblet seg til.", client_socket)

    connected = True
    try:
        while connected:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"[{client_address}] Koblet fra (tom melding).")
                connected = False
                break # Gå til finally-blokken for å fjerne klienten

            # Sjekk for 'avslutt'-kommando fra klienten (som sendes av client_gui.py)
            # Meldingen vil være formatert som "brukernavn: avslutt"
            if ": avslutt" in message.lower(): # Enkel sjekk
                print(f"[{client_address}] Ba om å avslutte via melding: {message}")
                connected = False
                # Ikke send "avslutt"-meldingen videre, klienten håndterer sin egen frakobling
                break


            print(f"Mottatt fra [{client_address}]: {message}")
            
            # Videresend meldingen til den andre klienten
            broadcast_message(message, client_socket)

    except ConnectionResetError:
        print(f"[{client_address}] Tilkoblingen ble tilbakestilt av klienten.")
    except socket.timeout:
        print(f"[{client_address}] Socket timeout.") # Kan skje hvis klienten ikke sender noe på lenge
    except Exception as e:
        print(f"[FEIL] En feil oppstod med {client_address}: {e}")
    finally:
        remove_client(client_socket)
Use code with caution
The handle_client function manages the communication with a single client.
It prints a message indicating the new connection.
It broadcasts a message to other clients informing them of the new connection.
It enters a loop to continuously receive and broadcast messages from the client.
If the client disconnects or sends an "avslutt" command, it breaks the loop.
It handles exceptions such as ConnectionResetError and socket.timeout.
In the finally block, it calls remove_client to remove the client from the server.
Starting the Server
def start_server():
    """
    Starter chat-serveren, lytter etter innkommende tilkoblinger for opptil to klienter.
    """
    HOST = '0.0.0.0'  # Lytt på alle tilgjengelige grensesnitt
    PORT = 65432      # Portnummer (bruk en port > 1023)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(1.0) # For å kunne sjekke KeyboardInterrupt jevnlig
    print("[STARTER] Serveren starter...")

    try:
        server_socket.bind((HOST, PORT))
        print(f"[LYTTER] Serveren lytter på {HOST}:{PORT}")
        server_socket.listen(2) # Tillat opptil 2 ventende tilkoblinger

        while True: # Hovedløkke for å akseptere nye tilkoblinger
            try:
                if len(clients) < 2: # Tillat kun to klienter
                    client_socket, client_address = server_socket.accept()
                    client_socket.settimeout(60.0) # Sett timeout for klient-socket

                    with client_lock:
                        clients.append((client_socket, client_address))
                    
                    print(f"[AKSEPTERT] Ny tilkobling fra {client_address}. Antall klienter: {len(clients)}")

                    client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
                    client_handler_thread.start()
                else:
                    # Serveren er full, vent litt før ny sjekk
                    # Alternativt, avvis tilkoblingen aktivt
                    try:
                        # For å unngå travel venting, kan vi akseptere og så lukke hvis full
                        conn_full, addr_full = server_socket.accept()
                        print(f"[AVVIST] Server full. Avviste tilkobling fra {addr_full}")
                        conn_full.send("Server: Beklager, chatrommet er fullt.\n".encode('utf-8'))
                        conn_full.close()
                    except socket.timeout:
                        pass # Ingen nye tilkoblingsforsøk, fortsett løkken
                    except socket.error:
                        pass # Annen socketfeil, fortsett løkken

            except socket.timeout:
                continue # Gå tilbake til starten av while-løkken for å sjekke for KeyboardInterrupt
            except socket.error as e:
                print(f"[SERVER SOCKET FEIL] {e}")
                break # Avslutt serveren ved alvorlig socketfeil

    except KeyboardInterrupt:
        print("\n[AVSLUTTER] Serveren avsluttes manuelt.")
    except Exception as e:
        print(f"[SERVER HOVEDFEIL] {e}")
    finally:
        print("Lukker alle klienttilkoblinger...")
        with client_lock:
            for client_sock, client_addr in clients:
                try:
                    client_sock.send("Server: Serveren avsluttes.\n".encode('utf-8'))
                    client_sock.close()
                except socket.error:
                    pass # Klienten kan allerede være frakoblet
            clients.clear()
        print("Lukker server socket.")
        server_socket.close()

if __name__ == "__main__":
    start_server()
Use code with caution
The start_server function initializes and starts the chat server.
It creates a server socket and binds it to a specific host and port.
It listens for incoming connections and accepts them.
For each accepted connection, it creates a new thread using threading.Thread to handle the client communication.
It handles exceptions and gracefully shuts down the server when a KeyboardInterrupt is received or a major error occurs.
The if __name__ == "__main__": block ensures that the start_server function is called only when the script is executed directly, not when it's imported as a module.
