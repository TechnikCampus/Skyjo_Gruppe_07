import random

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

    def __init__(self):
        self.name = ""
        self.round = 0
        self.player_counter = 0
        self.draw_counter = 0
        self.final_phase = False
        self.active_player = None
        self.player_list = []
        self.discard_pile = []
        self.draw_pile = []

    def shuffle_cards(self):
        # Beispiel-Kartendeck: Zahlen von -2 bis 12, mehrfach vorhanden
        deck = [-2, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] * 8
        random.shuffle(deck)
        self.draw_pile = deck
        self.discard_pile = []

    def refresh_round_scores(self):
        for player in self.player_list:
            player.round_score = sum(card for card in player.cards if card is not None)

    def refresh_total_player_scores(self):
        for player in self.player_list:
            player.total_score += player.round_score

    def check_game_over(self):
        # Spielende: Ein Spieler hat >= 100 Punkte
        for player in self.player_list:
            if player.total_score >= 100:
                return True
        return False

    def check_round_over(self):
        # Runde vorbei, wenn alle Karten eines Spielers aufgedeckt sind
        for player in self.player_list:
            if player.flipped_cards == len(player.cards):
                return True
        return False

    def check_for_active_player(self):
        return self.active_player is not None

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
