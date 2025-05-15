##### Player Class #####

class Player():

    def __init__(self,name):

        self.ip_addr = ""
        self.name = name           # Der Name dieses Spielers
        self.is_online = False  # speichert ob der Spieler Online ist
        self.round_score = 0        # Rundenpunktzahl des Spielers
        self.total_score = 0     # Gesamtpunktzahl des Spielers
        self.card_deck = []     # Kartendeck des Spielers als 4 x 3 Liste
        self.is_active = False        # Ist der Spieler am Zug?
        self.is_admin = False         # ist der Spieler ein Admin? Admins haben Sonderrechte

    def flip_card(self):    # deckt eine Karte auf
        pass

    def remove_card(self):  # entfernt eine Karte vom Kartendeck
        pass

    def add_card(self):     # fügt eine Karte hinzu ins Kartendeck
        pass

    def count_card_sum(self):   # zählt die Summe aller Karten
        pass

    def check_for_triplets(self):   # Sonderregel: Überprüfen auf Drillinge
        pass

    def check_for_all_flipped(self):   # überprüft ob alle Karten aufgedeckt sind
        pass

    def enter_lobby(self):     # betreten der Lobby
        pass

    def leave_lobby(self):     # verlassen der Lobby
        pass

