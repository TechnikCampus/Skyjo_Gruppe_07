##### Client network functions #####
import socket
import pickle
import struct

def connect_to_server(name,game,maxplayers,server_ip):                # erzeugt verbindung zum Server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((server_ip,65432))
    client_data = {"Name": name, "Game":game, "Max Players": maxplayers}    # Spielername und Name des Spiels dem man beitreten möchte
    sock.sendall(pickle.dumps(client_data))      # dem Server wird bei einer Neuverbindung der Name des neuen Clients mitgeteilt
    return sock

def receive_from_server(sock):
    try:
        
        raw_msglen = recvall(sock, 4)
        if not raw_msglen:
            return "Nichts gesendet vom Server"
        msglen = struct.unpack(">I", raw_msglen)[0]  
        
        # Den Header der Daten lesen, wie viele Bytes sollen empfangen werden?

        data = recvall(sock, msglen)
        if not data:
            return "Nichts gesendet vom Server"
        
        # Genau so viele Bytes lesen

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
        'Player Game': player_game
    }

    for parameter in player_parameters:
        info[parameter[0]] = parameter[1]

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

    


