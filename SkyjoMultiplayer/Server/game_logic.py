##### Game logic functions on the server #####

import Common as cmn

def handle_connections(client_message,game_dict):

        if client_message[0] == "Online Again":

            # client_message[1][0] = Spielername
            # client_message[1][1] = Spiel dem der Spieler zugeordnet ist

            print(f"{client_message[1][0]} ist online wieder im Spiel : {client_message[1][1]}")
            for game in game_dict.values():
                for player in game.player_list:
                    if player.name == client_message[1][0]:
                        player.is_online = True                # ein alter Spieler hat sich wieder verbunden!

        elif client_message[0] == "New Player":

            # client_message[1][0] = Spielername
            # client_message[1][1] = Spiel dem der Spieler zugeordnet ist

            print(f"{client_message[1][0]} hat sich verbunden, ist in Spiel: {client_message[1][1]}")
            game = game_dict.get(client_message[1][1])

            game.player_list.append(cmn.Player(client_message[1][0]))   # neue Instanz eines Spielers erstellen
            game.player_counter += 1                                    # Spielerzähler des betroffenen Spiels erhöhen
            if len(game.player_list) == 1:
                game.player_list[0].is_admin = True                     # Wenn der Spieler das Spiel erstellt hat wird er Admin
            for player in game.player_list:
                if player.name == client_message[1][0]:
                    player.is_online = True                             # is_online des Spielers setzen
                    player.initialize_card_deck()                       # Kartendeck mit Platzhaltern füllen
        
        elif client_message[0] == "New Game":                           # ein neues Spiel soll erstellt werden

            # client_message[1][0]: Spielname
            # client_message[1][1]: max Spieleranzahl

            print(f"Ein neues Spiel wurde gestartet mit dem Namen: {client_message[1][0]}")
            new_game = cmn.Game_state(client_message[1][0],client_message[1][1])          # neue Instanz von game_state erstellen
                                         
            game_dict[client_message[1][0]] = new_game                                    # anhängen an game_dict


        elif client_message[0] == "Lost connection": 

            # client_message[1][0] = Spielername
            # client_message[1][1] = Spiel dem der Spieler zugeordnet ist

            print(f"{client_message[1][0]} hat die Verbindung verloren, ist nicht mehr online in: {client_message[1][1]}")
            game = game_dict.get(client_message[1][1])
            if game:
                for player in game.player_list:
                    if player.name == client_message[1][0]:
                        player.is_online = False               # is_online des Spielers zurücksetzen

