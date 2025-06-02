##### GUI Functions and Classes for the client #####

from pygame_widgets import button, textbox, slider
from pygame import freetype
from Client.MenuState import Menu_State

freetype.init()
font = freetype.Font(None, size=24)

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.server_ip = ""
        self.client_name = ""
        self.game_name = ""
        self.Menu_State = Menu_State.MAIN_MENU
        self.game_exit = False
        self.max_players = 4  # Default max players
        self.create_Host_Game()
        self.create_Join_Game()
        self.create_Main_Menu()

    def Main_Menu(self):
        for widget in self.Main_Menu_Widgets.values():
            widget.show()
        for widget in self.Host_Game_Widgets.values():
            widget.hide()
        for widget in self.Join_Game_Widgets.values():
            widget.hide()

    def Host_Game(self):
        for widget in self.Host_Game_Widgets.values():
            widget.show()
        for widget in self.Main_Menu_Widgets.values():
            widget.hide()
        for widget in self.Join_Game_Widgets.values():
            widget.hide()

    def Join_Game(self):
        for widget in self.Join_Game_Widgets.values():
            widget.show()
        for widget in self.Main_Menu_Widgets.values():
            widget.hide()
        for widget in self.Host_Game_Widgets.values():
            widget.hide()

    def Game(self):
        pass

    def update_server_ip(self, text):
        # Update the server IP address based on user input
        self.server_ip = text.strip()

    def update_client_name(self, text):
        # Update the client name based on user input
        self.client_name = text.strip()

    def update_game_name(self, text):
        # Update the game name based on user input
        self.game_name = text.strip()

    def update_max_players(self, value):
        # Update the maximum number of players based on slider value
        self.max_players = int(value)

    def connect_to_server(self):
        # Initialize the connection to the server
        print(f"Connecting to server at {self.server_ip}")
        # Here you would typically call a function to connect to the server
        # e.g., clnt.connect_to_server(self.server_ip, self.client_name)

        self.Menu_State = Menu_State.HOST_GAME  # Change to host game state after connecting
    
    def start_hosting(self):
        # Initialize the hosting process
        print(f"Hosting game '{self.game_name}' as {self.client_name} with max players {self.max_players}")

        self.Menu_State = Menu_State.GAME  # Change to game state after hosting

    def join_game(self):
        # Initialize the joining process
        print(f"Joining game '{self.game_name}' as {self.client_name}")

        self.Menu_State = Menu_State.GAME  # Change to game state after joining

    def exit_game(self):
        # Initialize the exit process
        print("Exiting game...")
        self.game_exit = True

    def create_Main_Menu(self):
        # Create buttons for the main menu
        self.Main_Menu_Widgets = {
            "ip_textbox": textbox.TextBox(
                self.screen, 
                x=100, y=50, width=200, height=50, 
                font=font, 
                text='Enter server IP', 
                onChange=self.update_server_ip
            ),
            "connect_button": button.Button(
                self.screen, 
                text='Connect to Server', 
                x=100, y=100, width=200, height=50, 
                onClick=self.connect_to_server
            ),
            "exit_button": button.Button(
                self.screen, 
                text='Exit', 
                x=100, y=300, width=200, height=50, 
                onClick=self.exit_game
            )
        }

    def create_Host_Game(self):
        # Create a button to start hosting the game
        self.Host_Game_Widgets = {
            "client_name_textbox": textbox.TextBox(
                self.screen, 
                x=100, y=50, width=200, height=50, 
                font=font, 
                text='Enter your name', 
                onChange=self.update_client_name
            ),
            "game_name_textbox": textbox.TextBox(
                self.screen, 
                x=100, y=150, width=200, height=50, 
                font=font, 
                text='Enter game name', 
                onChange=self.update_game_name
            ),
            "max_players_slider": slider.Slider(
                self.screen, 
                x=100, y=100, width=200, height=50, 
                min=2, max=8, step=1, 
                initial=4, 
                onChange=self.update_max_players
            ),
            "back_button": button.Button(
                self.screen, 
                text='Back', 
                x=100, y=200, width=200, height=50, 
                onClick=self.Main_Menu
            ),
            "host_button": button.Button(
                self.screen, 
                text='Connect to Server', 
                x=100, y=100, width=200, height=50, 
                onClick=self.start_hosting
            )
        }

    def create_Join_Game(self):
        # Create a button to join a game
        self.Join_Game_Widgets = {
            "client_name_textbox": textbox.TextBox(
                self.screen, 
                x=100, y=50, width=200, height=50, 
                font=font, 
                text='Enter your name', 
                onChange=self.update_client_name
            ),
            "game_name_textbox": textbox.TextBox(
                self.screen, 
                x=100, y=150, width=200, height=50, 
                font=font, 
                text='Enter game name', 
                onChange=self.update_game_name
            ),
            "back_button": button.Button(
                self.screen, 
                text='Back', 
                x=100, y=200, width=200, height=50, 
                onClick=self.Main_Menu
            ),
            "join_button": button.Button(
                self.screen, 
                text='Connect to Server', 
                x=100, y=100, width=200, height=50, 
                onClick=self.join_game
            )
        }
    
    def get_Menu_State(self):
        # Return the current menu state
        return self.Menu_State
