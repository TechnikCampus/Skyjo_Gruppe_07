##### GUI Functions and Classes for the client #####

from pygame_widgets import button, textbox, slider
from pygame import freetype
from Client.MenuState import Menu_State
from Client import network

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
        self.server_ip = ""
        self.client_name = ""
        self.game_name = ""
        self.socket = None
        self.Menu_State = Menu_State.MAIN_MENU
        self.game_exit = False
        self.max_players = 4  # Default max players
        self.HEIGHT = screen.get_height()
        self.WIDTH = screen.get_width()
        self.Main_Menu_Widgets = {}
        self.Host_Game_Widgets = {}
        self.create_Host_Game()
        self.create_Main_Menu()

    def Main_Menu(self):
        for widget in self.Main_Menu_Widgets.values():
            widget.show()
        for widget in self.Host_Game_Widgets.values():
            widget.hide()

    def Host_Game(self):
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

    def Game(self):
        for widget in self.Main_Menu_Widgets.values():
            widget.hide()
        for widget in self.Host_Game_Widgets.values():
            widget.hide()

    def connect_to_server(self):
        # Initialize the connection to the server
        self.server_ip = self.Main_Menu_Widgets["ip_textbox"].getText()
        if not self.server_ip:
            print("Server IP cannot be empty.")
            return
        print(f"Connecting to server at {self.server_ip}")
        # Here you would typically call a function to connect to the server
        # e.g., clnt.connect_to_server(self.server_ip, self.client_name)

        self.Menu_State = Menu_State.HOST_GAME  # Change to host game state after connecting
    
    def start_hosting(self):
        # Initialize the hosting process
        self.client_name = self.Host_Game_Widgets["client_name_textbox"].getText()
        self.game_name = self.Host_Game_Widgets["game_name_textbox"].getText()
        if not self.client_name or not self.game_name:
            print("Client name and game name cannot be empty.")
            return
        print(f"Hosting game '{self.game_name}' as {self.client_name} with max players {self.max_players}")
        self.socket = network.connect_to_server(self.client_name, self.game_name, self.max_players, self.server_ip)

        self.Menu_State = Menu_State.GAME  # Change to game state after hosting

    def exit_game(self):
        # Initialize the exit process
        print("Exiting game...")
        self.game_exit = True

    def back(self):
        self.Menu_State = Menu_State.MAIN_MENU  # Change to main menu state

    def create_Main_Menu(self):
        # Create the main menu widgets
        self.Main_Menu_Widgets = {
            "ip_textbox": textbox.TextBox(
                self.screen, 
                x=self.WIDTH // 2 - textbox_width // 2, y=self.HEIGHT // 2 - textbox_height // 2, width=textbox_width, height=textbox_height,  
                placeholderText='Enter server IP', 
                fontSize=textbox_font_size,
                onSubmit=self.connect_to_server
            ),
            "connect_button": button.Button(
                self.screen, 
                text='Connect to Server', 
                fontSize=button_font_size,
                x=self.WIDTH // 2 - button_width // 2, y=self.HEIGHT - 2 * button_height - 30, width=button_width, height=button_height, 
                onClick=self.connect_to_server
            ),
            "exit_button": button.Button(
                self.screen, 
                text='Exit', 
                fontSize=button_font_size,
                x=self.WIDTH // 2 - button_width // 2, y=self.HEIGHT - button_height - 20, width=button_width, height=button_height, 
                onClick=self.exit_game
            )
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
    
    def get_Menu_State(self):
        # Return the current menu state
        return self.Menu_State