def handle_games(client_message,game_dict):
    
        if client_message[0] == "Client info":

            # client_message[1] = Name des Clients
            # client_message[2] = Name des Spiels in dem der Client ist
            # client_message[3] = Art des Befehls

            if "Take from Discard Pile" in client_message[3]:

                x,y = client_message[3].get("Take from Discard Pile")    # die "Koordinaten" der Zielkarte im Kartendeck

                if check_for_permission(game_dict,client_message[1],client_message[2],"Take from Discard Pile"):
                    # Nur ausführen wenn Client Berechtigung dazu hat:
                    game = game_dict.get(client_message[2])
                    for index,player in enumerate(game.player_list):

                        if player.name == client_message[1]:
                            if player.card_deck[x][y]:
                                # Ausführen wenn die Karte existiert:
                                # Karte mit der vom Ablagestapel tauschen
                                player.card_deck[x][y], game.discard_pile[0] = game.discard_pile[0], player.card_deck[x][y]
                                game.discard_pile[0].visible = True
                                print(f"Spieler {player.name} hat eine Karte vom Ablagestapel genommen! An Stelle:  {[x,y]}")
                                player.is_active = False        # Spieler hat seinen Zug gemacht, ist nicht mehr am Zug
                                final_phase, player_name = game.check_final_phase()  # ist Spiel jetzt in Endphase?

                                if final_phase:
                                    # Wenn Spiel in Endphase:
                                    # Spieler merken, muss am Schluss am wenigsten Punkte haben, sonst Punkteverdopplung
                                    game.first_all_flipped_player = player_name
                                    game.final_phase = True
                                else:
                                    game.final_phase = False               # Überprüfen ob Spiel in der Endphase ist nun
                                if game.final_phase:
                                    game.draw_counter -= 1                 # Wenn Spiel in Endphase Zugcounter reduzieren

                                next_index = (index + 1) % len(game.player_list)
                                game.player_list[next_index].is_active = True    # nächsten Spieler zum Zug berechtigen

            elif "Check Draw Pile" in client_message[3]:

                if check_for_permission(game_dict,client_message[1],client_message[2],"Check Draw Pile"):
                    # Nur ausführen bei Berechtigung:

                    game = game_dict.get(client_message[2])
                    game.draw_pile[0].visible = True    # Nachziehstapel aufdecken
                    print(f"{client_message[1]} hat den Nachziehstapel aufgedeckt!")

            elif "Take from Draw Pile" in client_message[3]:

                x,y = client_message[3].get("Take from Draw Pile")   # Die Koordinaten der Zielkarte im Kartendeck

                if check_for_permission(game_dict,client_message[1],client_message[2],"Take from Draw Pile"):
                    # Nur ausführen bei Berechtigung:
                    game = game_dict.get(client_message[2])
                    for index,player in enumerate(game.player_list):

                        if player.name == client_message[1]:
                            # Ausführen falls Karte existiert_
                            if player.card_deck[x][y]:
                                player.card_deck[x][y].visible = True             # Karte im Kartendeck aufdecken
                                game.discard_pile[0] = player.card_deck[x][y]     # Auf den Ablagestapel legen
                                player.card_deck[x][y] = game.draw_pile.pop(0)    # Karte vom Nachziehstapel ins Kartendeck nehmen
                                print(f"Spieler {player.name} hat eine Karte vom Nachziehstapel genommen! An Stelle:  {[x,y]}")
                                player.is_active = False   # Spieler hat seinen Zug gemacht, ist nicht mehr am Zug
                                final_phase, player_name = game.check_final_phase()

                                if final_phase:
                                    # Wenn Spiel in Endphase:
                                    # Spieler merken, muss am Schluss am wenigsten Punkte haben, sonst Punkteverdopplung
                                    game.first_all_flipped_player = player_name
                                    game.final_phase = True
                                else:
                                    game.final_phase = False
                                if game.final_phase:
                                    game.draw_counter -= 1

                                next_index = (index + 1) % len(game.player_list)
                                game.player_list[next_index].is_active = True    # nächsten Spieler zum Zug berechtigen

            elif "Flip Card" in client_message[3]:

                x,y = client_message[3].get("Flip Card")     # Koordinaten der Zielkarte

                if check_for_permission(game_dict,client_message[1],client_message[2],"Flip Card"):
                    # Nur ausführen bei Berechtigung:
                    game = game_dict.get(client_message[2])
                    for index,player in enumerate(game.player_list):

                        if player.name == client_message[1]:
                            # Ausführen wenn Karte existiert:
                            if player.card_deck[x][y]:
                                if not player.card_deck[x][y].visible: 
                                    player.card_deck[x][y].visible = True   # Karte umdrehen wenn sie noch verdeckt ist

                                    if player.is_active:
                                        # Nur ausführen während normalen Zügen (nicht bei Rundenbeginn!)
                                        game.discard_pile.insert(0,game.draw_pile.pop(0))
                                        print(f"{player.name} hat eine Karte umgedreht! An Stelle: {[x,y]}")
                                        player.is_active = False   # Spieler hat seinen Zug gemacht, ist nicht mehr am Zug

                                        final_phase, player_name = game.check_final_phase()
                                        if final_phase:
                                            # Wenn Spiel in Endphase:
                                            # Spieler merken, muss am Schluss am wenigsten Punkte haben, sonst Punkteverdopplung
                                            game.first_all_flipped_player = player_name
                                            game.final_phase = True
                                        else:
                                            game.final_phase = False    # Überprüfen ob Spiel nun in der Endphase ist
                                        if game.final_phase:
                                            game.draw_counter -= 1     # Wenn Spiel in Endphase Zugcounter reduzieren

                                        next_index = (index + 1) % len(game.player_list)
                                        game.player_list[next_index].is_active = True

            elif "Leave Game" in client_message[3]:
                
                game = game_dict.get(client_message[2])
                if game.end_scores:
                # Man kann das Spiel verlassen wenn es vorbei ist:
                    for player in game.player_list:
                        if player.name == client_message[1]:
                            print(f"{player.name} hat das Spiel ordentlich verlassen")
                            game.player_list.remove(player)    # Spieler aus Spielerliste entfernen
                            game.player_counter -= 1           # Spielerzähler reduzieren

            elif "End Game" in client_message[3]:
                
                game = game_dict.get(client_message[2])
                for player in game.player_list:
                    if player.name == client_message[1] and player.is_admin:
                    # Spiel kann nur beendet werden vom Admin
                        print(f"Admin {player.name} hat das Spiel geschlossen")
                        game.closed = True   # wird gesetzt, damit es in clean_up_games() entfernt wird

