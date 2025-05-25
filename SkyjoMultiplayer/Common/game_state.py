import random
from .card import Card

"""
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.round_score = 0
        self.total_score = 0
        self.flipped_cards = 0  # Anzahl aufgedeckter Karten

    def flip_card(self):
        self.flipped_cards += 1

    def reset_for_new_round(self):
        self.cards = []
        self.round_score = 0
        self.flipped_cards = 0
"""

class Game_state:

    def __init__(self,name,maxplayers):        # beim Start eines Spiels den Namen und die max. Spieleranzahl festlegen

        self.running = False
        self.name = name
        self.round = 1
        self.player_counter = 0
        self.max_players = maxplayers
        self.draw_counter = maxplayers
        self.final_phase = False
        self.active_player = None
        self.player_list = []
        self.discard_pile = []        # wichtig: discard_pile[0]: obere aufgedeckte Karte
        self.draw_pile = []           # wichtig: draw_pile[0]: oberste Karte des Stapels
        self.first_all_flipped_player = None

    def shuffle_cards(self, card_set):

        random.shuffle(card_set)  # das festgelegte Kartenset mit 150 Spielkarten mischeln
    
        for player in self.player_list:    # jedem Spieler zufällige Karten verteilen(4 Spalten, 3 Zeilen)

            player.card_deck.clear()  # das bei Serverbeitritt initialisierte Kartendeck mit Platzhaltern löschen
            for _ in range(3):  
                row = []
                for _ in range(4):  
                    card = card_set.pop(0)  
                    row.append(Card(value=card, colour=None))
                player.card_deck.append(row)
            
        self.discard_pile = [Card(value=card_set.pop(0),colour=None,visible=True)]   # eine Karte auf den Ablagestapel (aufgedeckt)
        self.draw_pile = [Card(value=value, colour=None) for value in card_set]      # restlichen Karten verdeckt auf den Nachziehstapel

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
        # round_score wieder zu 0 setzen für nächste Runde (Standardwert
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
        # oder die Rundenzahl ist = 11

        max_score = max(player.total_score for player in self.player_list)
        if max_score >= 100 or self.round >= 11:

            self.running = False
            print("Spiel vorbei!")
            return True
        else: 
            return False


    def check_final_phase(self):

        # Endphase der Runde startet, wenn alle Karten eines Spielers aufgedeckt sind
        # Falls ein Spieler alle aufgedeckt hat, Namen des Spielers mit zurückgeben

        for player in self.player_list:
            if all(card.visible for card in player.card_deck):
                return (True,player.name)
        return False


    def check_for_active_player(self):
        
        # Sucht den Namen des Spielers der am Zug ist

        active_player = None
        for player in self.player_list:
            if player.is_active == True:
                active_player = player.name
        return active_player
    
    def select_round_starter(self):

        if not self.active_player:
            player_flipped_cards = [player.check_flipped_cards() for player in self.player_list]
            if all(flipped == 2 for flipped in player_flipped_cards):
                max_card_sum = max([player.count_visible_card_sum() for player in self.player_list])
                for player in self.player_list:
                    if player.count_visible_card_sum() == max_card_sum:
                        return player.name
            else:
                return None
        return None

    
    """

    def check_for_two_cards_flipped(self):
        # Alle Spieler müssen zu Beginn 2 Karten aufgedeckt haben
        return all(player.flipped_cards >= 2 for player in self.player_list)

    
    def select_active_player(self):
        # Nächster Spieler in der Liste, der noch Karten hat
        if not self.player_list:
            self.active_player = None
            return
        if self.active_player is None:
            self.active_player = self.player_list[0]
        else:
            idx = self.player_list.index(self.active_player)
            self.active_player = self.player_list[(idx + 1) % len(self.player_list)]
    

    def make_player_move(self, move):
        # move: dict mit z.B. {'action': 'draw', 'from': 'draw_pile'}
        if self.active_player is None:
            return False
        if move['action'] == 'draw':
            if move['from'] == 'draw_pile' and self.draw_pile:
                card = self.draw_pile.pop()
                self.active_player.cards.append(card)
            elif move['from'] == 'discard_pile' and self.discard_pile:
                card = self.discard_pile.pop()
                self.active_player.cards.append(card)
            else:
                return False
            self.draw_counter += 1
            return True
        elif move['action'] == 'flip':
            self.active_player.flip_card()
            return True
        return False                          
    

    def start_new_round(self):
        self.round += 1
        self.shuffle_cards()
        for player in self.player_list:
            player.reset_for_new_round()
            # Jeder Spieler bekommt z.B. 12 Karten
            player.cards = [self.draw_pile.pop() for _ in range(12)]
        # Erste Karte auf den Ablagestapel
        self.discard_pile.append(self.draw_pile.pop())
        self.active_player = self.player_list[0] if self.player_list else None
        self.draw_counter = 0
        
    """
