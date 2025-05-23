import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider 
from pygame_widgets.textbox import TextBox

# --- Farben ---
WHITE = (255, 255, 255)
TURQUOISE = (52, 197, 209)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# --- Fenstergröße ---
WIDTH, HEIGHT = 1000, 600

# --- Initialisierung ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skyjo Multiplayer")
font = pygame.font.SysFont(None, 36)

# --- Globale Variablen ---
slider = None
player_name_box = None
game_name_box = None
widgets = []
host_button_rect = (0, 0, 0, 0)
join_button_rect = (0, 0, 0, 0)


client_name = ""
client_game = ""

# --- Buttons Hauptmenü ---
buttons = [
    ("Spiel erstellen", (400, 320, 200, 50)),
    ("Spiel beitreten", (400, 400, 200, 50))
]

# --- Callback-Funktion für TextBox Submit ---
def output():
    if player_name_box and game_name_box:
        print("Spielername:", player_name_box.getText())
        print("Servername:", game_name_box.getText())

# --- Hilfsfunktionen ---
def reset_widgets():
    global widgets, slider, player_name_box, game_name_box
    widgets.clear()
    slider = None
    player_name_box = None
    game_name_box = None

def draw_buttons():
    for text, rect in buttons:
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2)
        txt_surf = font.render(text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=(rect[0] + rect[2]//2, rect[1] + rect[3]//2))
        screen.blit(txt_surf, txt_rect)

def draw_background_text():
    big_font = pygame.font.SysFont(None, 100)
    text_surface = big_font.render("Skyjo Multiplayer", True, WHITE)
    text_surface.set_alpha(200)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text_surface, text_rect)

def draw_spielerauswahl():
    global host_button_rect

    # Überschrift
    header_font = pygame.font.SysFont(None, 60)
    header = header_font.render("Spiel hosten", True, BLACK)
    header_rect = header.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 160))
    screen.blit(header, header_rect)

    # Labels
    label_font = pygame.font.SysFont(None, 32)
    spieler_label = label_font.render("Spielername", True, BLACK)
    spieler_label_rect = spieler_label.get_rect(midleft=(WIDTH // 2 - 150, HEIGHT // 2 - 110))
    screen.blit(spieler_label, spieler_label_rect)

    game_label = label_font.render("Servername", True, BLACK)
    game_label_rect = game_label.get_rect(midleft=(WIDTH // 2 - 150, HEIGHT // 2 - 20))
    screen.blit(game_label, game_label_rect)

    # TextBoxen für Namen
    if player_name_box:
        player_name_box.setX(WIDTH // 2 - 150)
        player_name_box.setY(HEIGHT // 2 - 80)
        player_name_box.draw()
    if game_name_box:
        game_name_box.setX(WIDTH // 2 - 150)
        game_name_box.setY(HEIGHT // 2)
        game_name_box.draw()

    # Slider Position & Anzeige
    slider_width = 300
    slider_x = WIDTH // 2 - slider_width // 2
    slider_y = HEIGHT // 2 + 120
    if slider:
        slider.setX(slider_x)
        slider.setY(slider_y)

        value_font = pygame.font.SysFont(None, 40)
        value_text = value_font.render(f"{slider.getValue()} Spieler", True, BLACK)
        value_rect = value_text.get_rect(center=(WIDTH // 2, slider_y - 30))
        screen.blit(value_text, value_rect)

    # "Spiel erstellen"-Button
    btn_width, btn_height = 180, 45
    btn_x = WIDTH // 2 - btn_width // 2
    btn_y = slider_y + 60
    host_button_rect = (btn_x, btn_y, btn_width, btn_height)

    pygame.draw.rect(screen, GRAY, host_button_rect)
    pygame.draw.rect(screen, DARK_GRAY, host_button_rect, 2)
    btn_font = pygame.font.SysFont(None, 32)
    btn_text = btn_font.render("Spiel Erstellen", True, BLACK)
    btn_text_rect = btn_text.get_rect(center=(btn_x + btn_width // 2, btn_y + btn_height // 2))
    screen.blit(btn_text, btn_text_rect)

def draw_join():
    global join_button_rect

    # Überschrift
    header_font = pygame.font.SysFont(None, 60)
    header = header_font.render("Spiel beitreten", True, BLACK)
    header_rect = header.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 160))
    screen.blit(header, header_rect)

    # Labels
    label_font = pygame.font.SysFont(None, 32)
    spieler_label = label_font.render("Spielername", True, BLACK)
    spieler_label_rect = spieler_label.get_rect(midleft=(WIDTH // 2 - 150, HEIGHT // 2 - 110))
    screen.blit(spieler_label, spieler_label_rect)

    game_label = label_font.render("Servername", True, BLACK)
    game_label_rect = game_label.get_rect(midleft=(WIDTH // 2 - 150, HEIGHT // 2 - 20))
    screen.blit(game_label, game_label_rect)

    # TextBoxen für Namen
    if player_name_box:
        player_name_box.setX(WIDTH // 2 - 150)
        player_name_box.setY(HEIGHT // 2 - 80)
        player_name_box.draw()
    if game_name_box:
        game_name_box.setX(WIDTH // 2 - 150)
        game_name_box.setY(HEIGHT // 2)
        game_name_box.draw()

    # "Beitreten"-Button
    btn_width, btn_height = 180, 45
    btn_x = WIDTH // 2 - btn_width // 2
    btn_y = HEIGHT // 2 + 120
    join_button_rect = (btn_x, btn_y, btn_width, btn_height)

    pygame.draw.rect(screen, GRAY, join_button_rect)
    pygame.draw.rect(screen, DARK_GRAY, join_button_rect, 2)
    btn_font = pygame.font.SysFont(None, 32)
    btn_text = btn_font.render("Beitreten", True, BLACK)
    btn_text_rect = btn_text.get_rect(center=(btn_x + btn_width // 2, btn_y + btn_height // 2))
    screen.blit(btn_text, btn_text_rect)

def draw_lobby(server_name, player_count):
    header_font = pygame.font.SysFont(None, 60)
    header = header_font.render("Lobby", True, BLACK)
    header_rect = header.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(header, header_rect)

    info_font = pygame.font.SysFont(None, 40)
    info_text = info_font.render(f"Beigetreten zu: {server_name}", True, BLACK)
    info_rect = info_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(info_text, info_rect)

    player_text = info_font.render(f"Spieler im Raum: {player_count}", True, BLACK)
    player_rect = player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(player_text, player_rect)

# --- Hauptfunktion ---
def main():
    global slider, player_name_box, game_name_box, widgets, client_name, client_game
    state = "main"
    lobby_server_name = ""
    lobby_player_count = 0

    while True:
        screen.fill(TURQUOISE)
        
        match state:
            case "main":
                draw_background_text()
                draw_buttons()
                reset_widgets()

            case "host":
                # Widgets initialisieren, wenn noch nicht vorhanden
                if not slider:
                    slider = Slider(screen, WIDTH // 2 - 150, HEIGHT // 2 + 140, 300, 30, min=2, max=4, step=1)
                    widgets.append(slider)

                if not player_name_box:
                    player_name_box = TextBox(
                        screen, WIDTH // 2 - 150, HEIGHT // 2 - 80, 300, 40, fontSize=20,
                        borderColour=BLACK, textColour=BLACK,
                        onSubmit=output, radius=10, borderThickness=2)
                    widgets.append(player_name_box)

                if not game_name_box:
                    game_name_box = TextBox(
                        screen, WIDTH // 2 - 150, HEIGHT // 2, 300, 40, fontSize=20,
                        borderColour=BLACK, textColour=BLACK,
                        onSubmit=output, radius=10, borderThickness=2)
                    widgets.append(game_name_box)
                    

                draw_spielerauswahl()

            case "join":
                # Widgets initialisieren, wenn noch nicht vorhanden
                if not player_name_box:
                    player_name_box = TextBox(
                        screen, WIDTH // 2 - 150, HEIGHT // 2 - 80, 300, 40, fontSize=20,
                        borderColour=BLACK, textColour=BLACK,
                        onSubmit=output, radius=10, borderThickness=2)
                    widgets.append(player_name_box)

                if not game_name_box:
                    game_name_box = TextBox(
                    screen, WIDTH // 2 - 150, HEIGHT // 2, 300, 40, fontSize=20,
                    borderColour=BLACK, textColour=BLACK,
                    onSubmit=output, radius=10, borderThickness=2)
                widgets.append(game_name_box)

                draw_join()

            case "lobby":
                draw_lobby(lobby_server_name, lobby_player_count)
                reset_widgets()

        # Events verarbeiten
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            match state:
                case "main":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = event.pos
                        for idx, (_, rect) in enumerate(buttons):
                            if pygame.Rect(rect).collidepoint(mx, my):
                                if idx == 0:
                                    state = "host"
                                elif idx == 1:
                                    state = "join"

                case "host":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if pygame.Rect(host_button_rect).collidepoint(event.pos):
                            # Speichere die Eingaben in die globalen Variablen
                            client_name = player_name_box.getText() if player_name_box else ""
                            client_game = game_name_box.getText() if game_name_box else ""
                            print(f"Spiel hosten mit {slider.getValue()} Spielern, Spielername: {client_name}, Spielname: {client_game}")
                            # Hier ggf. zu "lobby" wechseln:
                            # state = "lobby"
                            # lobby_server_name = client_game
                            # lobby_player_count = slider.getValue()

                case "join":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if pygame.Rect(join_button_rect).collidepoint(event.pos):
                            # Speichere die Eingaben in die globalen Variablen
                            client_name = player_name_box.getText() if player_name_box else ""
                            client_game = game_name_box.getText() if game_name_box else ""
                            print(f"Beitreten mit Spielername: {client_name}, Servername: {client_game}")
                            # Hier ggf. zu "lobby" wechseln:
                            # state = "lobby"
                            # lobby_server_name = client_game
                            # lobby_player_count = 1

        pygame_widgets.update(events)
        pygame.display.flip()



if __name__ == "__main__":
    main()