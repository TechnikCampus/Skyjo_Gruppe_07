##### Game logic functions on the server #####

def clean_up_games(game_list):   # entfernt geschlossene Spiel, Spieler die gegangen sind, und leere Spiele

    game_list[:] = [game for game in game_list if not (getattr(game, "closed", False) or (game.end_scores and game.player_counter == 0))]

    for game in game_list:

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

            for player in game.player_list:      # jeder Spieler ist nicht am Zug
                player.is_active = False
            
        game.active_player = game.check_for_active_player()    # nach aktivem Spieler suchen
        round_starter = game.select_round_starter()            # Spieler der die Runde startet suchen (nur wenn es Sinn ergibt)

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

    if game.name == "D R O" and game.round == 1:     # steht für "Debug Round Over", setzt Spielzustand für einfaches debuggen
        
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

        # Alle Karten bis auf eine aufdecken für einfachen Rundenübergangstest


def is_lobby_ready(game):

    # Funktion soll prüfen ob das Spiel gestartet werden kann!
    # wenn Spiel schon läuft soll False zurückgegeben werden!

    if game.max_players == game.player_counter:

        if not game.check_for_active_player() and not game.running and not game.end_scores:
            return True
        else:
            return False
    else: 
        return False

def check_for_permission(gamelist, playername, gamename, player_order):

    can_make_move = False
    client_game = None
    client_player = None

    # Spiel und Spieler suchen
    for game in gamelist:
        if game.name == gamename:
            client_game = game
            for player in game.player_list:
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

    if can_make_move or round_start:
        if player_order == "Take from Discard Pile" and not client_game.draw_pile[0].visible and client_game.discard_pile[0]:
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



