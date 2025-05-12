##### Main server script #####

import Server as svr
import pygame

server = svr.start_socket()

pygame.init()
clock = pygame.time.clock()

while True:
    
    clock.tick(60)
    svr.create_client_thread(server)




