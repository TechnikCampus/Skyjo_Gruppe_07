##### Main client script #####
import pygame
import Client as clnt
import pickle
import sys

pygame.init()

# Test:

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Debugfenster")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# Test

client_name = "Jonas"

clock = pygame.time.Clock()
sock = clnt.connect_to_server(client_name)

take_from_discard_pile = False
accept_card = False
choose_card = False

while True:

    # Test:

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                take_from_discard_pile = not take_from_discard_pile
            elif event.key == pygame.K_b:
                accept_card = not accept_card
            elif event.key == pygame.K_c:
                choose_card = not choose_card

    send_list = [take_from_discard_pile,accept_card,choose_card]
    clnt.send_to_server(sock,send_list,client_name)

    received = clnt.receive_from_server(sock)
    if not received:
        break
    print(received)

    """
    debugging_screen = {

        f"Round counter: {received["Game_Round"]}",
        f"Player counter: {received["Player_Number"]}",
        f"Client Name: {received["Your Name"]}"
    }

    for i, line in enumerate(debugging_screen):
        text_surface = font.render(line, True, (255, 255, 255))  # Weißer Text
        screen.blit(text_surface, (10, 10 + i * 30))
    """
    screen.fill((0,0,0))
    pygame.display.flip()

    # Test
