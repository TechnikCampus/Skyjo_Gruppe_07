##### Main client script #####
import ctypes
# Set the DPI awareness to ensure proper scaling on high DPI displays
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 1 for DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2

import pygame
import pygame_widgets
import Client as clnt
from Client.MenuState import Menu_State
import threading
import queue
import sys

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((1920, 1080))

command_queue = queue.Queue()

menu_state = Menu_State.MAIN_MENU

client_name = ""
client_game = ""
server_ip = ""
sock = None
snapshot = None
send_list = []

GUI = clnt.GUI(display)
GUI.load_images()

def input_thread():

    while True:
        try:
            parts = []
            if not parts:
                continue

            cmd = parts[0]
            if cmd == "check" and " ".join(parts[:3]) == "check draw":
                command_queue.put(("Check Draw Pile", True))

            elif cmd == "flip":
                x, y = int(parts[1]), int(parts[2])
                command_queue.put(("Flip Card", (x, y)))

            elif cmd == "take" and parts[1] == "from" and parts[2] == "discard":
                x, y = int(parts[3]), int(parts[4])
                command_queue.put(("Take from Discard Pile", (x, y)))

            elif cmd == "take" and parts[1] == "from" and parts[2] == "draw":
                x, y = int(parts[3]), int(parts[4])
                command_queue.put(("Take from Draw Pile", (x, y)))

            elif cmd == "leave":
                command_queue.put(("Leave Game",True))

            elif cmd == "end":
                command_queue.put(("End Game", True))

            else:
                print("Ungültiger Befehl.")
        except Exception as e:
            print("Fehler bei Eingabe:", e)

def main_game_loop():
    global sock, client_name, client_game, snapshot
    send_list = []
    while not command_queue.empty():
        send_list.append(command_queue.get())

def connection_handler():
    global sock, client_name, client_game, snapshot, send_list, menu_state
    while True:
        if menu_state != Menu_State.GAME or sock is None or client_name == "" or client_game == "":
            continue
        if send_list:

            try:
                clnt.send_to_server(sock, send_list, client_name, client_game)
                received = clnt.receive_from_server(sock)
                #print([player.card_deck for player in received.get("Players")])

                snapshot = {
                    "Active": received.get("Active"),
                    "Players": received.get("Players"),
                    "Discard Pile": received.get("Discard Pile"),
                    "Draw Pile": received.get("Draw Pile")
                }

                if received is None or received == "Nichts gesendet vom Server":
                    print("Warnung: Keine gültige Antwort vom Server erhalten.")
                    return

                if ("Leave Game",True) in send_list:
                    print("Du hast das Spiel verlassen!") 

            except Exception as e:
                print("Fehler bei der Serverkommunikation:", e)


        else:

            try:
                received = clnt.receive_from_server(sock)
                #print([player.card_deck for player in received.get("Players")])

                snapshot = {
                    "Active": received.get("Active"),
                    "Players": received.get("Players"),
                    "Discard Pile": received.get("Discard Pile"),
                    "Draw Pile": received.get("Draw Pile")
                }

                if received is None or received == "Nichts gesendet vom Server":
                    return
                
            except Exception as e:
                print("Fehler bei der Serverkommunikation:", e)

threading.Thread(target=input_thread, daemon=True).start()
threading.Thread(target=connection_handler, daemon=True).start()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or GUI.get_gui_state()["quitting"]:
            running = False

    display.fill((50, 50, 50))  # Clear the screen with a dark gray color

    client_game = GUI.get_gui_state()["game_name"]
    client_name = GUI.get_gui_state()["client_name"]
    server_ip = GUI.get_gui_state()["server_ip"]
    sock = GUI.get_gui_state()["sock"]
    menu_state = GUI.get_gui_state()["menu_state"]

    match menu_state:
        case Menu_State.MAIN_MENU:
            GUI.Main_Menu()
        case Menu_State.HOST_GAME:
            GUI.Host_Game_Menu()
        case Menu_State.GAME:
            main_game_loop()
            GUI.Game(snapshot)

    pygame_widgets.update(events)

    menu_state = GUI.get_gui_state()["menu_state"]

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
sys.exit()
