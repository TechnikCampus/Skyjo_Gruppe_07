import random
from .card import Card

class Game_state:

    def __init__(self,name,maxplayers):        # beim Start eines Spiels den Namen und die max. Spieleranzahl festlegen

        self.running = False                   # läuft das Spiel?
        self.name = name          
        self.round = 1
        self.player_counter = 0                # Spielerzähler
        self.max_players = maxplayers
        self.draw_counter = maxplayers         # Zugcounter (für Endphase)
        self.final_phase = False               # Ist das Spiel in der Endphase?
        self.active_player = None              # Name des Spielers am Zug
        self.player_list = []                  # Spielerliste
        self.discard_pile = []                 # wichtig: discard_pile[0]: obere aufgedeckte Karte
        self.draw_pile = []                    # wichtig: draw_pile[0]: oberste Karte des Stapels
        self.first_all_flipped_player = None   # Name des Spielers der zuerst alle Karten aufgedeckt hat
        self.end_scores = []                   # Endspielstand
        self.closed = False                    # Wenn hier True gesetzt wird wird das Spiel entfernt in clean_up_games()

    def shuffle_cards(self, card_set):

        card_set_copy = card_set.copy()

        random.shuffle(card_set_copy)  # das festgelegte Kartenset mit 150 Spielkarten mischeln
    
        for player in self.player_list:    # jedem Spieler zufällige Karten verteilen(4 Spalten, 3 Zeilen)

            player.card_deck.clear()  # das bei Serverbeitritt initialisierte Kartendeck mit Platzhaltern löschen

            for _ in range(3):  # die Kartendecks aller Spieler mit den gemischelten Karten füllen
                row = []
                for _ in range(4):  
                    card = card_set_copy.pop(0)  
                    row.append(Card(value=card, colour=None))
                player.card_deck.append(row)
            
        self.discard_pile = [Card(value=card_set_copy.pop(0),colour=None,visible=True)]   # eine Karte auf den Ablagestapel (aufgedeckt)
        self.draw_pile = [Card(value=value, colour=None) for value in card_set_copy]      # restlichen Karten verdeckt auf den Nachziehstapel

    def remove_triplets(self):

        # Bei jedem Spieler alle aufgedeckten Drillinge entfernen

        for player in self.player_list:
            if player.check_for_triplets():
                for column in player.check_for_triplets():
                    for i in range(3):
                        player.card_deck[i][column] = None

                print(f"Bei Spieler {player.name} wurden Drillinge entfernt!")

    def refresh_round_scores(self):

        # Sichtbare (für Client) und insgesamte (für Server) Spielerpunktzahl updaten

        for player in self.player_list:
            player.round_score = player.count_card_sum()
            player.visible_round_score = player.count_visible_card_sum()


    def refresh_total_player_scores(self):

        # Am Ende der Runde: Spielerpunktzahlen zu Gesamtpunktzahl dazu addieren,
        # round_score wieder zu 0 setzen für nächste Runde (Standardwert)
        # first_all_flipped_player: Der Spieler der zuerst alle Karten aufgedeckt hat
        # wenn dieser nicht den niedrigsten Rundenscore hat -> Punktzahl verdoppeln

        lowest_round_score = min([player.round_score for player in self.player_list])

        for player in self.player_list:

            if player.name == self.first_all_flipped_player and player.round_score != lowest_round_score:
                player.total_score += (2 * player.round_score)
            else: player.total_score += player.round_score

            player.round_score = 0


    def check_game_over(self):

        # Spielende: Ein Spieler hat >= 100 Punkte

        max_score = max(player.total_score for player in self.player_list)
        if max_score >= 100:

            for player in self.player_list:
                self.end_scores.append((player.name,player.total_score))   # Endspielstand definieren

            self.running = False
            print("Spiel vorbei!")


    def check_final_phase(self):

        # Endphase der Runde startet, wenn alle Karten eines Spielers aufgedeckt oder entfernt sind
        # Falls ein Spieler alle aufgedeckt hat, Namen des Spielers mit zurückgeben

        for player in self.player_list:
            if all((card is None or card.visible) for row in player.card_deck for card in row):
                return (True,player.name)
        return False,"None"      # "None" dazuschreiben da ansonsten ein Fehler in server.py entsteht

    def check_for_active_player(self):
        
        # Sucht den Namen des Spielers der am Zug ist

        active_player = None
        for player in self.player_list:
            if player.is_active == True:
                active_player = player.name
        return active_player
    
    def select_round_starter(self):

        # Spieler suchen der die Runde startet

        if not self.active_player:
            # Nur wenn kein Spieler am Zug ist 
            player_flipped_cards = [player.check_flipped_cards() for player in self.player_list]
            if all(flipped == 2 for flipped in player_flipped_cards):
                # Ausführen wenn alle Spieler zwei Karten aufgdeckt haben:
                max_card_sum = max([player.count_visible_card_sum() for player in self.player_list])
                for player in self.player_list:
                    if player.count_visible_card_sum() == max_card_sum:  # den Spieler mit der höchsten Kartensumme suchen
                        return player.name
            else:
                return None
        return None

