##### Game logic functions on the server #####


def update_game_state(game):  # updatet den Spielzustand
    pass

    # Hier gehört hin:

    # refresh_round_scores()
    # refresh_total_player_scores()
    # check_game_over()
    # check_round_over() und start_new_round()
    # check_for_two_cards_flipped()


def start_game(game):   # startet ein neues Spiel, setzt Startvariablen
    pass

    # Hier gehört hin:

    # Shuffle_cards()
    # start_new_round()


def is_lobby_ready(game):

    # Funktion soll prüfen ob das Spiel gestartet werden kann!
    # wenn Spiel schon läuft soll False zurückgegeben werden!

    if game.max_players == game.player_counter:

        if not game.check_for_active_player():
            return True
        else:
            return False
    else: 
        return False 


