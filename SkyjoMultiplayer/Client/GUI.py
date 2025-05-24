import pygame
import sys
import pygame_widgets
from pygame import freetype
from pygame_widgets.slider import Slider 
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

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
freetype.init()

# --- Schriftarten ---
font = freetype.SysFont('Arial', 24, bold=True)


# --- Globale Variablen ---
state = "main"  # Startzustand

# --- Button Click Funktions ---
def back():
    print("Back button clicked")
    global state
    match state:
        case "host":
            state = "main"
        case "join":
            state = "main"

def host_menu():
    print("Host game button clicked")
    global state
    state = "host"

def join_menu():
    print("Join game button clicked")
    global state
    state = "join"

def host_game():
    global client_name, client_game
    print("Host game button clicked")
    if host_page["player_name_box"] and host_page["game_name_box"]:
        client_name = host_page["player_name_box"].getText()
        client_game = host_page["game_name_box"].getText()
        print(f"Hosting game with name: {client_game} and player: {client_name}")

def join_game():
    global client_name, client_game
    print("Join game button clicked")
    if join_page["player_name_box"] and join_page["game_name_box"]:
        client_name = join_page["player_name_box"].getText()
        client_game = join_page["game_name_box"].getText()
        print(f"Joining game with name: {client_game} and player: {client_name}")

# --- Standard Widget Size and Color ---
button_size = (200, 50)

# --- UI Pages ---
main_page = {
    "host_menu_button": Button(screen, WIDTH // 2 - button_size[0] // 2, 320, *button_size, text ="Spiel erstellen", radius = 10, onClick=host_menu),
    "join_menu_button": Button(screen, WIDTH // 2 - button_size[0] // 2, 400, *button_size, text ="Spiel beitreten", radius = 10, onClick=join_menu)
}

host_page = {
    "player_name_box": TextBox(screen, WIDTH // 2 - 150, 80, 300, 40, fontSize=24, placeholderText="Spielername"),
    "game_name_box": TextBox(screen, WIDTH // 2 - 150, 160, 300, 40, fontSize=24, placeholderText="Servername"),
    "max_players_slider": Slider(screen, WIDTH // 2 - 150, 280, 300, 20, min=0, max=2, step=1, initial=0, handleRadius=15),
    "host_button": Button(screen, WIDTH // 2 - button_size[0] // 2, 320, *button_size, text ="Spiel erstellen", radius = 10, onClick=host_game),
    "back_button": Button(screen, 10, HEIGHT - 60, *button_size, text ="Zurück", radius = 10, onClick=back)
}
join_page = {
    "player_name_box": TextBox(screen, WIDTH // 2 - 150, 80, 300, 40, fontSize=24, placeholderText="Spielername"),
    "game_name_box": TextBox(screen, WIDTH // 2 - 150, 160, 300, 40, fontSize=24, placeholderText="Servername"),
    "host_button": Button(screen, WIDTH // 2 - button_size[0] // 2, 320, *button_size, text ="Spiel erstellen", radius = 10, onClick=host_game),
    "back_button": Button(screen, 10, HEIGHT - 60, *button_size, text ="Zurück", radius = 10, onClick=back)
}


client_name = ""
client_game = ""
max_players = 0

# --- Hilfsfunktionen ---
def display_ui(state):
    match state:
        case "main":
            for widget in main_page.values():
                widget.show()
            for widget in host_page.values():
                widget.hide()
            for widget in join_page.values():
                widget.hide()
            font.size = 60
            font.render_to(screen, (WIDTH // 2 - font.get_rect("Skyjo Multiplayer").width // 2, 100), "Skyjo Multiplayer", WHITE)
        case "host":
            for widget in host_page.values():
                widget.show()
            for widget in main_page.values():
                widget.hide()
            for widget in join_page.values():
                widget.hide()
            
            font.size = 24
            font.render_to(screen, (WIDTH // 2 - font.get_rect("Max Spieleranzahl: 0").width // 2, 240), f"Max Spieleranzahl: {max_players}", WHITE)
        case "join":
            for widget in join_page.values():
                widget.show()
            for widget in main_page.values():
                widget.hide()
            for widget in host_page.values():
                widget.hide()


# --- Hauptfunktion ---
def main():
    global state, max_players

    while True:
        screen.fill(TURQUOISE)
        display_ui(state)

        max_players = host_page["max_players_slider"].getValue() + 2 if state == "host" else 0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame_widgets.update(events)
        pygame.display.flip()



if __name__ == "__main__":
    main()