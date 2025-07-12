##### Server Network Functions #####

import threading
import socket
import pickle
import struct

connections = []

def start_socket():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # erstellt socket
    server.bind(('0.0.0.0', 65111))  
    server.listen(10)            # maximale gleichzeitige Clientanzahl
    server.setblocking(False)    # wichtig, das Hauptspielschleife nicht blockiert wird falls keine neue Verbindung da
    print("Server gestartet")
    return server

def create_client_thread(server,game_dict,client_messages): # überprüft neue Vebindungen und erstellt einen Thread pro Client

    try:
        conn,addr = server.accept()   # neue Verbindung akzeptieren
        conn.settimeout(1.0)

        try:
            name_message = pickle.loads(conn.recv(1024))
            new_client_name = name_message.get("Name",None)    # Grunddaten der neuen Verbindung erfassen
            new_client_game = name_message.get("Game",None)
            max_player_count = name_message.get("Max Players",0)
        except:
            print("Fehler: Nichts empfangen von neuem Client")
            conn.close()
            return
        
        if not new_client_name:
            print("Fehler: Der Client hat keinen Namen mitgeschickt")
            conn.close()
            return

        connections.append((conn,addr))  # Zu vorhandenen Verbindungen hinzufügen
        print(f"Neuer Thread gestartet für {new_client_name} , {addr}")

        # Thread starten:
        thread = threading.Thread(target=handle_client, daemon= True, args = (conn,addr,game_dict,client_messages,new_client_name,new_client_game,max_player_count))    # thread wird gestartet der handle_client ausführt
        thread.start()

    except BlockingIOError:  # nichts tun falls keine neue Verbindung da
        pass

def send_to_client(game,conn,player_name):    # sendet dictionary mit Daten an Client
    
    message_to_client = {
                        "Game Name": game.name,
                        "Game Round" : game.round,
                        "Draw Counter": game.draw_counter,
                        "Player Number": game.player_counter,
                        "Discard Pile" : game.discard_pile,
                        "Draw Pile" : game.draw_pile,
                        "Players" : game.player_list,
                        "Your Name": player_name,
                        "Final Phase": game.final_phase,
                        "Active": game.active_player,
                        "Running": game.running,
                        "End Scores": game.end_scores
                        } 

    # In den Header packen wie viele Daten gesendet werden, dann Daten senden:
    try:
        data = pickle.dumps(message_to_client)
        msg = struct.pack(">I", len(data)) + data
        conn.sendall(msg)
    except Exception as e:
        print(f"Fehler beim Senden an Client: {e}")

def recvall(conn, n):   # Hilfsfunktion die n Bytes liest

    data = b""
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def receive_from_client(conn):

    # Header lesen: Wie viele Bytes schickt der Client?
    try:
        raw_msglen = recvall(conn, 4)
        if not raw_msglen:
            print("Vom Client kam nichts (Header fehlt)")
            return None
        msglen = struct.unpack(">I", raw_msglen)[0]
    
        # So viele Bytes wie im Header spezifiziert auslesen:
        data = recvall(conn, msglen)
        if not data:
            print("Vom Client kam nichts (Body fehlt)")
            return None
        return pickle.loads(data)
    
    except socket.timeout:
        return "Nichts gesendet vom Client"
    except Exception as e:
        print(f"Fehler beim Empfangen vom Client: {e}")
        return None

def handle_client(conn,addr,game_dict,client_messages,new_client_name,new_client_game,maxplayers):
    
    # Läuft in den Threads der einzelnen Verbindungen
    # In handle_client() nur über client_messages.put() game_state indirekt verändern!
    # ansonsten Synchronisationsprobleme bei vielen Clients

    thread_player_name = None    # threadspezifische Variablen die den Client identifizieren
    thread_player_game = None
    thread_game = None
    
    try:
        game = game_dict.get(new_client_game)
        thread_player_game = game.name
        thread_game = game                   # schauen ob ein Spiel mit diesem Namen schon vorhanden ist
    except:
        pass

    if not thread_player_game:
        thread_player_game = new_client_game
        client_messages.put(("New Game", (thread_player_game, maxplayers)))    # Spielname noch nicht vorhanden, neues starten

        # Warten, bis Spiel sicher in game_dict eingetragen ist
        while True:
            thread_game = game_dict.get(thread_player_game)
            if thread_game:
                break 
    
    number_of_online_players = 0
    for player in thread_game.player_list:
        if player.is_online:
            number_of_online_players += 1

    if number_of_online_players == thread_game.max_players:
        print(f"Fehler: {thread_player_game} ist bereits voll! ")
        conn.close()
        return                                 # erstmal schauen ob in dem Spiel noch Platz ist! Falls nein verbindung ablehnen
    
    for player in thread_game.player_list:     # schauen ob schon Spieler mit diesem namen da sind
        if new_client_name == player.name:

            if not player.is_online:
                thread_player_name = new_client_name
                client_messages.put(("Online Again",(thread_player_name,thread_player_game)))   # Spieler kehrt zurück, nach verbindungsverlust
            else:
                print(f"Fehler: {new_client_name} existiert schon und ist online in: {thread_player_game}")
                conn.close()
                return                         # Verbindung ablehnen, keine doppelte Namensbelegungen
            
    if not thread_player_name and (thread_game.player_counter < thread_game.max_players):  # falls ganz neuer Name, neuen Spieler erstellen
        thread_player_name = new_client_name
        client_messages.put(("New Player", (thread_player_name,thread_player_game)))

    while True:
        
        # Threadschleife beenden wenn nicht mehr benötigt:
        if thread_game.closed:
            print(f"Thread für {thread_player_name} geschlossen, da Spiel nicht mehr existiert")
            conn.close()
            break

        for player in thread_game.player_list:
            if player.name == thread_player_name and player.left:
                print(f"Thread für {thread_player_name} geschlossen, da der Spieler das Spiel verlassen hat")
                conn.close()
                break
        
        # Hauptthreadschleife:
        try:
            send_to_client(thread_game,conn,thread_player_name)  # die wichtigen Daten von game_state werden an die clients geschickt
        except:
            conn.close()
            client_messages.put(("Lost connection",(thread_player_name,thread_player_game)))     # Bei Fehler beim senden, Server informieren
            print("Fehler beim senden an client")                                                # und Verbidnung trennen
            return                                                               

        message = receive_from_client(conn)   # von client einen Befehl empfangen

        if message == "Nichts gesendet vom Client":
            continue 

        elif message:
            client_messages.put(("Client info",thread_player_name,thread_player_game,message))   # diesen Befehl in die Queue anhängen (threadsicher)
            
        else:
            conn.close()
            client_messages.put(("Lost connection",(thread_player_name,thread_player_game)))    # so dass game_state informiert werden kann
                                                                                                # dass dieser Spieler verschwunden ist
            return
        






