##### Client network functions #####
import socket
import pickle

def connect_to_server(name):      # erzeugt verbindung zum Server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('Hier Ip eingeben',65432))
    name_of_client = {"Name": name}    
    sock.sendall(pickle.dumps(name_of_client)) # dem Server wird bei einer Neuverbindung der Name des neuen Clients mitgeteilt
    return sock

def receive_from_server(sock):    # Daten vom Server verarbeiten
    
    received = pickle.loads(sock.recv(4096))
    return received

    # es fehlt: Sicherungsmechanismus bei verbindungsabbruch!

def send_to_server(sock,player_info,player_name):         # Daten an server senden
    
    info = {
            "Player Name": player_name,
            "Take from discard Pile": player_info[0],
            "Accept Card": player_info[1],
            "Choose Card": player_info[2]                 # während Gameloop den Server mit "Befehlen" updaten
            }                                             # Server entscheidet selbst ob er sie ausführt oder nicht
    sock.sendall(pickle.dumps(info))

    # es fehlt: Sicherungsmechanismus bei verbindungsabbruch!
    


