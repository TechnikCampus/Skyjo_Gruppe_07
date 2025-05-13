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

    clock.tick(10)     # zu testzwecken verlangsamt! normal: 60 FPS

    svr.create_client_thread(server,game_state,client_messages)     # auf neue verbindungen überprüfen, falls da einen 
                                                                    # Thread starten

    # Testprogramm #

    game_state.round += 0.1

    # Testprogramm #
    
    while not client_messages.empty():               # die Queue mit Client Nachrichten durchgehen 
        addr,msg = client_messages.get()            

        # Testprogramm #

        print(f"{addr} sagt: {msg}")    # Queue Nachrichten ausgeben

        # Testprogramm #



