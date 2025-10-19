# client_gui.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

# Globale variabler for GUI-elementer og socket
client_socket = None
receive_thread = None
username = "Bruker" # Standard brukernavn

# Funksjon for å motta meldinger fra serveren og vise dem i GUI
def receive_messages(text_area):
    """
    Lytter etter og viser meldinger mottatt fra serveren i GUI.
    Kjører i en egen tråd.
    """
    if not client_socket:
        return

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                text_area.insert(tk.END, "Serveren lukket tilkoblingen eller meldingen var tom.\n")
                text_area.see(tk.END) # Rull til slutten
                break
            text_area.insert(tk.END, message + "\n")
            text_area.see(tk.END) # Rull til slutten
    except ConnectionResetError:
        if text_area.winfo_exists(): # Sjekk om widgeten fortsatt eksisterer
            text_area.insert(tk.END, "Tilkoblingen til serveren ble tilbakestilt.\n")
            text_area.see(tk.END)
    except ConnectionAbortedError:
        if text_area.winfo_exists():
            text_area.insert(tk.END, "Tilkoblingen til serveren ble avbrutt.\n")
            text_area.see(tk.END)
    except Exception as e:
        if text_area.winfo_exists():
            text_area.insert(tk.END, f"[FEIL I MOTTAK] En feil oppstod: {e}\n")
            text_area.see(tk.END)
    finally:
        if text_area.winfo_exists():
            text_area.insert(tk.END, "Avslutter mottakstråden.\n")
            text_area.see(tk.END)
        if client_socket:
            try:
                client_socket.close()
            except:
                pass # Ignorer feil hvis socket allerede er lukket

# Funksjon for å sende meldinger til serveren
def send_message(event=None): # event=None for å tillate binding til Enter-tasten
    """
    Sender meldingen fra input-feltet til serveren.
    """
    if not client_socket:
        messagebox.showerror("Feil", "Ikke koblet til serveren.")
        return

    message_to_send = message_entry.get()
    if message_to_send:
        full_message = f"{username}: {message_to_send}"
        try:
            client_socket.send(full_message.encode('utf-8'))
            # Viser egen melding i chat-vinduet også
            # chat_area.insert(tk.END, f"Meg: {message_to_send}\n")
            # chat_area.see(tk.END)
            message_entry.delete(0, tk.END) # Tøm input-feltet
            if message_to_send.lower() == 'avslutt':
                chat_area.insert(tk.END, "Kobler fra serveren...\n")
                chat_area.see(tk.END)
                # Ingen break her, la receive_messages håndtere frakobling fra serverens side
                # eller lukk vinduet for å avslutte
        except socket.error as e:
            chat_area.insert(tk.END, f"[SENDFEIL] {e}\n")
            chat_area.see(tk.END)
            if client_socket:
                client_socket.close()


# Funksjon for å håndtere lukking av vinduet
def on_closing():
    """
    Håndterer hva som skjer når GUI-vinduet lukkes.
    """
    if client_socket:
        try:
            # Informer serveren om at klienten avslutter (valgfritt, men god praksis)
            client_socket.send(f"{username}: avslutt".encode('utf-8'))
            client_socket.close()
        except socket.error:
            pass # Ignorer feil hvis socket allerede er lukket eller utilgjengelig
    root.destroy() # Lukk Tkinter-vinduet

