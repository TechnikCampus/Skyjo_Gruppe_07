class Card:
    def __init__(self, value, colour, visible=False, sizeX=100, sizeY=150):
        self.value = value  # Zahlenwert der Karte
        self.colour = colour  # Farbe der Karte
        self.visible = visible  # Sichtbarkeit der Karte
        self.sizeX = sizeX  # Breite der Karte
        self.sizeY = sizeY  # Höhe der Karte
        self.image = None  # Bild-Attribut der Karte
