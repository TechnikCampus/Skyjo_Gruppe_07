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

"""
def receive_from_server(sock):    # Daten vom Server empfangen

    
    # Alter Code der Probleme gemacht hat:

    try:
        received = pickle.loads(sock.recv(4096))
        return received
    except:
        print("Fehler beim empfangen vom Server!")
        sock.close()
        return None

    #
        
    try:
        data = sock.recv(4096)
        if not data:
            return "Nichts gesendet vom Server"
        return pickle.loads(data)
    except socket.timeout:
        return "Nichts gesendet vom Server"
    except Exception as e:
        print(f"Fehler beim Empfang vom Server: {e}")
        return None
    
"""
###########################################################
def receive_from_server(sock):
    try:
        # Zuerst 4 Byte lesen → enthalten die Länge der Nutzdaten
        raw_msglen = recvall(sock, 4)
        if not raw_msglen:
            return "Nichts gesendet vom Server"
        msglen = struct.unpack(">I", raw_msglen)[0]  # big-endian unsigned int

        # Jetzt genau msglen Bytes lesen
        data = recvall(sock, msglen)
        if not data:
            return "Nichts gesendet vom Server"

        return pickle.loads(data)
    except Exception as e:
        print(f"Fehler beim Empfang vom Server: {e}")
        return None

def recvall(sock, n):
    """Hilfsfunktion: Lies genau n Bytes vom Socket."""
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

################################################

"""
def send_to_server(sock,player_parameters,player_name,player_game):         # Daten an server senden
    
    info = {'Player Name': player_name,
            'Player Game': player_game} 

    for parameter in player_parameters:
        info[parameter[0]] = parameter[1]

    try:
        sock.sendall(pickle.dumps(info))
    except:
        print("Fehler beim senden an Server!")
        sock.close()
        return None

"""

def send_to_server(sock, player_parameters, player_name, player_game):
    info = {
        'Player Name': player_name,
        'Player Game': player_game
    }

    for parameter in player_parameters:
        info[parameter[0]] = parameter[1]

    try:
        data = pickle.dumps(info)
        msg = struct.pack(">I", len(data)) + data  # Länge + Inhalt
        sock.sendall(msg)
    except Exception as e:
        print("Fehler beim Senden an Server:", e)
        sock.close()
        return None

    


