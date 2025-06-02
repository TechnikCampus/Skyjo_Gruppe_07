##### Main client script #####
import pygame
import pygame_widgets
import Client as clnt
from Client.MenuState import Menu_State
import sys

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((800, 600))

menu_state = Menu_State.MAIN_MENU

GUI = clnt.GUI(display)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or GUI.game_exit:
            running = False

    GUI.Main_Menu() if menu_state == Menu_State.MAIN_MENU else None
    GUI.Host_Game() if menu_state == Menu_State.HOST_GAME else None
    GUI.Join_Game() if menu_state == Menu_State.JOIN_GAME else None

    pygame_widgets.update(pygame.event.get())

    menu_state = GUI.get_Menu_State()

    pygame.display.flip()
    clock.tick(60)
