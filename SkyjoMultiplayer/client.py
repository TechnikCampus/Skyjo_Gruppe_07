##### Main client script #####
import pygame
import Client as clnt
import pickle

pygame.init()
clock = pygame.time.Clock()
sock = clnt.connect_to_server()

while True:

    clock.tick(60)

    # Testprogramm #
    message = input("Was ist deine Nachricht an den Server")
    serialised = {"msg": message}
    sock.sendall(pickle.dumps(serialised))

    # Tesprogramm #