# Card class
import os

BILDER_PFAD = os.path.join(os.path.dirname(__file__), "Karten_png")

def get_image_path(value):
    """Erzeugt den Bildpfad für eine Karte."""
    filename = f"card_{value}.png"
    return os.path.join(BILDER_PFAD, filename)

class Card:
    def __init__(self, value, colour, visible=False, sizeX=100, sizeY=150):
        """
        Initialisiert eine Karte mit den angegebenen Eigenschaften.

        :param value: Zahlenwert der Karte (z. B. -2, 0, 5, 12)
        :param colour: Farbe der Karte (z. B. "red", "blue", "green")
        :param visible: Gibt an, ob die Karte aufgedeckt ist (Standard: False)
        :param sizeX: Breite der Karte für die GUI (Standard: 100)
        :param sizeY: Höhe der Karte für die GUI (Standard: 150)
        """
        self.value = value
        self.colour = colour
        self.visible = visible
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.image_path = None  # Bildpfad-Attribut

    def flip(self):
        """Deckt die Karte auf oder verdeckt sie."""
        self.visible = not self.visible

    def set_image(self, image_path):
        """Setzt den Bildpfad der Karte."""
        self.image_path = image_path

    def set_image_from_file(self):
        """Setzt das Bild automatisch anhand von value."""
        path = get_image_path(self.value)
        if os.path.exists(path):
            self.image_path = path
        else:
            self.image_path = None  # Oder ein Standardbild

    def get_image(self):
        """Gibt den Pfad zum Bild der Karte zurück."""
        return self.image_path

    def get_value(self):
        """Gibt den Wert der Karte zurück."""
        return self.value

    def get_colour(self):
        """Gibt die Farbe der Karte zurück."""
        return self.colour

    def get_visible(self):
        """Gibt zurück, ob die Karte sichtbar ist oder nicht."""
        return self.visible

    def get_sizeX(self):
        """Gibt die Breite der Karte zurück."""
        return self.sizeX

    def get_sizeY(self):
        """Gibt die Höhe der Karte zurück."""
        return self.sizeY

    def __str__(self):
        """Gibt eine lesbare Darstellung der Karte zurück."""
        return f"Card(value={self.value}, colour={self.colour}, visible={self.visible})"

    def __repr__(self):
        """Gibt eine technische Darstellung der Karte zurück."""
        return self.__str__()