##### Main server script #####

import Server as svr
import pygame
import Common as cmn
from queue import Queue

server = svr.start_socket()     # startet einen Server
game_list = []                  # Liste aller laufenden Spiele  
client_queue = Queue()          # startet eine Queue für threadsichere Datenverarbeitung


pygame.init()

while True:

    svr.create_client_thread(server,game_list,client_queue)     # auf neue verbindungen überprüfen, falls da einen 
                                                                # Thread starten

    while not client_queue.empty():     # In dieser Schleife werden Client-Anfragen verarbeitet

        client_message = client_queue.get()

        # Nun: Überprüfen um was für eine Art Nachricht es sich handelt:

        # client_message[0]: Art der Nachricht

        # client_message[1]: Absender bzw. Spielname (siehe network.py)

        # client_message[2]: Verschiedene Spieldaten, siehe Client\network.py -> def send_to_server
        # (nur wenn client_messages[0] = "Client info")

        if client_message[0] == "Online Again":
            print(f"{client_message[1][0]} ist online wieder im Spiel : {client_message[1][1]}")
            for game in game_list:
                for player in game.player_list:
                    if player.name == client_message[1][0]:
                        player.is_online = True                # ein alter Spieler hat sich wieder verbunden!

        elif client_message[0] == "New Player":
            print(f"{client_message[1][0]} hat sich verbunden, ist in Spiel: {client_message[1][1]}")
            for game in game_list:
                if game.name == client_message[1][1]:
                    game.player_list.append(cmn.Player(client_message[1][0]))   # neue Instanz eines Spielers erstellen mit dem neuen Namen
                    game.player_counter += 1                                    # Spielerzähler erhöhen
                    if len(game.player_list) == 1:
                        game.player_list[0].is_admin = True                     # Wenn der Spieler das Spiel erstellt hat wird er Admin
                    for player in game.player_list:
                        if player.name == client_message[1][0]:
                            player.is_online = True                             # ein neuer Spieler hat sich verbunden
        
        elif client_message[0] == "New Game":                                   # ein neues Spiel wurde erstellt!
            print(f"Ein neues Spiel wurde gestartet mit dem Namen: {client_message[1][0]}")                       
            new_game = cmn.Game_state(client_message[1][0],client_message[1][1])          # neue Instanz von game_state

            # client_message[1][0]: Spielname
            # client_message[1][1]: max Spieleranzahl
                                         
            game_list.append(new_game)                 # anhängen an game_list


        elif client_message[0] == "Lost connection": 
            print(f"{client_message[1][0]} hat die Verbindung verloren, ist nicht mehr online in: {client_message[1][1]}")
            for game in game_list:
                if game.name == client_message[1][1]:
                    for player in game.player_list:
                        if player.name == client_message[1]:
                            player.is_online = False               # ein Spieler hat die Verbindung verloren

        elif client_message[0] == "Client info":           # "Befehle" des Clients wurden empfangen!
            pass
            
            # Hier soll nun ausgeführt werden: Funktionen zur Verarbeitung des Spielerzugs! (siehe game_state)

            # client_message[1] = Name des Clients
            # client_message[2] = Name des Spiels in dem der Client ist


            ################################################################# 

            if "Take from Discard Pile" in client_message[3]:

                x,y = client_message[3].get("Take from Discard Pile")

                if svr.check_for_permission(game_list,client_message[1],client_message[2],"Take from Discard Pile"):
                    
                    for game in game_list:
                        if game.name == client_message[2]:
                            for player in game.player_list:
                                if player.name == client_message[1]:

                                    if player.card_deck[x,y]:
                                        player.card_deck[x][y], game.discard_pile[0] = game.discard_pile[0], player.card_deck[x][y]
                                        game.discard_pile[0].visible = True

                                    # Existiert die Karte?
                                    # Karte von Ablagestapel mit der des Spielers tauschen
                                    # Karte auf Ablagestapel aufdecken

                                    # Hier fehlt: Nächsten Spieler zum Zug berechtigen

            elif "Check Draw Pile" in client_message[3]:

                if svr.check_for_permission(game_list,client_message[1],client_message[2],"Check Draw Pile"):

                    for game in game_list:
                        if game.name == client_message[2]:
                            game.draw_pile[0].visible = True

                            # Nachziehstapel aufdecken

            elif "Take from Draw Pile" in client_message[3]:

                x,y = client_message[3].get("Take from Draw Pile")

                if svr.check_for_permission(game_list,client_message[1],client_message[2],"Take from Draw Pile"):

                    for game in game_list:
                        if game.name == client_message[2]:
                            for player in game.player_list:
                                if player.name == client_message[1]:

                                    if player.card_deck[x][y]:
                                        player.card_deck[x][y].visible = True
                                        game.discard_pile[0] = player.card_deck[x][y]
                                        player.card_deck[x][y] = game.draw_pile[0]
                                        game.draw_pile.pop(0)

                                        # Existiert die Karte
                                        # Karte im Spielerdeck aufdecken
                                        # In den Ablagestapel kopieren
                                        # Karte vom Nachziehstapel in Kartendeck kopieren
                                        # Oberste Karte vom Nachziehstapel entfernen

                                        # Hier fehlt: Nächsten Spieler zum Zug berechtigen

            elif "Flip Card" in client_message[3]:

                x,y = client_message[3].get("Flip Card")

                if svr.check_for_permission(game_list,client_message[1],client_message[2],"Flip Card"):

                    for game in game_list:
                        if game.name == client_message[2]:
                            for player in game.player_list:
                                if player.name == client_message[1]:

                                    if player.card_deck[x][y]:
                                        if not player.card_deck[x][y].visible: 
                                            player.card_deck[x][y].visible = True
                                            if player.is_active:
                                                game.discard_pile.insert(0,game.draw_pile.pop(0))

                                                # Hier fehlt: Nächsten Spieler zum Zug berechtigen

                                    # Existiert die Karte?
                                    # Falls noch nicht aufgdeckt aufdecken
                                    # Karte vom Nachziehstapel auf Ablagestapel,
                                    # wenn der Spieler gerade einen Zug gemacht hat, NICHT wenn
                                    # es Rundenbeginn war und der Spieler der startet ausgewählt wird

            #######################################################################
                                
    # Nach Abprüfen und Verarbeiten der Client-Anfragen generelle Spiellogikfunktionen durchführen:

    for game in game_list:

        if svr.is_lobby_ready(game):         # schauen ob ein Spiel gestartet werden kann

            # Spielstartlogik: Karten mischen usw.
            svr.start_game(game,cmn.card_set)
        
        else:

            # Während das Spiel läuft Spielfunktionen ausführen, z.B. Punkte zählen usw.
            svr.update_game_state(game)
            


