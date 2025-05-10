##### Game State class and Functions #####

class Game_state():

    def __init__(self):
        
        self.round          # speichert die derzeitige Runde
        self.draw_counter   # Zugcounter, siehe Struktogramm
        self.final_phase    # Ist das Spiel in der Endphase?
        self.next_player

    def shuffle_cards(self):   # benutzt Random zum Mischen der Karten
        pass

    def refresh_round_scores(self):  # Rundenpunktzahl aller Spieler aktualisieren
        pass

    def refresh_total_player_scores(self):   # Gesamtpunktzahl der Spieler aktualisieren
        pass

    def check_game_over(self):   # überprüfen ob das Spiel vorbei ist, round = 11? oder hat ein Spieler >100 Punkte?
        pass

    def check_round_over(self):   # überprüfen ob die Runde vorbei ist? draw_counter = 0?
        pass

    def check_for_active_player(self):   # ist ein Spieler am Zug?
        pass

    def check_for_two_cards_flipped(self):    # überprüft ob alle Spieler zwei Karten aufgedeckt haben zu Rundenbeginn
        pass 

    def select_active_player(self):   # den nächsten Spieler festlegen der am Zug ist, auch zu Beginn des Spiels
        pass

    def analyse_player_move(self):    # analysiert/überprüft was der aktive Spieler machen will und führt das aus wenn erlaubt
        pass

    def start_new_round(self):
        pass






