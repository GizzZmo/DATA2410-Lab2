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
