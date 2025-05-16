# Card-Klasse mit eingebetteten Bildern
import base64  # Erforderlich für das Kodieren und Dekodieren von Bildern
from io import BytesIO  # Erforderlich für die Verarbeitung von Bilddaten
try:
    from PIL import Image  # Sicherstellen, dass PIL installiert und verfügbar ist
except ImportError:
    raise ImportError("Pillow-Bibliothek ist nicht installiert. Bitte installieren Sie sie mit 'pip install pillow'.")  # Fehlerhinweis, wenn Pillow nicht installiert ist
import os

CARD_IMAGE_MAPPING = {  # Zuordnung von Kartenwerten zu Bilddateinamen
    -2: "card_-2.png",  # Bilddatei für Karte -2
    -1: "card_-1.png",  # Bilddatei für Karte -1
    0: "card_0.png",  # Bilddatei für Karte 0
    1: "card_1.png",  # Bilddatei für Karte 1
    2: "card_2.png",  # Bilddatei für Karte 2
    3: "card_3.png",  # Bilddatei für Karte 3
    4: "card_4.png",  # Bilddatei für Karte 4
    5: "card_5.png",  # Bilddatei für Karte 5
    6: "card_6.png",  # Bilddatei für Karte 6
    7: "card_7.png",  # Bilddatei für Karte 7
    8: "card_8.png",  # Bilddatei für Karte 8
    9: "card_9.png",  # Bilddatei für Karte 9
    10: "card_10.png",  # Bilddatei für Karte 10
    11: "card_11.png",  # Bilddatei für Karte 11
    12: "card_12.png",  # Bilddatei für Karte 12
}

CARD_BACK_IMAGE = "card_back.png"  # Hinzufügen des Kartenrückseitenbildes

CARD_BACK_IMAGE_MAPPING = {  # Zuordnung für das Kartenrückseitenbild
    "back": CARD_BACK_IMAGE  # Kartenrückseite
}

KARTEN_BILDER = {}  # Wörterbuch zum Speichern der Kartenbilder

def load_images_from_folder(folder_path):
    for card_value, file_name in CARD_IMAGE_MAPPING.items():  # Iteration über die Zuordnung
        file_path = os.path.join(folder_path, file_name)  # Erstellen des vollständigen Dateipfads
        if os.path.exists(file_path):  # Überprüfen, ob die Datei existiert
            try:
                with open(file_path, "rb") as image_file:  # Öffnen der Bilddatei
                    base64_string = base64.b64encode(image_file.read()).decode("utf-8")  # Kodieren in Base64
                    KARTEN_BILDER[card_value] = base64_string  # Speichern im Wörterbuch
            except Exception as e:
                print(f"Fehler beim Laden der Bilddatei {file_name}: {e}")  # Fehlerbehandlung
        else:
            print(f"Bilddatei {file_name} für Karte {card_value} nicht gefunden.")  # Hinweis, wenn Datei fehlt

def get_image_from_base64(base64_string):
    image_data = base64.b64decode(base64_string)  # Dekodieren des Base64-Bildes
    return Image.open(BytesIO(image_data))  # Rückgabe als PIL-Image

current_dir = os.path.dirname(os.path.abspath(__file__))  # Aktuelles Verzeichnis
karten_png_path = os.path.join(current_dir, "karten_png")  # Pfad zum Ordner "karten_png"
load_images_from_folder(karten_png_path)  # Laden der Bilder aus dem Ordner

class Card:
    def __init__(self, value, colour, visible=False, sizeX=100, sizeY=150):
        self.value = value  # Zahlenwert der Karte
        self.colour = colour  # Farbe der Karte
        self.visible = visible  # Sichtbarkeit der Karte
        self.sizeX = sizeX  # Breite der Karte
        self.sizeY = sizeY  # Höhe der Karte
        self.image = None  # Bild-Attribut der Karte

    def flip(self):
        self.visible = not self.visible  # Deckt die Karte auf oder verdeckt sie

    def set_image_from_embedded(self):
        base64_string = KARTEN_BILDER.get(self.value)  # Abrufen des Base64-Bildes
        if base64_string:
            self.image = get_image_from_base64(base64_string)  # Setzen des Bild-Attributs
        else:
            self.image = None  # Kein Bild gefunden, Standardwert setzen

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

    def __str__(self):
        return f"Card(value={self.value}, colour={self.colour}, visible={self.visible})"  # Technische Darstellung der Karte
