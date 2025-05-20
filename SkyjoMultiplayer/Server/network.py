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

def create_client_thread(server,game_list,client_messages): # überprüft neue Vebindungen und erstellt einen Thread pro Client

    try:
        conn,addr = server.accept()

        try:
            name_message = pickle.loads(conn.recv(1024))        # evtl empfindlich für Übertragungsfehler!
                                                                # Name von neuer Verbindung untersuchen
            new_client_name = name_message.get("Name",None)
            new_client_game = name_message.get("Game",None)
        except:
            print("Fehler: Nichts empfangen von neuem Client")
            conn.close()
            return
        
        if not new_client_name:
            print("Fehler: Der Client hat keinen Namen mitgeschickt")
            conn.close()
            return

        connections.append((conn,addr))
        print(f"Neuer Thread gestartet für {new_client_name} , {addr}")
        thread = threading.Thread(target=handle_client, args = (conn,addr,game_list,client_messages,new_client_name,new_client_game))    # thread wird gestartet der handle_client ausführt
        thread.start()

    except BlockingIOError:  # nichts tun falls keine neue Verbindung da
        pass

def send_to_client(game,conn,player_name):    # sendet dictionary mit Daten an Client
    
    message_to_client = {
                        "Game Round" : game.round,
                        "Draw Counter": game.draw_counter,
                        "Player Number": game.player_counter,
                        "Discard Pile" : game.discard_pile,
                        "Draw Pile" : game.draw_pile,
                        "Players" : game.player_list,
                        "Your Name": player_name
                        } 
    
    conn.sendall(pickle.dumps(message_to_client))   

def receive_from_client(conn):    # empfängt von Client gesendetes Dictionary
    
    try:
        message_from_client = pickle.loads(conn.recv(1024))
        return message_from_client
    except:
        print("Nichts empfangen")
        return None

def handle_client(conn,addr,game_list,client_messages,new_client_name,new_client_game):  # wird pro Spieler aufgerufen um dessen Eingaben zu verarbeiten
    
    # In handle_client() nur über client_messages.put() game_state indirekt verändern!
    # ansonsten Synchronisationsprobleme bei vielen Clients (vermutlich)

    thread_player_name = None
    
    for game in game_list:   # schauen ob ein Spiel mit diesem Namen schon läuft

        if new_client_game == game.name:

            for player in game.player_list:

                if new_client_name == player.name:                 # überprüfen ob schon ein Spieler mit diesem Namen vorhanden ist

                    if not player.is_online:
                        thread_player_name = new_client_name
                        thread_player_game = game  
                        client_messages.put(("Online Again",(thread_player_name,thread_player_game)))    # Server über Rückkehr informieren

                    else:
                        print(f"Fehler: {new_client_name} existiert schon und ist online in: {game.name}")    # Verbindung ablehnen, Threadschleife endet
                        conn.close()
                        return
                    
    if not thread_player_game:
        thread_player_game = new_client_game
        client_messages.put(("New Game",thread_player_game))      # Server signalisieren dass ein neues Spiel gestartet wurde

    if not thread_player_name:
        thread_player_name = new_client_name
        client_messages.put(("New Player", (thread_player_name,thread_player_name)))  # Server signalisieren dass ein neuer Spieler da ist

    for game in game_list:
        if game.name == thread_player_game:
            thread_game = game

    while True:
        try:
            send_to_client(thread_game,conn,thread_player_name)  # die wichtigen Daten von game_state werden an die clients geschickt
        except:
            conn.close()
            client_messages.put(("Lost connection",(thread_player_name,thread_player_game)))     # Bei Fehler beim senden, Server informieren
            print("Fehler beim senden an client")                           # und Verbidnung trennen
            return                                                               

        message = receive_from_client(conn)   # von client einen "Befehl" empfangen
        if message:
            client_messages.put(("Client info",thread_player_name,message))   # diesen Befehl in die Queue anhängen (threadsicher)
        else:
            conn.close()
            client_messages.put(("Lost connection",thread_player_name))    # so dass game_state informiert werden kann
                                                                           # dass dieser Spieler verschwunden ist
            return




