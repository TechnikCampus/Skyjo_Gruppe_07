##### Main client script #####
import pygame
import Client as clnt
import pickle
import sys

pygame.init()

clock = pygame.time.Clock()

client_name = "Hier Client Name eingeben (Test)"

clock = pygame.time.Clock()
sock = clnt.connect_to_server(client_name)

while True:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    send_list = []                                          # Liste mit Dingen die an den Server gesendet werden sollen
                                                            # siehe Client\network.py -> def send_to_server
    clnt.send_to_server(sock,send_list,client_name)         

    received = clnt.receive_from_server(sock)               # empfängt den aktuellen Spielzustand vom Server
    if not received:
        break


