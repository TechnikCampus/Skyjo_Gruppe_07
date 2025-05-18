from SkyjoMultiplayer.Common.card import Card

# Erstelle eine Karte mit einem Wert, für den ein Bild existiert
karte = Card(5, "red")
karte.set_image_from_file()

print("Bildpfad:", karte.get_image())

# Prüfe, ob das Bild existiert
import os
if karte.get_image() and os.path.exists(karte.get_image()):
    print("Bild wurde korrekt gefunden und zugeordnet!")
else:
    print("Bild wurde NICHT gefunden oder zugeordnet!")
