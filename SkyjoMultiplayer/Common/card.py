# Card-Klasse mit eingebetteten Bildern
import pygame

CARD_FILE_MAPPING = {  # Zuordnung von Kartenwerten zu Bilddateinamen
    "-2": "card_-2.png",  # Bilddatei für Karte -2
    "-1": "card_-1.png",  # Bilddatei für Karte -1
    "0": "card_0.png",  # Bilddatei für Karte 0
    "1": "card_1.png",  # Bilddatei für Karte 1
    "2": "card_2.png",  # Bilddatei für Karte 2
    "3": "card_3.png",  # Bilddatei für Karte 3
    "4": "card_4.png",  # Bilddatei für Karte 4
    "5": "card_5.png",  # Bilddatei für Karte 5
    "6": "card_6.png",  # Bilddatei für Karte 6
    "7": "card_7.png",  # Bilddatei für Karte 7
    "8": "card_8.png",  # Bilddatei für Karte 8
    "9": "card_9.png",  # Bilddatei für Karte 9
    "10": "card_10.png",  # Bilddatei für Karte 10
    "11": "card_11.png",  # Bilddatei für Karte 11
    "12": "card_12.png",  # Bilddatei für Karte 12
    "back": "card_back.png"  # Bilddatei für Kartenrückseite
}

class Card:
    def __init__(self, value, colour, visible=False, sizeX=100, sizeY=150):
        self.value = value  # Zahlenwert der Karte
        self.colour = colour  # Farbe der Karte
        self.visible = visible  # Sichtbarkeit der Karte
        self.sizeX = sizeX  # Breite der Karte
        self.sizeY = sizeY  # Höhe der Karte

    def get_image(self):
        return self.image  # Gibt das Bild der Karte zurück

    def get_value(self):
        return self.value  # Gibt den Wert der Karte zurück

    def get_colour(self):
        return self.colour  # Gibt die Farbe der Karte zurück

    def get_visible(self):
        return self.visible  # Gibt zurück, ob die Karte sichtbar ist oder nicht

    def get_sizeX(self):
        return self.sizeX  # Gibt die Breite der Karte zurück

    def get_sizeY(self):
        return self.sizeY  # Gibt die Höhe der Karte zurück