# server.py
import socket
import threading

# Funksjon for å håndtere en klients tilkobling
def handle_client(client_socket, client_address):
    """
    Håndterer kommunikasjonen med en tilkoblet klient.
    Mottar meldinger fra klienten og sender meldinger til klienten.
    """
    print(f"[NY TILKOBLING] {client_address} koblet til.")
    connected = True
    try:
        while connected:
            # Motta melding fra klienten
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"[{client_address}] Koblet fra (tom melding).")
                connected = False
                break

            if message.lower() == 'avslutt':
                print(f"[{client_address}] Ba om å avslutte.")
                client_socket.send("Server: Du har blitt koblet fra.".encode('utf-8'))
                connected = False
                break

            print(f"[{client_address}] {message}")

            # Send svar tilbake til klienten (eller til den andre klienten i en to-personers chat)
            # For enkelhets skyld, i dette eksemplet sender vi bare en bekreftelse
            # eller lar serveroperatøren skrive en melding.
            # For en ekte to-personers chat, må du videresende meldingen til den andre tilkoblede klienten.
            # Dette eksemplet fokuserer på en enkelt klient-server-interaksjon.

    except ConnectionResetError:
        print(f"[{client_address}] Tilkoblingen ble tilbakestilt av klienten.")
        connected = False
    except Exception as e:
        print(f"[FEIL] En feil oppstod med {client_address}: {e}")
        connected = False
    finally:
        print(f"Lukker tilkobling for {client_address}.")
        client_socket.close()

# Funksjon for serveren å sende meldinger (valgfritt, for server-til-klient-kommunikasjon)
def send_messages(client_socket):
    """
    Lar serveroperatøren sende meldinger til den tilkoblede klienten.
    Kjører i en egen tråd.
    """
    try:
        while True:
            message_to_send = input() # Serveroperatøren skriver her
            if message_to_send:
                client_socket.send(message_to_send.encode('utf-8'))
                if message_to_send.lower() == 'avslutt server': # For å stoppe serveren helt
                    print("Serveren avsluttes...")
                    # Merk: Dette vil bare stoppe sendingstråden og ikke nødvendigvis serveren
                    # For en fullstendig stopp, trenger du mer sofistikert håndtering
                    break
    except EOFError: # Håndterer ctrl+d for å stoppe input
        print("Input-tråd for sending avsluttes.")
    except Exception as e:
        print(f"[FEIL I SENDING] {e}")


# Hovedfunksjon for serveren
def start_server():
    """
    Starter chat-serveren, lytter etter innkommende tilkoblinger.
    """
    # Definer serverens IP-adresse og port
    # La IP være tom for å lytte på alle tilgjengelige grensesnitt
    # Eller bruk 'localhost' for kun lokale tilkoblinger
    HOST = '0.0.0.0'
    PORT = 65432  # Portnummer (bruk en port > 1023)

    # Opprett en socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[STARTER] Serveren starter...")

    try:
        # Bind socketen til adressen og porten
        server_socket.bind((HOST, PORT))
        print(f"[LYTTER] Serveren lytter på {HOST}:{PORT}")

        # Sett serveren til å lytte etter innkommende tilkoblinger (maks 1 i kø her for enkelhet)
        server_socket.listen(1)

        while True: # Hovedløkke for å akseptere nye tilkoblinger
            # Aksepter en ny tilkobling
            # conn er en ny socket-objekt som kan brukes til å sende og motta data på tilkoblingen
            # addr er adressen bundet til socketen i den andre enden av tilkoblingen
            client_socket, client_address = server_socket.accept()

            # Opprett og start en ny tråd for å håndtere klienten
            # Dette lar serveren håndtere flere klienter samtidig (selv om dette eksemplet er enklere)
            client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler_thread.daemon = True # Tillater hovedprogrammet å avslutte selv om tråder kjører
            client_handler_thread.start()

            # Valgfritt: Start en tråd for serveren å sende meldinger til denne klienten
            # For en to-personers chat, ville du hatt en mer kompleks logikk
            # for å videresende meldinger mellom de to klientene.
            # Dette er en forenklet versjon.
            # server_send_thread = threading.Thread(target=send_messages, args=(client_socket,))
            # server_send_thread.daemon = True
            # server_send_thread.start()

            print(f"[AKTIVE TILKOBLINGER] {threading.active_count() - 1}") # -1 for hovedtråden

    except socket.error as e:
        print(f"[SOCKET FEIL] {e}")
    except KeyboardInterrupt:
        print("\n[AVSLUTTER] Serveren avsluttes manuelt.")
    finally:
        print("Lukker server socket.")
        server_socket.close()

if __name__ == "__main__":
    start_server()
