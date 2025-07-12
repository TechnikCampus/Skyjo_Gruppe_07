##### Client network functions #####

import socket
import pickle
import struct

def connect_to_server(name,game,maxplayers,server_ip):                # erzeugt verbindung zum Server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((server_ip,65111))
    client_data = {"Name": name, "Game":game, "Max Players": maxplayers}    
    sock.sendall(pickle.dumps(client_data))       # Spielerdaten des Clients werden dem Server mitgeteilt
    return sock

def receive_from_server(sock):

    try:

        # Den Header der Daten lesen, wie viele Bytes sollen empfangen werden?
        raw_msglen = recvall(sock, 4)
        if not raw_msglen:
            return "Nichts gesendet vom Server"
        msglen = struct.unpack(">I", raw_msglen)[0]  

        # Genau so viele Bytes lesen (Nutzdaten)
        data = recvall(sock, msglen)
        if not data:
            return "Nichts gesendet vom Server"
        
        return pickle.loads(data)
    except Exception as e:
        print(f"Fehler beim Empfang vom Server: {e}")
        return None

def recvall(sock, n):

    # Hilfsfunktion die n Bytes empfängt
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def send_to_server(sock, player_parameters, player_name, player_game):

    info = {
        'Player Name': player_name,
        'Player Game': player_game          # dem Server Spielername und Spielname mitteilen
    }

    for parameter in player_parameters:
        info[parameter[0]] = parameter[1]   # hängt die Befehle die gesendet werden sollen an das dict an

    # Die Länge der zu sendenden Daten in den Header packen und
    # danach die Daten senden:
    
    try:
        data = pickle.dumps(info)
        msg = struct.pack(">I", len(data)) + data  
        sock.sendall(msg)
    except Exception as e:
        print("Fehler beim Senden an Server:", e)
        sock.close()
        return None

    


