##### Client network functions #####
import socket
import pickle

def connect_to_server(name):      # erzeugt verbindung zum Server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('Hier Server IP eingeben',65432))
    name_of_client = {"Name": name}    
    sock.sendall(pickle.dumps(name_of_client)) # dem Server wird bei einer Neuverbindung der Name des neuen Clients mitgeteilt
    return sock

def receive_from_server(sock):    # Daten vom Server verarbeiten
    
    try:
        received = pickle.loads(sock.recv(4096))
        return received
    except:
        print("Fehler beim empfangen vom Server!")
        sock.close()
        return None


def send_to_server(sock,player_info,player_name):         # Daten an server senden
    
    info = {
            'Player_Name': player_name,
            'Take_from_discard_Pile': player_info[0],
            'Accept_Card': player_info[1],
            'Choose_Card': player_info[2]                 # während Gameloop den Server mit "Befehlen" updaten
            }                                             # Server entscheidet selbst ob er sie ausführt oder nicht
    try:
        sock.sendall(pickle.dumps(info))
    except:
        print("Fehler beim senden an Server!")
        sock.close()
        return None

    


