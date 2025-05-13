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

    try:
        data = sock.recv(4096)  # groß genug für Dictionary
        message_from_server = pickle.loads(data)

        # Ausgabe der empfangenen Daten
        print("Nachricht vom Server:")
        for key, value in message_from_server.items():
            print(f"{key}: {value}")
    except:
        print("Konnte nichts empfangen")

    # Tesprogramm #