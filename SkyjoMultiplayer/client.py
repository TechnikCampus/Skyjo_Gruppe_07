##### Main client script #####
import pygame
import Client as clnt
import pickle
import sys

pygame.init()

clock = pygame.time.Clock()

client_name = "Hier Client Name eingeben (Test)"
client_game = "Hier den Namen der gewünschten Lobby eingeben (Test)"

clock = pygame.time.Clock()
sock = clnt.connect_to_server(client_name,client_game)

while True:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    send_list = []

    # send_list enthält Parameter-Wert Paare die an den Server gesendet werden sollen
    # Beispiel:

    """
    send_list = [

        ("take_from_discard_pile",True)
        ("flip_card",(4,7))

    ]
    
    """

    # send_list kann auch leer sein wenn nichts gesendet werden muss
    
    clnt.send_to_server(sock,send_list,client_name,client_game)         

    received = clnt.receive_from_server(sock)               # empfängt den aktuellen Spielzustand vom Server
    if not received:
        break


