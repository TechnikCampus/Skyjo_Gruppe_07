# Das hier ist ein Testclient:
# Hier können über eine CLI Benutzeroberfläche dem Server Befehle erteilt werden um
# zu testen ob die Spiellogik richtig funktioniert, es kann also ein "echter" Client (mit einer richitgen GUI) simuliert werden
# (Ist nicht schön geworden, nur für Testzwecke)

import pygame
import Client as clnt
import sys
import threading
import queue

pygame.init()
clock = pygame.time.Clock()

client_name = str(input("Gebe hier deinen Namen ein >> "))

client_game = "NeueLobby"
max_players = 4
server_ip = "192.168.0.133"

sock = clnt.connect_to_server(client_name, client_game, max_players, server_ip)

command_queue = queue.Queue()

def input_thread():

    print("Gib dem Server einen Befehl\n")

    while True:
        try:
            user_input = input(">> ")
            parts = user_input.strip().split()

            if not parts:
                continue

            cmd = parts[0]
            if cmd == "Check" and " ".join(parts[:3]) == "Check Draw Pile":
                command_queue.put(("Check Draw Pile", True))

            elif cmd == "Flip" and parts[1] == "Card":
                x, y = int(parts[2]), int(parts[3])
                command_queue.put(("Flip Card", (x, y)))

            elif cmd == "Take" and parts[1] == "from" and parts[2] == "Discard" and parts[3] == "Pile":
                x, y = int(parts[4]), int(parts[5])
                command_queue.put(("Take from Discard Pile", (x, y)))

            elif cmd == "Take" and parts[1] == "from" and parts[2] == "Draw" and parts[3] == "Pile":
                x, y = int(parts[4]), int(parts[5])
                command_queue.put(("Take from Draw Pile", (x, y)))

            else:
                print("Ungültiger Befehl.")
        except Exception as e:
            print("Fehler bei Eingabe:", e)



threading.Thread(target=input_thread, daemon=True).start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    send_list = []
    while not command_queue.empty():
        send_list.append(command_queue.get())

    if send_list:

        """
        # Alter Code der Probleme gemacht hat:

        clnt.send_to_server(sock, send_list, client_name, client_game)
        received = clnt.receive_from_server(sock)
        """
        try:
            clnt.send_to_server(sock, send_list, client_name, client_game)
            received = clnt.receive_from_server(sock)

            if received is None or received == "Nichts gesendet vom Server":
                print("Warnung: Keine gültige Antwort vom Server erhalten.")
                continue  # nicht abbrechen!

        # Das hier sendet der Server als Info über den Spielzustand:

            game_round = received.get("Game Round")
            game_draw_counter = received.get("Draw Counter")
            game_player_number = received.get("Player Number")
            player_list = received.get("Players")
            discard_pile = received.get("Discard Pile")
            draw_pile = received.get("Draw Pile")
            game_name = received.get("Game Name")
            active = received.get("Active")
            final_phase = received.get("Final Phase")

            card_row_1 = []
            card_row_2 = []
            card_row_3 = []
            discard = []
            draw = []

            # Kartendecks für die Anzeige vorbereiten:

            for player in player_list:
                row1 = player.card_deck[0]
                for card in row1:
                    if card:
                        if not card.visible:
                            card_row_1.append("X")
                        else:
                            card_row_1.append(str(card.value))
                    else:
                        card_row_1.append("D")
                    card_row_1.append("|")
                card_row_1.append("    ")

            for player in player_list:
                row2 = player.card_deck[1]
                for card in row2:
                    if card:
                        if not card.visible:
                            card_row_2.append("X")
                        else:
                            card_row_2.append(str(card.value))
                    else:
                        card_row_2.append("D")
                    card_row_2.append("|")
                card_row_2.append("    ")
    
            for player in player_list:
                row3 = player.card_deck[2]
                for card in row3:
                    if card:
                        if not card.visible:
                            card_row_3.append("X")
                        else:
                            card_row_3.append(str(card.value))
                    else:
                        card_row_3.append("D")
                    card_row_3.append("|")
                card_row_3.append("    ")
        
            # Stapel für die Anzeige vorbereiten:

            for card in discard_pile:
                if card.visible:
                    discard.append(str(card.value))
                else:
                    discard.append("X")

            for card in draw_pile:
                if card.visible:
                    draw.append(str(card.value))
                else:
                    draw.append("X")
        
        # Game State in die Konsole ausgeben:

            print("---------------------------------------------------------- \n")
            print(f"Spiel: {game_name}   Runde: {game_round}   Zugcounter: {game_draw_counter} \n")
            print(f"Spieler anwesend: {game_player_number}   Am Zug: {active}  Endphase:   {final_phase} \n")
            print("---------------------------------------------------------- \n")
            print("".join(card_row_1))
            print("\n")
            print("".join(card_row_2))
            print("\n")
            print("".join(card_row_3))
            print("\n")
            print("---------------------------------------------------------- \n")
            print("Spielernamen:")
            for i, player in enumerate(player_list, 1):
                print(f"Spieler {i}: {player.name}", end="  ")
                print("\n")
            print("---------------------------------------------------------- \n")
            print("Discard Pile: ")
            print(" | ".join(discard) if discard else "Leer")
            print("\n")
            print("Draw Pile: ")
            print(" | ".join(draw) if draw else "Leer")
            print("\n")
            print("---------------------------------------------------------- \n")

        except Exception as e:
            print(f"Fehler während Kommunikation mit Server: {e}")
            continue  # ggf. statt `break`, damit der Client nicht stirbt
        
    else:

        """

        # Alter Code der Probleme gemacht hat:
        
        received = clnt.receive_from_server(sock)
        
        if not received:
            break
        """
        try:
            received = clnt.receive_from_server(sock)
            if received is None or received == "Nichts gesendet vom Server":
                # Kein Problem, einfach weitermachen
                continue
            # Optional: serverseitige Änderungen anzeigen
        except Exception as e:
            print(f"Fehler beim Empfangen: {e}")
            continue