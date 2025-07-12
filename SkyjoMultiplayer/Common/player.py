import random
from .card import Card

class Player:
    def __init__(self, name):

        self.ip_addr = ""                 # IPv4 des Spielers
        self.name = name
        self.is_online = False            # ist der Spieler online?
        self.round_score = 0              # Rundenpunktzahl (mit verdeckten Karten)
        self.visible_round_score = 0      # für den Spieler sichtbare Rundenpunktzahl
        self.total_score = 0              # Spielergesamtpunktzahl
        self.card_deck = []               # Spielerkartendeck
        self.is_active = False            # ist der Spieler am Zug?
        self.is_admin = False             # ist der Spieler ein Admin?
        self.left = False                 # Spieler wird aus der Spielerliste entfernt wenn hier True gesetzt wird

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
                if card:
                    sum += card.value
        return sum
    
    def count_visible_card_sum(self):

        # Zählt die Punktzahl des Spielers (nur sichtbare Karten, für Client!)

        sum = 0
        for row in self.card_deck:
            for card in row:
                if card:
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

        # Füllt Kartendeck mit Platzhaltern solange die Runde noch nicht gestartet hat
        # weil noch auf Spieler gewartet wird

        for i in range(3):
            row = [Card(0,colour = None, visible = True) for _ in range(4)]
            self.card_deck.append(row)
