##### Neue verbesserte GUI für Skyjo Client #####

from pygame_widgets import button, textbox, slider
import pygame
from pygame import freetype
from Client.MenuState import Menu_State
from Client import network
from Client.GameRenderer import GameRenderer
from Client.WidgetManager import WidgetManager
from Client.EventHandler import EventHandler
from Client.GameStateManager import GameStateManager
from Common import *
import socket

# Pygame und Font initialisieren
freetype.init()
pygame.init()

# Design Konstanten
COLORS = {
    'background': (135, 206, 235),  # Sky blue
    'card_bg': (255, 255, 255),     # White
    'text_primary': (0, 0, 0),      # Black
    'text_secondary': (64, 64, 64), # Dark gray
    'accent': (0, 100, 200),        # Blue
    'warning': (200, 100, 0),       # Orange
    'success': (0, 150, 0),         # Green
    'error': (200, 0, 0),           # Red
    'selected': (255, 255, 0),      # Yellow
    'button_bg': (240, 240, 240),   # Light gray
    'bg_primary': (255, 255, 255),  # White - for primary background
    'bg_secondary': (220, 220, 220), # Light gray - for secondary background
}

FONTS = {
    'title': freetype.Font(None, size=48),
    'subtitle': freetype.Font(None, size=32),
    'normal': freetype.Font(None, size=24),
    'small': freetype.Font(None, size=18),
    'button': freetype.Font(None, size=20),
}

# Layout Konstanten
LAYOUT = {
    'button_width': 280,
    'button_height': 60,
    'textbox_width': 400,
    'textbox_height': 50,
    'slider_width': 400,
    'slider_height': 40,
    'margin': 20,
    'card_width': 120,
    'card_height': 180,
    'card_spacing': 10,
}

