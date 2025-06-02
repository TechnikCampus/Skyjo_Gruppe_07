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

GUI = clnt.GUI(display)

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

threading.Thread(target=input_thread, daemon=True).start()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or GUI.game_exit:
            running = False

    send_list = []
    while not command_queue.empty():
        send_list.append(command_queue.get())

    display.fill((255, 255, 255))  # Clear the screen with white

    match menu_state:
        case Menu_State.MAIN_MENU:
            GUI.Main_Menu()
        case Menu_State.HOST_GAME:
            GUI.Host_Game()
        case Menu_State.JOIN_GAME:
            GUI.Join_Game()
        case Menu_State.GAME:
            GUI.Game()

    pygame_widgets.update(events)

    menu_state = GUI.get_Menu_State()

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS
