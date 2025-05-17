##### Main server script #####

import Server as svr
import pygame
import Common as cmn
from queue import Queue

server = svr.start_socket()     # startet einen Server
game_state = cmn.Game_state()   # erzeugt eine Instanz von game_state
client_queue = Queue()       # startet eine Queue für threadsichere Datenverarbeitung


pygame.init()

while True:

    svr.create_client_thread(server,game_state,client_queue)     # auf neue verbindungen überprüfen, falls da einen 
                                                                 # Thread starten

    while not client_queue.empty():     # In dieser Schleife werden Client-Anfragen verarbeitet

        client_message = client_queue.get()

        # Nun: Überprüfen um was für eine Art Nachricht es sich handelt:

        # client_message[0]: Art der Nachricht

        # client_message[1]: Name des Clients

        # client_message[2]: Verschiedene Spieldaten, siehe Client\network.py -> def send_to_server
        # (nur wenn client_messages[0] = "Client info")

        if client_message[0] == "Online Again":
            print(f"{client_message[1]} ist online wieder")
            for player in game_state.player_list:
                if player.name == client_message[1]:
                    player.is_online = True                # ein alter Spieler hat sich wieder verbunden!

        elif client_message[0] == "New Player":
            print(f"{client_message[1]} hat sich verbunden!")
            game_state.player_list.append(cmn.Player(client_message[1]))   # neue Instanz eines Spielers erstellen mit dem neuen Namen
            for player in game_state.player_list:
                player.is_online = True                    # ein neuer Spieler hat sich verbunden

        elif client_message[0] == "Lost connection": 
            print(f"{client_message[1]} hat die Verbindung verloren!")
            for player in game_state.player_list:
                if player.name == client_message[1]:
                    player.is_online = False               # ein Spieler hat die Verbindung verloren

        elif client_message[0] == "Client info":           # "Befehle" des Clients wurden empfangen!
            pass
            
            # Hier die Befehle des Clients importieren! Befehle des Clients als Dictionary mit
            # unterschiedlichen Parametern.

            # client_message[1] = Name des Clients

            # Untersuchung eines Befehls(Beispiel):
            # client_message[2].get("take_from_discard_pile", False)



