import random

class Player:
    def __init__(self, name):
        self.ip_addr = ""
        self.name = name
        self.is_online = False
        self.round_score = 0
        self.total_score = 0
        # Kartendeck: 4 Zeilen, 3 Spalten, jede Karte ist ein Dict mit Wert und Status (aufgedeckt/verdeckt)
        self.card_deck = [[{'value': None, 'flipped': False} for _ in range(3)] for _ in range(4)]
        self.is_active = False
        self.is_admin = False

    def flip_card(self, row, col):
        """Deckt eine Karte auf."""
        if 0 <= row < 4 and 0 <= col < 3:
            self.card_deck[row][col]['flipped'] = True

    def remove_card(self, row, col):
        """Entfernt eine Karte aus dem Deck (setzt sie auf None)."""
        if 0 <= row < 4 and 0 <= col < 3:
            self.card_deck[row][col] = {'value': None, 'flipped': False}

    def add_card(self, row, col, value):
        """Fügt eine Karte mit Wert value an Position (row, col) hinzu."""
        if 0 <= row < 4 and 0 <= col < 3:
            self.card_deck[row][col] = {'value': value, 'flipped': False}

    def count_card_sum(self):
        """Zählt die Summe aller aufgedeckten Karten."""
        total = 0
        for row in self.card_deck:
            for card in row:
                if card['flipped'] and card['value'] is not None:
                    total += card['value']
        return total

    def check_for_triplets(self):
        """Überprüft jede Spalte auf Drillinge (gleicher Wert, alle aufgedeckt)."""
        for col in range(3):
            values = []
            for row in range(4):
                card = self.card_deck[row][col]
                if card['flipped'] and card['value'] is not None:
                    values.append(card['value'])
                else:
                    break
            if len(values) == 4 and all(v == values[0] for v in values):
                return True
        return False

    def check_for_all_flipped(self):
        """Überprüft, ob alle Karten aufgedeckt sind."""
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
        """Initialisiert das Deck mit einer Liste von 12 Kartenwerten."""
        if len(card_values) != 12:
            raise ValueError("Es werden genau 12 Kartenwerte benötigt.")
        idx = 0
        for row in range(4):
            for col in range(3):
                self.card_deck[row][col] = {'value': card_values[idx], 'flipped': False}
                idx += 1
