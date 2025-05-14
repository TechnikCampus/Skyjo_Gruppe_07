##### GUI Functions and Classes for the client #####

def get_Player_Input():      # Funktion die ausliest ob der Spieler etwas angeklickt hat was eine Aktion auslöst
                             # Interpretation dieser Daten serverseitig
    
    # Hier Ausleselogik einfügen, diese füllt folgende Variablen:

    take_from_discard_pile = True    # wird True gesetzt wenn Spieler auf den Ablagestapel geklickt hat
    accept_card = True               # wird True gesetzt wenn Spieler auf Accept geklickt hat, nachdem ihm die Karte
                                     # vom Ablagestapel gezeigt wurde
    choose_card = [0,0]              # "Koordinaten" der Karte auf die der Spieler geklickt hat

    return [take_from_discard_pile,accept_card,choose_card]