# Hovedfunksjon for klienten
def start_client_gui():
    """
    Starter chat-klienten med et grafisk brukergrensesnitt.
    """
    global client_socket
    global receive_thread
    global username

    # Spør om server-IP og brukernavn ved oppstart
    # Dette er en enkel måte, kan gjøres mer elegant i et større GUI
    server_host_input = simpledialog.askstring("Server Detaljer", "Skriv inn serverens IP-adresse (f.eks. localhost):", parent=root)
    if not server_host_input:
        root.destroy() # Lukk hvis brukeren avbryter
        return

    username_input = simpledialog.askstring("Brukernavn", "Skriv inn ditt brukernavn:", parent=root)
    if username_input:
        username = username_input
    
    SERVER_HOST = server_host_input
    SERVER_PORT = 65432  # Samme port som serveren bruker

    # Opprett en socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Koble til serveren
        chat_area.insert(tk.END, f"Kobler til serveren på {SERVER_HOST}:{SERVER_PORT}...\n")
        chat_area.see(tk.END)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        chat_area.insert(tk.END, "Koblet til serveren!\n")
        chat_area.see(tk.END)
        messagebox.showinfo("Tilkoblet", f"Koblet til serveren som {username}!")


        # Start en tråd for å motta meldinger fra serveren
        receive_thread = threading.Thread(target=receive_messages, args=(chat_area,), daemon=True)
        receive_thread.start()

    except socket.error as e:
        if chat_area: # Sjekk om chat_area er initialisert
            chat_area.insert(tk.END, f"[SOCKET FEIL] Kunne ikke koble til serveren: {e}\n")
            chat_area.see(tk.END)
        else:
            print(f"[SOCKET FEIL] Kunne ikke koble til serveren: {e}")
        messagebox.showerror("Tilkoblingsfeil", f"Kunne ikke koble til serveren: {e}")
        if client_socket:
            client_socket.close()
        root.destroy() # Lukk vinduet hvis tilkobling feiler
        return
    except Exception as e: # Generell feilhåndtering for uventede feil under oppsett
        if chat_area:
            chat_area.insert(tk.END, f"[OPPSTARTSFEIL] {e}\n")
            chat_area.see(tk.END)
        else:
            print(f"[OPPSTARTSFEIL] {e}")
        messagebox.showerror("Feil", f"En uventet feil oppstod: {e}")
        if client_socket:
            client_socket.close()
        root.destroy()
        return

# Sett opp hovedvinduet for GUI
root = tk.Tk()
root.title(f"Python Chat Klient - {username}") # Tittelen kan oppdateres etter brukernavn er satt

# Chat-område (tekstboks for å vise meldinger)
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='normal', height=20, width=70)
chat_area.pack(padx=10, pady=10)
chat_area.configure(state='disabled') # Gjør den skrivebeskyttet først
# Midlertidig enable for å sette inn startmeldinger, så disable igjen
chat_area.configure(state='normal')
chat_area.insert(tk.END, "Velkommen til chatten! Koble til en server for å starte.\n")
chat_area.configure(state='disabled')


# Input-felt for å skrive meldinger
message_entry = tk.Entry(root, width=60, font=("Helvetica", 12))
message_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10), fill=tk.X, expand=True)
message_entry.bind("<Return>", send_message) # Send melding med Enter-tasten

# Send-knapp
send_button = tk.Button(root, text="Send", command=send_message, font=("Helvetica", 10), bg="#4CAF50", fg="white", relief=tk.RAISED, borderwidth=2)
send_button.pack(side=tk.RIGHT, padx=(5, 10), pady=(0, 10))

# Start tilkoblingsprosessen etter at GUI er satt opp
# Vi kan kalle start_client_gui() fra en meny eller knapp senere for mer fleksibilitet
# For nå, la oss starte den via en knapp eller automatisk etter at brukernavn er satt.

# Meny (valgfritt, men god praksis for tilkobling etc.)
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Koble til server...", command=lambda: threading.Thread(target=start_client_gui, daemon=True).start()) # Kjør i tråd for å ikke fryse GUI
filemenu.add_separator()
filemenu.add_command(label="Avslutt", command=on_closing)
menubar.add_cascade(label="Fil", menu=filemenu)
root.config(menu=menubar)


# Håndter lukking av vinduet
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start Tkinter hovedløkke
if __name__ == "__main__":
    # Initialiser GUI-elementer før start_client_gui kalles for å unngå referansefeil
    # start_client_gui() vil nå bli kalt via menyen
    # Hvis du vil koble til automatisk ved oppstart (etter å ha fått IP/brukernavn):
    # root.after(100, start_client_gui) # Forsinket kall for å la GUI initialisere
    
    # For nå, la brukeren klikke "Koble til server..." fra menyen.
    # Eller, for enklere testing, kall start_client_gui direkte etter at root er definert.
    # Men det er bedre å la brukeren initiere tilkoblingen.
    # For å teste umiddelbart, kan du fjerne menyen og kalle:
    # threading.Thread(target=start_client_gui, daemon=True).start()
    # Men da må input for server IP og brukernavn håndteres før GUI-løkken starter helt.
    
    # La oss starte med å be om detaljer og så starte GUI-loopen.
    # For å unngå at simpledialog blokkerer for tidlig, kan vi starte tilkoblingen
    # etter at hovedvinduet er synlig, f.eks. via en knapp eller meny.
    # Den nåværende implementasjonen med menyen er en god start.
    
    root.mainloop()
