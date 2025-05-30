##### Main client script #####
import pygame
import Client as clnt
import sys

pygame.init()

clock = pygame.time.Clock()

client_name = "Jonas"
client_game = "NeueLobby"
max_players = 4

clock = pygame.time.Clock()
sock = clnt.connect_to_server(client_name,client_game,max_players)

while True:

    #clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    send_list = []

    # send_list enthält Parameter-Wert Paare die an den Server gesendet werden sollen
    # Beispiel:


    send_list = [

    ]
    
    # send_list kann auch leer sein wenn nichts gesendet werden muss
    
    clnt.send_to_server(sock,send_list,client_name,client_game)         
    
    received = clnt.receive_from_server(sock)

    if not received:
        break



