import random
from .card import Card

class Player:
    def __init__(self, name):

        self.ip_addr = ""
        self.name = name
        self.is_online = False
        self.round_score = 0
        self.visible_round_score = 0
        self.total_score = 0
        self.card_deck = []
        self.is_active = False
        self.is_admin = False

    """
    def flip_card(self, row, col):
        #Deckt eine Karte auf
        if 0 <= row < 4 and 0 <= col < 3:
            self.card_deck[row][col]['flipped'] = True

    def remove_card(self, row, col):
        #Entfernt eine Karte aus dem Deck (setzt sie auf None)
        if 0 <= row < 4 and 0 <= col < 3:
            self.card_deck[row][col] = {'value': None, 'flipped': False}

    def add_card(self, row, col, value):
        #Fügt eine Karte mit Wert value an Position (row, col) hinzu
        if 0 <= row < 4 and 0 <= col < 3:
            self.card_deck[row][col] = {'value': value, 'flipped': False}

    """
    def check_flipped_cards(self):
    
        # Gibt zurück wie viele Karten der Spieler aufgedeckt hat

        flipped_cards = 0
        for row in self.card_deck:
            for card in row:
                if card.visible:
                    flipped_cards += 1

        return flipped_cards
    

    def count_card_sum(self):

        # Zählt die Punktzahl des Spielers (nicht sichtbare Karten mit eingeschlossen, für Server!)

        sum = 0
        for row in self.card_deck:
            for card in row:
                sum += card.value
        return sum
    
    def count_visible_card_sum(self):

        # Zählt die Punktzahl des Spielers (nur sichtbare Karten, für Client!)

        sum = 0
        for row in self.card_deck:
            for card in row:
                if card.visible:
                    sum += card.value
        return sum

    def check_for_triplets(self):
        
        # Gibt bei dem Spieler eine Liste mit Spalten zurück in denen 3 gleiche Karten aufgedeckt sind
        # so dass diese entfernt werden können

        triplets_found_in_column = []
        for i in range(4):

            column_cards = [self.card_deck[row][i] for row in range(3)]

            if any(card is None for card in column_cards):     # Nicht ausführen für Spalten in denen keine Karten sind! Sonst AttributeError
                continue

            values = [card.value for card in column_cards]
            visibility = [card.visible for card in column_cards]

            if len(set(values)) == 1 and all(visibility) == True:
                triplets_found_in_column.append(i)

        return triplets_found_in_column
    
    def initialize_card_deck(self):

        for i in range(3):
            row = [Card(0,colour = None, visible = True) for _ in range(4)]
            self.card_deck.append(row)

    """
    def check_for_all_flipped(self):
        Überprüft, ob alle Karten aufgedeckt sind.
        for row in self.card_deck:
            for card in row:
                if not card['flipped']:
                    return False
        return True
    
    def enter_lobby(self):
        self.is_online = True

    def leave_lobby(self):
        self.is_online = False

    def initialize_deck(self, card_values):
        #Initialisiert das Deck mit einer Liste von 12 Kartenwerten.
        if len(card_values) != 12:
            raise ValueError("Es werden genau 12 Kartenwerte benötigt.")
        idx = 0
        for row in range(4):
            for col in range(3):
                self.card_deck[row][col] = {'value': card_values[idx], 'flipped': False}
                idx += 1
    """