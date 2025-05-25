##### Game logic functions on the server #####

def update_game_state(game,card_set):  # updatet den Spielzustand
    
    game.remove_triplets()
    game.refresh_round_scores()

    if game.draw_counter == 0:

        game.refresh_total_player_score()
        game.round += 1
        game.final_phase = False
        game.draw_counter = game.max_players
        game.active_player = game.first_all_flipped_player

        for player in game.player_list:
            if player.name == game.first_all_flipped_player:
                player.is_active = True
            else: 
                player.is_active = False
        
        game.active_player = game.check_for_active_player()
        
        game.shuffle_cards(card_set)
        game.check_game_over()

        # game.running wird auf False gesetzt in check_game_over, hat momentan keinen Effekt!


def start_game(game,cardset):      # startet ein neues Spiel, setzt Startvariablen
    
    game.shuffle_cards(cardset)    # Karten mischen
    print("Karten wurden gemischelt")
    game.running = True


def is_lobby_ready(game):

    # Funktion soll prüfen ob das Spiel gestartet werden kann!
    # wenn Spiel schon läuft soll False zurückgegeben werden!

    if game.max_players == game.player_counter:

        if not game.check_for_active_player() and not game.running:
            return True
        else:
            return False
    else: 
        return False

def check_for_permission(gamelist,playername,gamename,player_order):

    can_make_move = False
    client_game = None
    client_player = None

    # Überprüfen ob der Spieler am Zug ist:

    for game in gamelist:
        if game.name == gamename:
            client_game = game
            for player in game.player_list:
                if player.name == playername:
                    client_player = player
                    if player.is_active:
                        can_make_move = True
                    else:
                        can_make_move = False

    # Falls ja: Prüfen ob der Spielzustand den Zug erlaubt:

    # Und:
    # Überprüfen ob gerade der Start der ersten Runde ist:
    # (kein Spieler am Zug und Spieler hat weniger als zwei Karten aufgedeckt)

    if not client_game.check_for_active_player() and client_player.check_flipped_cards < 2:    
        round_start = True
    else:
        round_start = False

    permission = False

    if can_make_move:

        # Vom Ablagestapel nehmen nicht erlaubt wenn Nachziehstapel aufgedeckt:
        if player_order == "Take from Discard Pile" and not client_game.draw_pile[0].visible and client_game.discard_pile[0]:
            if not round_start:
                permission = True

        # Nachziehstapel kann immer angeguckt werden wenn man am Zug ist
        elif player_order == "Check Draw Pile":
            if not round_start:
                permission = True

        # Man kann nur vom Nachziehstapel nehmen wenn man diesen aufgedeckt hat
        elif player_order == "Take from Draw Pile" and client_game.draw_pile[0].visible:
            if not round_start:
                permission = True

        # Man kann nur eine Karte umdrehen wenn man den Nachziehstapel aufgedeckt hat,
        # oder zu Rundenbeginn

        elif player_order == "Flip Card" and (client_game.draw_pile[0].visible or round_start):
            permission = True

    if permission:
        print(f"{playername} hat die Erlaubnis das zu tun!")
    else:
        print(f"Zug von {playername} wurde vom Server verweigert!")

    return permission



