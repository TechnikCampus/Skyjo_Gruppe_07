##### Client network functions #####
import socket
import pickle

def connect_to_server(name,game,maxplayers,server_ip):                # erzeugt verbindung zum Server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((server_ip,65432))
    client_data = {"Name": name, "Game":game, "Max Players": maxplayers}    # Spielername und Name des Spiels dem man beitreten möchte
    sock.sendall(pickle.dumps(client_data))      # dem Server wird bei einer Neuverbindung der Name des neuen Clients mitgeteilt
    return sock

def receive_from_server(sock):    # Daten vom Server empfangen
    
    try:
        received = pickle.loads(sock.recv(4096))
        return received
    except:
        print("Fehler beim empfangen vom Server!")
        sock.close()
        return None


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

    