def clean_up_games(game_dict):   # entfernt geschlossene Spiele, Spieler die gegangen sind und leere Spiele

    games_to_remove = []

    for game_name, game in game_dict.items():
        if game.closed or (game.end_scores and game.player_counter == 0):
            # Spiel entfernen falls es beendet wurde oder zu Ende ist und alle das Spiel verlassen haben 
            games_to_remove.append(game_name)

    for name in games_to_remove:
        print(f"Spiel '{name}' wird entfernt (geschlossen oder leer).")
        del game_dict[name]     # Spiel aus game_dict entfernen

    for game in game_dict.values():
        # Spieler entfernen die das Spiel verlassen haben
        game.player_list[:] = [player for player in game.player_list if not getattr(player, "left", False)]

def update_game_state(game,card_set):  # updatet den Spielzustand nachdem Clientbefehle abgearbeitet wurden
    
    if game.running:      # nur wenn das Spiel läuft ausführen:

        game.remove_triplets()           # Drillinge entfernen
        game.refresh_round_scores()      # Rundenscores aktualisieren

        if game.draw_counter == 0:       # Bedeutet = Runde Vorbei, Endauswertung machen

            game.refresh_total_player_scores()   # Gesamtpunktzahl aktualisieren
            game.round += 1                      # Nächste Runde starten
            game.final_phase = False             # Final Phase zurücksetzen
            game.draw_counter = game.max_players # Draw Counter zurücksetzen
            game.active_player = None            # Kein aktiver Spieler
             
            game.shuffle_cards(card_set)         # Karten mischen
            game.check_game_over()               # überprüfen ob Spiel vorbei, falls ja game.running auf False setzen

            for player in game.player_list:      # kein Spieler ist am Zug
                player.is_active = False
            
        game.active_player = game.check_for_active_player()    # nach aktivem Spieler suchen
        round_starter = game.select_round_starter()            # Spieler der die Runde startet suchen

        if not game.active_player:                             # Wenn es keinen aktiven Spieler gibt aber einen Rundenstarter
            if round_starter:                                  # dann Rundenstarter zum aktiven Spieler machen
                game.active_player = round_starter
                for player in game.player_list:
                    if player.name == round_starter:
                        player.is_active = True
        

def start_game(game,cardset):      # startet eine neue Runde, setzt Startvariablen
    
    game.shuffle_cards(cardset)    # Karten mischen
    print("Karten wurden gemischelt")
    game.running = True

    ### Für Debugging (Rundenübergangslogik) ###

    if game.name == "D R O" and game.round == 1:
        
        for column in range(3):
            for row in range(3): 
                game.player_list[0].card_deck[column][row].visible = True
        
        game.player_list[0].card_deck[0][3].visible = True
        game.player_list[0].card_deck[1][3].visible = True

        for column in range(3):
            for row in range(3): 
                game.player_list[1].card_deck[column][row].visible = True
        
        game.player_list[1].card_deck[0][3].visible = True
        game.player_list[1].card_deck[1][3].visible = True

        game.player_list[0].is_active = True

    ######

def is_lobby_ready(game):  # überprüft ob alle Spieler da sind

    if game.max_players == game.player_counter:  # sind alle Spieler da?

        if not game.check_for_active_player() and not game.running and not game.end_scores: 
            return True
        else:
            return False
    else: 
        return False

def check_for_permission(game_dict, playername, gamename, player_order):

    can_make_move = False
    client_game = None
    client_player = None

    # Spiel und Spieler suchen
    client_game = game_dict.get(gamename)
    for player in client_game.player_list:
        if player.name == playername:
            client_player = player
            can_make_move = player.is_active

    # SCHUTZ: Wenn Spiel oder Spieler nicht mehr existieren (z. B. gelöscht)
    if client_game is None or client_player is None:
        print(f"Befehl von {playername} nicht ausgeführt, Spieler oder Spiel existiert nicht mehr")
        return False

    # SCHUTZ: Falls Spiel bereits geschlossen wurde
    if getattr(client_game, "closed", False):
        print(f"Spiel ({gamename}) ist geschlossen. Keine Aktionen mehr erlaubt.")
        return False

    # Erlaubt Rundenstart mit weniger als zwei aufgedeckten Karten, auch wenn kein Spieler aktiv ist
    if not client_game.check_for_active_player() and client_player.check_flipped_cards() < 2:
        round_start = True
    else:
        round_start = False

    permission = False

    ### Berechtigungslogik: ###

    if can_make_move or round_start:
        if player_order == "Take from Discard Pile" and client_game.discard_pile[0]:
            if not round_start:
                permission = True
        elif player_order == "Check Draw Pile":
            if not round_start:
                permission = True
        elif player_order == "Take from Draw Pile" and client_game.draw_pile[0].visible:
            if not round_start:
                permission = True
        elif player_order == "Flip Card" and (client_game.draw_pile[0].visible or round_start):
            permission = True

    if permission:
        print(f"{playername} hat die Erlaubnis, {player_order} auszuführen.")
    else:
        print(f"{playername} darf {player_order} nicht ausführen (verweigert).")

    return permission



