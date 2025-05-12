##### Server Network Functions #####
import threading
import socket
import pickle

connections = []

def start_socket():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # erstellt socket
    server.bind(('0.0.0.0', 65432))  
    server.listen(4)
    server.setblocking(False)    # wichtig, das Hauptspielschleife nicht blockiert wird falls keine neue Verbindung da
    return server

def create_client_thread(server): # überprüft neue Vebindungen und erstellt einen Thread pro Client

    try:
        conn,addr = server.accept()
        connections.append((conn,addr))
        thread = threading.Thread(target=handle_client, args = (conn,addr))    # thread wird gestartet der handle_client ausführt
        thread.start()
        print(f"A new Thread was started for {conn} , {addr}")
    except BlockingIOError:  # nichts tun falls keine neue Verbindung da
        pass

def compress_data():   # benutzt Pickle Modul um Daten senden zu können (senden als Dictionary)
    pass

def send_to_client():    # sendet dictionary mit Daten an Client
    pass

def receive_from_client():    # empfängt von Client gesendetes Dictionary
    pass

def handle_client(conn,addr):  # wird pro Spieler aufgerufen um dessen Eingaben zu verarbeiten

    # Testprogramm #

    print(f"[THREAD GESTARTET] verbunden mit {addr}")
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                print(f"[TRENNUNG] {addr} hat die Verbindung beendet.")
                break

            # Daten deserialisieren
            deserialised = pickle.loads(data)

            # Nachricht ausgeben
            message = deserialised.get("msg", None)
            if message:
                print(f"[{addr}] sagt: {message}")

        except EOFError:
            print(f"[FEHLER] Ungültige oder unvollständige Daten von {addr}")
            break
        except Exception as e:
            print(f"[FEHLER] bei {addr}: {e}")
            break

    conn.close()
    print(f"[THREAD ENDE] Verbindung zu {addr} geschlossen.")

    # Tesptrogramm #




