# client.py
import socket
import threading

# Funksjon for å motta meldinger fra serveren
def receive_messages(client_socket):
    """
    Lytter etter og skriver ut meldinger mottatt fra serveren.
    Kjører i en egen tråd.
    """
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Serveren lukket tilkoblingen eller meldingen var tom.")
                break
            print(f"\n{message}") # \n for å unngå at meldingen kommer på samme linje som input-prompt
    except ConnectionResetError:
        print("Tilkoblingen til serveren ble tilbakestilt.")
    except ConnectionAbortedError:
        print("Tilkoblingen til serveren ble avbrutt.")
    except Exception as e:
        print(f"[FEIL I MOTTAK] En feil oppstod: {e}")
    finally:
        print("Avslutter mottakstråden.")
        client_socket.close() # Lukk socketen hvis den ikke allerede er lukket

# Hovedfunksjon for klienten
def start_client():
    """
    Starter chat-klienten og kobler til serveren.
    """
    # Definer serverens IP-adresse og port
    # Endre 'localhost' til serverens faktiske IP-adresse hvis den kjører på en annen maskin
    SERVER_HOST = input("Skriv inn serverens IP-adresse (f.eks. localhost eller 192.168.1.10): ")
    SERVER_PORT = 65432  # Samme port som serveren bruker

    # Opprett en socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Koble til serveren
        print(f"Kobler til serveren på {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Koblet til serveren!")

        # Start en tråd for å motta meldinger fra serveren
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True # Tillater hovedprogrammet å avslutte selv om tråden kjører
        receive_thread.start()

        # Hovedløkke for å sende meldinger
        while True:
            message_to_send = input("Skriv melding (eller 'avslutt' for å koble fra): ")
            if message_to_send:
                client_socket.send(message_to_send.encode('utf-8'))
                if message_to_send.lower() == 'avslutt':
                    print("Kobler fra serveren...")
                    break
        
    except socket.error as e:
        print(f"[SOCKET FEIL] Kunne ikke koble til serveren: {e}")
    except KeyboardInterrupt:
        print("\n[AVSLUTTER] Klienten avsluttes manuelt.")
        try:
            client_socket.send("avslutt".encode('utf-8')) # Informer serveren
        except:
            pass # Ignorer feil hvis socket allerede er lukket
    finally:
        print("Lukker klient socket.")
        client_socket.close()

if __name__ == "__main__":
    start_client()
