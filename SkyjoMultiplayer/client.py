##### Main client script #####
import pygame
import Client as clnt
import pickle

client_name = "Jonas"

pygame.init()
clock = pygame.time.Clock()
sock = clnt.connect_to_server(client_name)

while True:

    clock.tick(60)
    clnt.send_to_server(sock,clnt.get_Player_Input(),client_name)
    received = clnt.receive_from_server(sock)                         # enthält nun den vom Server gesendeten game_state
