##### GUI Functions and Classes for the client #####

import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider 
from pygame_widgets.textbox import TextBox

def get_Player_Input():
    pass

# Farben
WHITE = (255, 255, 255)
turkis= (52,197,209)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# ...existing imports und Farben...

# Fenstergröße
WIDTH, HEIGHT = 1000, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skyjo Multiplayer")

font = pygame.font.SysFont(None, 36)

# Button-Daten: (Text, (x, y, Breite, Höhe))
buttons = [
    ("Spiel erstellen", (400, 320, 200, 50)),
    ("Spiel beitreten", (400, 400, 200, 50))
]

slider = None

host_button_rect = (450, 280, 150, 40)


def draw_buttons():
    for text, rect in buttons:
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2)
        txt_surf = font.render(text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=(rect[0]+rect[2]//2, rect[1]+rect[3]//2))
        screen.blit(txt_surf, txt_rect)

def draw_background_text():
    big_font = pygame.font.SysFont(None, 100)
    text_surface = big_font.render("Skyjo Multiplayer", True, (255, 255, 255))
    text_surface.set_alpha(200)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text_surface, text_rect)

def draw_spielerauswahl():
    # Überschrift mittig
    header_font = pygame.font.SysFont(None, 60)
    header = header_font.render("Spiel hosten", True, BLACK)
    header_rect = header.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(header, header_rect)
    # Slider mittig
    slider_width = 300
    slider_x = WIDTH // 2 - slider_width // 2
    slider_y = HEIGHT // 2 - 20

    if slider :
        slider.setX(slider_x)
        slider.setY(slider_y)
        slider.draw()
        # Spieleranzahl als Zahl über dem Slider anzeigen
        value_font = pygame.font.SysFont(None, 40)
        value_text = value_font.render(f"{slider.getValue()} Spieler", True, BLACK)
        value_rect = value_text.get_rect(center=(slider_x + 30, slider_y - 30))
        screen.blit(value_text, value_rect)
    # "Spiel hosten"-Button mittig unter dem Slider
    btn_width, btn_height = 180, 45
    btn_x = WIDTH // 2 - btn_width // 2
    btn_y = slider_y + 60
    global host_button_rect
    host_button_rect = (btn_x, btn_y, btn_width, btn_height)
    pygame.draw.rect(screen, GRAY, host_button_rect)
    pygame.draw.rect(screen, DARK_GRAY, host_button_rect, 2)
    btn_font = pygame.font.SysFont(None, 32)
    btn_text = btn_font.render("Spiel Erstellen", True, BLACK)
    btn_text_rect = btn_text.get_rect(center=(btn_x + btn_width // 2, btn_y + btn_height // 2))
    screen.blit(btn_text, btn_text_rect)

def main():
    global slider
    state = "main"  # "main", "host"
    while True:
        screen.fill(turkis)
        if state == "main":
            draw_background_text()
            draw_buttons()
            # Slider  werden entfernt, falls noch vorhanden
            if slider:
                slider.hide()
                slider = None
        elif state == "host":
            # Slider werden nur im Host-Mode erzeugt
            if not slider:
                slider_width = 300  # z.B. 300 Pixel breit
                slider_x = WIDTH // 2 - slider_width // 2
                slider_y = HEIGHT // 2 - 20
                slider = Slider(screen, slider_x, slider_y, slider_width, 30, min=2, max=4, step=1)
            draw_spielerauswahl()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if state == "main" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for idx, (_, rect) in enumerate(buttons):
                    r = pygame.Rect(rect)
                    if r.collidepoint(mx, my):
                        if idx == 0:
                            state = "host"
                        elif idx == 1:
                            print("Spiel beitreten geklickt")
            if state == "host" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                r = pygame.Rect(host_button_rect)
                if r.collidepoint(mx, my):
                    print(f"Spiel hosten mit {slider.getValue()} Spielern!")
        pygame_widgets.update(events)
        pygame.display.flip()

if __name__ == "__main__":
    main()