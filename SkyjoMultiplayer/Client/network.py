##### Client network functions #####
import socket

def connect_to_server():      # erzeugt verbindung zum Server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('Hier IP eingeben',65432))
    return sock

def compress_data():          # Daten komprimieren mit Pickle Modul
    pass

def receive_from_server():    # Daten vom Server verarbeiten
    pass

def send_to_server():         # Daten an server senden
    pass

