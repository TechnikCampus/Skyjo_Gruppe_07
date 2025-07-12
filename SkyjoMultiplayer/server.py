##### Main server script #####

import Server as svr
import Common as cmn
from queue import Queue

server = svr.start_socket()     
game_dict = {}                  # Dictionary aller laufenden Spiele  
client_queue = Queue()          # startet eine Queue für threadsichere Datenverarbeitung

while True:

    svr.create_client_thread(server,game_dict,client_queue)     # auf neue verbindungen überprüfen, falls da einen 
                                                                # Thread starten

    while not client_queue.empty():     # In dieser Schleife werden Client-Anfragen in der Queue verarbeitet

        client_message = client_queue.get()

        svr.handle_connections(client_message,game_dict) # kümmert sich um neue Verbindungen, neue Spiele, geschl. Verbindungen
        svr.handle_games(client_message,game_dict)       # verarbeitet Spielerbefehle die aus den Threads kommen

    svr.clean_up_games(game_dict)  # entfernt Spiele die geschlossen wurden und Spieler die weg sind nach Spielende

    for game in game_dict.values():

        if not game.closed:

            if svr.is_lobby_ready(game):                  # schauen ob ein Spiel gestartet werden kann
                print("Die Spielrunde kann jetzt gestartet werden")
                svr.start_game(game,cmn.card_set)         # Spiel starten
        
            else:

                # Während das Spiel läuft Spielfunktionen ausführen, z.B. Punkte zählen usw.
                svr.update_game_state(game,cmn.card_set)

            


