##### GUI Functions and Classes for the client #####

from pygame_widgets import button, textbox, slider
import pygame
from pygame import freetype
from Client.MenuState import Menu_State
from Client import network
from Common import *

freetype.init()
font = freetype.Font(None, size=30)

button_height = 70
button_width = 300
button_font_size = 30

textbox_width = 500
textbox_height = 50
textbox_font_size = 30

slider_width = 500
slider_height = 50

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.HEIGHT = screen.get_height()
        self.WIDTH = screen.get_width()
        self.Main_Menu_Widgets = {}
        self.Host_Game_Widgets = {}

        self.menu_state = Menu_State.MAIN_MENU  # Start with the main menu
        self.running = True
        self.server_ip = ""
        self.client_name = ""
        self.game_name = ""
        self.max_players = 0
        self.sock = None

        self.CARD_IMAGES = {}  # Wörterbuch zum Speichern der geladenen Kartenbilder

        self.create_Host_Game()
        self.create_Main_Menu()

    def Main_Menu(self):
        for widget in self.Main_Menu_Widgets.values():
            widget.show()
        for widget in self.Host_Game_Widgets.values():
            widget.hide()

    def Host_Game_Menu(self):
        for widget in self.Host_Game_Widgets.values():
            widget.show()
        for widget in self.Main_Menu_Widgets.values():
            widget.hide()

        # Update the maximum number of players based on slider value
        self.max_players = self.Host_Game_Widgets["max_players_slider"].getValue() + 2
        
        font.render_to(
            self.screen, 
            (self.WIDTH // 2 - 100, 50 + 2 * (button_height + 30)), 
            f'Max Players: {self.max_players}', 
            (0, 0, 0), 
            size=30
        )

    def Game(self, snapshot=None):
        for widget in self.Main_Menu_Widgets.values():
            widget.hide()
        for widget in self.Host_Game_Widgets.values():
            widget.hide()

        if snapshot:
            # Display the game state
            font.render_to(
                self.screen, 
                (self.WIDTH // 2 - 100, 50), 
                f'Game: {self.game_name}', 
                (0, 0, 0), 
                size=40
            )
            # Here you would render the game state using the snapshot data
            # For example, displaying player decks, discard pile, etc.
            player_iter = 0
            for i, player in enumerate(snapshot.get("Players")):
                card_surface = pygame.Surface(((250) * 4 - 10, (370) * 3 + 100)).convert_alpha()  # Create a surface for the player's cards
                card_surface.fill((255, 255, 255, 0))  # Fill with transparent color

                card_deck = player.card_deck
                for j, card_row in enumerate(card_deck):
                    for k, card_info in enumerate(card_row):
                        visible = card_info.get_visible()
                        if visible:
                            card_image = self.CARD_IMAGES.get(str(card_info.get_value())) 
                        else:
                            card_image = self.CARD_IMAGES.get("back")
                        
                        card_surface.blit(card_image, (k * 250, j * 370 + 90))
                if player.name == self.client_name:
                    card_surface = pygame.transform.scale_by(card_surface, 0.5)  # Scale down the card surface
                    self.screen.blit(card_surface, (self.WIDTH / 2 - card_surface.get_width() / 2, self.HEIGHT - card_surface.get_height() - 50))  # Draw the card surface on the screen
                else:
                    font.render_to(
                        card_surface, 
                        (10, 10),
                        f'Player: {player.name}', 
                        (0, 0, 0), 
                        size=70
                    )
                    card_surface = pygame.transform.scale_by(card_surface, 0.3)  # Scale down the card surface
                    self.screen.blit(card_surface, (player_iter * 600 + 100, 100))  # Draw the card surface on the screen
                    player_iter += 1

    def create_Main_Menu(self):
        # Create the main menu widgets
        self.Main_Menu_Widgets = {
            "ip_textbox": textbox.TextBox(
                self.screen, 
                x=self.WIDTH // 2 - textbox_width // 2, y=self.HEIGHT // 2 - textbox_height // 2, width=textbox_width, height=textbox_height,  
                placeholderText='Enter server IP', 
                fontSize=textbox_font_size,
                onSubmit=self.input_ip
            ),
            "connect_button": button.Button(
                self.screen, 
                text='Connect to Server', 
                fontSize=button_font_size,
                x=self.WIDTH // 2 - button_width // 2, y=self.HEIGHT - 2 * button_height - 30, width=button_width, height=button_height, 
                onClick=self.input_ip
            ),
            "exit_button": button.Button(
                self.screen, 
                text='Exit', 
                fontSize=button_font_size,
                x=self.WIDTH // 2 - button_width // 2, y=self.HEIGHT - button_height - 20, width=button_width, height=button_height, 
                onClick=self.exit_game
            ),
        }

    def create_Host_Game(self):
        # Create the widgets for hosting a game
        self.Host_Game_Widgets = {
            "client_name_textbox": textbox.TextBox(
                self.screen, 
                x=self.WIDTH // 2 - textbox_width // 2, y=50, width=textbox_width, height=textbox_height, 
                placeholderText='Enter your name', 
                fontSize=textbox_font_size,
            ),
            "game_name_textbox": textbox.TextBox(
                self.screen, 
                x=self.WIDTH // 2 - textbox_width // 2, y=50 + button_height + 30, width=textbox_width, height=textbox_height, 
                placeholderText='Enter game name', 
                fontSize=textbox_font_size,
            ),
            "max_players_slider": slider.Slider(
                self.screen, 
                x=self.WIDTH // 2 - slider_width // 2, y=50 + 3 * (button_height + 30), width=slider_width, height=slider_height, 
                min=0, max=2, step=1, 
                initial=0, 
            ),
            "back_button": button.Button(
                self.screen, 
                text='Back', 
                fontSize=button_font_size,
                x=self.WIDTH // 2 - button_width // 2, y=self.HEIGHT - button_height - 20, width=button_width, height=button_height, 
                onClick=self.back
            ),
            "host_button": button.Button(
                self.screen, 
                text='Connect to Server', 
                fontSize=button_font_size,
                x=self.WIDTH // 2 - button_width // 2, y=self.HEIGHT - 2 * button_height - 30, width=button_width, height=button_height, 
                onClick=self.start_hosting
            )
        }

    def start_hosting(self):
        # Initialize the hosting process
        self.client_name = self.Host_Game_Widgets["client_name_textbox"].getText()
        self.game_name = self.Host_Game_Widgets["game_name_textbox"].getText()
        if not self.client_name or not self.game_name:
            print("Client name and game name cannot be empty.")
            return
        print(f"Hosting game '{self.game_name}' as {self.client_name} with max players {self.max_players}")
        self.sock = network.connect_to_server(self.client_name, self.game_name, self.max_players, self.server_ip)
        self.sock.settimeout(1.0)  # Set a timeout for the socket operations

        self.menu_state = Menu_State.GAME  # Change to game state after hosting

    def input_ip(self):
            # Initialize the connection to the server
            self.server_ip = self.Main_Menu_Widgets["ip_textbox"].getText()
            if not self.server_ip:
                print("Server IP cannot be empty.")
                return
            print(f"Connecting to server at {self.server_ip}")
            # Here you would typically call a function to connect to the server
            # e.g., clnt.connect_to_server(self.server_ip, self.client_name)

            self.menu_state = Menu_State.HOST_GAME  # Change to host game state after connecting

    def back(self):
        self.menu_state = Menu_State.MAIN_MENU  # Change to main menu state

    def exit_game(self):
        # Initialize the exit process
        print("Exiting game...")
        self.running = False

    def get_gui_state(self):
        return {
            "menu_state": self.menu_state,
            "client_name": self.client_name,
            "game_name": self.game_name,
            "server_ip": self.server_ip,
            "sock": self.sock,
            "quitting": not self.running
        }
    
    def load_images(self):
        # Load card images from the Common.card module
        for card_value, file_name in card.CARD_FILE_MAPPING.items():  # Iteration über die Zuordnung
            card_image = pygame.image.load(f"Common/Karten_png/{file_name}").convert_alpha()  # Laden des Bildes
            self.CARD_IMAGES[str(card_value)] = card_image  # Speichern des Bildes im Wörterbuch
        
        print("Card images loaded successfully.")