class SkyjoGUI:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        
        # Design constants as instance attributes
        self.COLORS = COLORS
        self.FONTS = FONTS
        self.LAYOUT = LAYOUT
        
        # GUI State
        self.menu_state = Menu_State.MAIN_MENU
        self.running = True
        
        # Game State
        self.server_ip = ""
        self.client_name = ""
        self.game_name = ""
        self.max_players = 2
        self.sock = None
        
        # Initialize helper classes
        self.game_state = GameStateManager()
        self.widget_manager = WidgetManager(screen, self.COLORS, self.LAYOUT)
        self.event_handler = EventHandler(screen, self.COLORS, self.LAYOUT)
        self.game_renderer = None  # Will be initialized after card images are loaded
        
        # GUI State for hover effects
        self.hovered_card = None  # Currently hovered card position
        self.hovered_pile = None  # Currently hovered pile ("draw" or "discard")
        
        # Card Images
        self.card_images = {}
        
        # Set up widget callbacks
        self._setup_widget_callbacks()
    
    def _setup_widget_callbacks(self):
        """Setzt die Callbacks für alle Widgets"""
        # Main menu callbacks
        self.widget_manager.set_widget_callback('main_menu', 'ip_textbox', self._on_connect_clicked)
        self.widget_manager.set_widget_callback('main_menu', 'connect_button', self._on_connect_clicked)
        self.widget_manager.set_widget_callback('main_menu', 'exit_button', self._on_exit_clicked)
        
        # Host game callbacks
        self.widget_manager.set_widget_callback('host_game', 'start_button', self._on_start_clicked)
        self.widget_manager.set_widget_callback('host_game', 'back_button', self._on_back_clicked)
    
    def load_card_images(self):
        """Lädt alle Kartenbilder"""
        try:
            for card_value, file_name in card.CARD_FILE_MAPPING.items():
                image_path = f"Common/Karten_png/{file_name}"
                card_image = pygame.image.load(image_path).convert_alpha()
                # Skaliere Bilder auf einheitliche Größe
                scaled_image = pygame.transform.scale(card_image, (LAYOUT['card_width'], LAYOUT['card_height']))
                self.card_images[str(card_value)] = scaled_image
            
            # Initialize GameRenderer after card images are loaded
            self.game_renderer = GameRenderer(self.screen, self.COLORS, self.FONTS, self.LAYOUT, self.card_images)
            
            return True
        except Exception as e:
            return False
    
    # =================== RENDERING METHODS ===================
    
    def render_main_menu(self):
        """Rendert das Hauptmenü"""
        self.widget_manager.show_widgets('main_menu')
        self.widget_manager.hide_widgets('host_game', 'game')
        
        # Title
        title_rect = FONTS['title'].get_rect("Skyjo Multiplayer")
        FONTS['title'].render_to(
            self.screen,
            (self.WIDTH // 2 - title_rect.width // 2, 100),
            "Skyjo Multiplayer",
            COLORS['text_primary']
        )
        
        # Subtitle
        subtitle_rect = FONTS['subtitle'].get_rect("Willkommen zum Skyjo Kartenspiel!")
        FONTS['subtitle'].render_to(
            self.screen,
            (self.WIDTH // 2 - subtitle_rect.width // 2, 160),
            "Willkommen zum Skyjo Kartenspiel!",
            COLORS['text_secondary']
        )
        
        # Enter key hint
        hint_text = "Tipp: Drücke Enter zum Verbinden"
        FONTS['small'].render_to(
            self.screen,
            (self.WIDTH // 2 - 100, self.HEIGHT - 30),
            hint_text,
            COLORS['text_secondary']
        )
    
    def render_host_game_menu(self):
        """Rendert das Host Game Menü"""
        self.widget_manager.show_widgets('host_game')
        self.widget_manager.hide_widgets('main_menu', 'game')
        
        # Title
        title_rect = FONTS['title'].get_rect("Neues Spiel erstellen")
        FONTS['title'].render_to(
            self.screen,
            (self.WIDTH // 2 - title_rect.width // 2, 50),
            "Neues Spiel erstellen",
            COLORS['text_primary']
        )
        
        # Max Players Label
        self.max_players = self.widget_manager.get_widget_value('host_game', 'players_slider') + 2
        players_text = f"Maximale Spielerzahl: {self.max_players}"
        FONTS['normal'].render_to(
            self.screen,
            (self.WIDTH // 2 - 100, 290),
            players_text,
            COLORS['text_primary']
        )
        
        # Server connection status
        if self.server_ip:
            status_text = f"Verbunden mit: {self.server_ip}"
            FONTS['small'].render_to(
                self.screen,
                (50, 50),
                status_text,
                COLORS['success']
            )
        
        # Enter key hint
        hint_text = "Tipp: Drücke Enter zum Spielstart"
        FONTS['small'].render_to(
            self.screen,
            (self.WIDTH // 2 - 100, self.HEIGHT - 50),
            hint_text,
            COLORS['text_secondary']
        )
    
    def render_game(self, snapshot=None, events=None):
        """Rendert das Spielfeld"""
        if not snapshot:
            # Show waiting message
            self.widget_manager.show_widgets('game')
            self.widget_manager.hide_widgets('main_menu', 'host_game')
            
            FONTS['subtitle'].render_to(
                self.screen,
                (50, 50),
                f"Spiel: {self.game_name}",
                COLORS['text_primary']
            )
            
            FONTS['normal'].render_to(
                self.screen,
                (50, 100),
                f"Spieler: {self.client_name}",
                COLORS['text_primary']
            )
            
            FONTS['normal'].render_to(
                self.screen,
                (50, 150),
                "Warte auf Spielstart oder andere Spieler...",
                COLORS['warning']
            )
            
            FONTS['small'].render_to(
                self.screen,
                (50, 200),
                "Falls das Spiel nicht startet, prüfe ob der Server läuft.",
                COLORS['text_secondary']
            )
            return None
        
        # Game not fully initialized
        if not self.game_renderer:
            FONTS['normal'].render_to(
                self.screen,
                (50, 250),
                "Lade Spielkomponenten...",
                COLORS['warning']
            )
            return None
        
        # Update game state
        self.game_state.update_initial_phase(snapshot, self.client_name)
        
        self.widget_manager.show_widgets('game')
        self.widget_manager.hide_widgets('main_menu', 'host_game')
        
        # Check if game is over
        game_running = snapshot.get("Running", True)
        end_scores = snapshot.get("End Scores", [])
        
        print(f"DEBUG: game_running = {game_running}, end_scores = {end_scores}")  # Debug output
        
        if not game_running and end_scores:
            print("DEBUG: Showing endscreen overlay")  # Debug output
            # Game is over - show endscreen overlay
            is_my_turn = self.game_state.is_my_turn(snapshot, self.client_name)
            
            # Render normal game components first (as background)
            self.game_renderer.render_game_header(
                snapshot, self.client_name, self.game_name, is_my_turn, 
                self.game_state.initial_phase
            )
            
            # Render piles and get rects for event handling
            draw_rect, discard_rect = self.game_renderer.render_piles(
                snapshot, self.game_state.draw_pile_checked, self.hovered_pile,
                is_my_turn, self.game_state.initial_phase
            )
            
            # Render player cards and get rects for event handling
            self.hovered_card, card_rects = self.game_renderer.render_player_cards(
                snapshot, self.client_name, self.game_state.selected_card,
                is_my_turn, self.game_state.initial_phase, self.game_state.draw_pile_checked
            )
            
            # Render other players
            self.game_renderer.render_other_players(snapshot, self.client_name)
            
            # Render endscreen overlay on top
            play_again_button_rect, exit_button_rect = self.game_renderer.render_endscreen_overlay(
                end_scores, self.client_name, snapshot
            )
            
            # Handle endscreen events
            if events:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if play_again_button_rect and play_again_button_rect.collidepoint(event.pos):
                            # Reset game state and return to main menu for a new game
                            self.game_state.reset_turn_state()
                            self.menu_state = Menu_State.MAIN_MENU
                            return None
                        elif exit_button_rect and exit_button_rect.collidepoint(event.pos):
                            # Exit to main menu
                            self.game_state.reset_turn_state()
                            self.menu_state = Menu_State.MAIN_MENU
                            return None
            
            return None
        
        is_my_turn = self.game_state.is_my_turn(snapshot, self.client_name)
        
        # Reset draw pile state if it's not our turn
        if not is_my_turn and self.game_state.draw_pile_checked:
            self.game_state.reset_draw_pile_state()
        
        # Render game components using GameRenderer
        self.game_renderer.render_game_header(
            snapshot, self.client_name, self.game_name, is_my_turn, 
            self.game_state.initial_phase
        )
        
        instruction_text = self.game_state.get_instruction_text(
            is_my_turn, self.game_state.initial_phase, 
            self.game_state.draw_pile_checked, self.game_state.selected_card
        )
        self.game_renderer.render_game_instructions(
            instruction_text
        )
        
        # Render piles and get rects for event handling
        draw_rect, discard_rect = self.game_renderer.render_piles(
            snapshot, self.game_state.draw_pile_checked, self.hovered_pile,
            is_my_turn, self.game_state.initial_phase
        )
        
        # Render player cards and get rects for event handling
        self.hovered_card, card_rects = self.game_renderer.render_player_cards(
            snapshot, self.client_name, self.game_state.selected_card,
            is_my_turn, self.game_state.initial_phase, self.game_state.draw_pile_checked
        )
        
        # Render other players
        self.game_renderer.render_other_players(snapshot, self.client_name)
        
        # Render action buttons and get flip button rect
        flip_button_rect = self.game_renderer.render_action_buttons(
            self.game_state.selected_card, self.game_state.initial_phase,
            is_my_turn, self.game_state.draw_pile_checked
        )
        
        # Handle events using EventHandler
        if events:
            # Handle flip button click
            flip_action = self.event_handler.handle_flip_button_click(
                events, flip_button_rect, self.game_state.selected_card
            )
            if flip_action == "flip_card":
                action = self.game_state.process_card_action(
                    "flip_card", self.game_state.selected_card['position']
                )
                if action:
                    self.game_state.clear_selection()  # Reset selection after command
                    return action
            
            # Handle pile clicks for draw pile
            pile_action = self.event_handler.handle_pile_click(
                events, draw_rect, discard_rect, self.game_state.selected_card,
                is_my_turn, self.game_state.initial_phase, self.game_state.draw_pile_checked
            )
            if pile_action == "draw_pile_click":
                self.game_state.draw_pile_checked = True
                return ("Check Draw Pile", True)
            elif pile_action == "draw_pile_swap":
                if self.game_state.selected_card['position']:
                    pos = self.game_state.selected_card['position']
                    self.game_state.clear_selection()
                    self.game_state.draw_pile_checked = False  # Reset draw pile state after swap
                    return ("Take from Draw Pile", pos)
            elif pile_action == "discard_pile_swap":
                if self.game_state.selected_card['position']:
                    pos = self.game_state.selected_card['position']
                    self.game_state.clear_selection()
                    return ("Take from Discard Pile", pos)
            
            # Handle card clicks
            card_action = self.event_handler.handle_game_card_click(
                events, card_rects, self.game_state.selected_card,
                is_my_turn, self.game_state.initial_phase, self.game_state.draw_pile_checked
            )
            
            # Process card actions
            if card_action == "clear_selection":
                self.game_state.clear_selection()
            elif card_action and len(card_action) >= 2:
                action_type = card_action[0]
                position = card_action[1]
                action_param = card_action[2] if len(card_action) > 2 else None
                
                if action_type == "select_card":
                    self.game_state.set_selection(position, action_param)
            
            # Update hover state
            self.hovered_card, self.hovered_pile = self.event_handler.update_hover_state(
                events, card_rects, draw_rect, discard_rect, 
                is_my_turn, self.game_state.initial_phase
            )
        
        return None
    
    # =================== EVENT HANDLERS ===================
    
    def _on_connect_clicked(self):
        """Verbindung zum Server"""
        self.server_ip = self.widget_manager.get_widget_text('main_menu', 'ip_textbox').strip()
        if not self.server_ip:
            return
        
        if self._test_server_connection():
            self.menu_state = Menu_State.HOST_GAME
    
    def _on_start_clicked(self):
        """Startet das Spiel"""
        self.client_name = self.widget_manager.get_widget_text('host_game', 'name_textbox').strip()
        self.game_name = self.widget_manager.get_widget_text('host_game', 'game_textbox').strip()
        
        if not self.client_name or not self.game_name:
            print("Fehler: Name oder Spielname ist leer")
            return
        
        try:
            print(f"Verbinde zu Server: {self.server_ip}:65111")
            print(f"Spieler: {self.client_name}, Spiel: {self.game_name}, Max Players: {self.max_players}")
            
            self.sock = network.connect_to_server(
                self.client_name, self.game_name, self.max_players, self.server_ip
            )
            
            if self.sock:
                self.sock.settimeout(2.0)  # Increase timeout to 2 seconds
                self.menu_state = Menu_State.GAME
                print("Erfolgreich verbunden!")
                
        except Exception as e:
            print(f"Fehler beim Verbinden: {e}")
            self.sock = None
    
    def _on_back_clicked(self):
        """Zurück zum Hauptmenü"""
        # Reset state first
        self.server_ip = ""
        self.client_name = ""
        self.game_name = ""
        self.sock = None
        
        # Change menu state
        self.menu_state = Menu_State.MAIN_MENU
        
        # Reset main menu widgets
        self._reset_main_menu_widgets()
    
    def _reset_main_menu_widgets(self):
        """Resettet Main Menu Widgets"""
        self.widget_manager.set_widget_text('main_menu', 'ip_textbox', "")
    
    def _reset_host_game_widgets(self):
        """Resettet Host Game Widgets"""
        self.widget_manager.set_widget_text('host_game', 'name_textbox', "")
        self.widget_manager.set_widget_text('host_game', 'game_textbox', "")
    
    def _on_exit_clicked(self):
        """Spiel beenden"""
        self.running = False
    
    # =================== UTILITY METHODS ===================
    
    def _test_server_connection(self):
        """Testet Serververbindung"""
        try:
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_sock.settimeout(2.0)
            test_sock.connect((self.server_ip, 65111))
            test_sock.close()
            return True
        except Exception as e:
            print(f"Verbindungstest fehlgeschlagen: {e}")
            return False
    
    def get_state(self):
        """Gibt aktuellen GUI-Zustand zurück"""
        return {
            "menu_state": self.menu_state,
            "client_name": self.client_name,
            "game_name": self.game_name,
            "server_ip": self.server_ip,
            "sock": self.sock,
            "quitting": not self.running
        }
    
    def get_action(self):
        """Gibt und resettet die aktuelle Aktion"""
        action = self.game_state.current_action
        if action:
            self.game_state.reset_after_action()  # Reset selection and action after retrieval
        return action
    
    def reset_game_state(self):
        """Resettet Spielzustand"""
        self.game_state.reset_turn_state()
        self.hovered_card = None
        self.hovered_pile = None
