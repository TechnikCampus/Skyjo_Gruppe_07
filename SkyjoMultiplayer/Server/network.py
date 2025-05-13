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

def create_client_thread(server,game_state,client_messages): # überprüft neue Vebindungen und erstellt einen Thread pro Client

    try:
        conn,addr = server.accept()
        connections.append((conn,addr))
        thread = threading.Thread(target=handle_client, args = (conn,addr,game_state,client_messages))    # thread wird gestartet der handle_client ausführt
        thread.start()
        print(f"A new Thread was started for {conn} , {addr}")
    except BlockingIOError:  # nichts tun falls keine neue Verbindung da
        pass

def send_to_client(game_state,conn):    # sendet dictionary mit Daten an Client
    
    message_to_client = {
                        "Game Round" : game_state.round,
                        "Player Number": game_state.player_counter,
                        "Discard Pile" : game_state.dicard_pile,
                        "Draw Pile" : game_state.draw_pile,
                        "Players" : game_state.player_list
                        }
    conn.sendall(pickle.dumps(message_to_client))

def receive_from_client(conn):    # empfängt von Client gesendetes Dictionary
    
    try:
        message_from_client = pickle.loads(conn.recv(1024))
        return message_from_client
    except:
        print("Nichts empfangen")
        return None

def handle_client(conn,addr,game_state,client_messages):  # wird pro Spieler aufgerufen um dessen Eingaben zu verarbeiten

    send_to_client(game_state,conn)  # die wichtigen (und öfftl. !) Daten von game_state werden an die clients geschickt
    message = receive_from_client(conn)   # von client einen "Befehl" empfangen
    if message:
        client_messages.put((addr,message))   # diesen Befehl in die Queue anhängen (threadsicher)

    """

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

    """




