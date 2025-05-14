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

    clock.tick(60)

    svr.create_client_thread(server,game_state,client_messages)     # auf neue verbindungen überprüfen, falls da einen 
                                                                    # Thread starten
    
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
            pass       




