##### Main server script #####

import Server as svr
import pygame
import Common as cmn
from queue import Queue

server = svr.start_socket()     # startet einen Server
game_state = cmn.Game_state()   # erzeugt eine Instanz von game_state
client_messages = Queue()       # startet eine Queue für threadsichere Datenverarbeitung


pygame.init()
clock = pygame.time.Clock()

while True:

    svr.create_client_thread(server,game_state,client_messages)     # auf neue verbindungen überprüfen, falls da einen 
                                                                     # Thread starten

    # Test #

    while not client_messages.empty():
        message = client_messages.get()
        if message[0] == "Online Again":        # hier nun player_list durchsuchen und beim betroffenen Spieler .is_online anpassen
            print(f"{message[1]} ist online wieder")
        elif message[0] == "New Player":        # hier nun einen neuen Spieler hinzufügen mit message[1] als Name
            print(f"{message[1]} hat sich verbunden!")
        elif message[0] == "Lost connection":   # hier nun player_list durchsuchen und beim betroffenen Spieler .is_online anpassen
            print(f"{message[1]} hat die Verbindung verloren!")
        elif message[0] == "Client info":       # hier nun die Client Info (also "Befehle" vom Client ausführen)
            print(f"Nachricht von {message[1]} 1: {message[2]["Take_from_discard_Pile"]} 2: {message[2]["Accept_Card"]} 3: {message[2]["Choose_Card"]}")
            if message[2]["Accept_Card"]:
                game_state.round -= 1
            elif message[2]["Choose_card"]:
                game_state.round += 1
                

        # Test #
    """
    while not client_messages.empty():               # die Queue mit Client Nachrichten durchgehen 

        message = client_messages.get() 

        # message[0] zeigt um welche "Art" Nachricht aus den Threads es sich handelt
        # message[1] gibt den Spielername an

        if message[0] == "Online Again":        # hier nun player_list durchsuchen und beim betroffenen Spieler .is_online anpassen
            pass 
        elif message[0] == "New Player":        # hier nun einen neuen Spieler hinzufügen mit message[1] als Name
            pass
        elif message[0] == "Lost connection":   # hier nun player_list durchsuchen und beim betroffenen Spieler .is_online anpassen
            pass
        elif message[0] == "Client info":       # hier nun die Client Info (also "Befehle" vom Client ausführen)

            # Test:
            
            print(f"{message[1]} hat etwas gesendet!")
            if message[2].Player_Name == "Jonas":
                game_state.round += 0.1
    """



