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
            
            # Store button rect for click detection
            self.flip_button_rect = button_rect
        else:
            self.flip_button_rect = None
    
    def _render_game_header(self, snapshot, is_my_turn):
        """Rendert Game Header"""
        # Game Title
        title_text = f"Spiel: {self.game_name}"
        FONTS['subtitle'].render_to(
            self.screen,
            (50, 30),
            title_text,
            COLORS['text_primary']
        )
        
        # Player Status
        if self.initial_phase:
            my_player = self._get_my_player(snapshot)
            if my_player:
                flipped_count = self._count_flipped_cards(my_player)
                status_text = f"Spieler: {self.client_name} - SPIELSTART: {flipped_count}/2 Karten aufgedeckt"
                color = COLORS['warning'] if flipped_count < 2 else COLORS['success']
            else:
                status_text = f"Spieler: {self.client_name} - SPIELSTART: Warte auf Spielerinfo..."
                color = COLORS['text_secondary']
        else:
            status_text = f"Spieler: {self.client_name}"
            if self.card_in_hand:
                status_text += " (Karte in der Hand)"
            color = COLORS['accent'] if self.card_in_hand else COLORS['text_primary']
        
        FONTS['normal'].render_to(
            self.screen,
            (50, 70),
            status_text,
            color
        )
        
        # Turn Status
        active_player = snapshot.get("Active")
        if is_my_turn:
            turn_text = "Du bist am Zug!"
            color = COLORS['success']
        elif active_player:
            turn_text = f"{active_player} ist am Zug"
            color = COLORS['text_secondary']
        else:
            turn_text = "Kein aktiver Spieler (alle decken Karten auf)"
            color = COLORS['warning']
        
        FONTS['normal'].render_to(
            self.screen,
            (50, 110),
            turn_text,
            color
        )
    
    def _render_action_selection_status(self, is_my_turn):
        """Rendert den Status der Aktionsauswahl"""
        if self.initial_phase:
            return  # No action selection needed in initial phase
            
        if not is_my_turn:
            return  # No action selection needed when not our turn
            
        # Action selection status box
        status_y = 150
        status_height = 40
        
        pygame.draw.rect(self.screen, COLORS['button_bg'], 
                        (50, status_y, self.WIDTH - 100, status_height), border_radius=5)
        
        if self.selected_action_type:
            action_names = {
                "flip": "Karte umdrehen",
                "draw": "Ziehen vom Nachziehstapel", 
                "discard": "Nehmen vom Ablagestapel"
            }
            status_text = f"Gewählte Aktion: {action_names.get(self.selected_action_type, 'Unbekannt')}"
            color = COLORS['success']
        else:
            status_text = "Keine Aktion gewählt - Wähle eine Aktion mit den Buttons unten"
            color = COLORS['warning']
            
        FONTS['normal'].render_to(
            self.screen,
            (60, status_y + 10),
            status_text,
            color
        )
    
    def _render_action_button_highlights(self):
        """Rendert Highlights für die ausgewählte Aktion"""
        if not self.selected_action_type or self.initial_phase:
            return
            
        # Get button positions from the game widgets
        button_map = {
            "flip": "flip_action_button",
            "draw": "draw_action_button", 
            "discard": "discard_action_button"
        }
        
        button_name = button_map.get(self.selected_action_type)
        if button_name and button_name in self.widgets['game']:
            # Recreate the position calculation with updated values
            action_button_y = self.HEIGHT - 160
            action_button_width = 150
            action_spacing = action_button_width + 30
            center_x = self.WIDTH // 2
            action_start_x = center_x - (3 * action_spacing) // 2
            
            button_positions = {
                "flip_action_button": action_start_x,
                "draw_action_button": action_start_x + action_spacing,
                "discard_action_button": action_start_x + 2 * action_spacing
            }
            
            if button_name in button_positions:
                button_x = button_positions[button_name]
                # Draw a highlight border around the selected button
                pygame.draw.rect(self.screen, COLORS['selected'], 
                               (button_x - 3, action_button_y - 3, action_button_width + 6, 41), 3)
    
    def _render_game_instructions(self, is_my_turn):
        """Rendert Spielanweisungen"""
        if self.initial_phase:
            # In initial phase, show flipping instructions
            instruction = "SPIELSTART: Decke 2 Karten auf! Klicke auf verdeckte Karten und dann 'Karte umdrehen'. Rechtsklick = Auswahl löschen"
            color = COLORS['success']
        elif not is_my_turn:
            instruction = "Warte auf deinen Zug..."
            color = COLORS['text_secondary']
        elif self.draw_pile_checked:
            if self.selected_card_for_flip:
                instruction = f"Nachziehstapel aufgedeckt → Verdeckte Karte an Position ({self.selected_card_for_flip[0]}, {self.selected_card_for_flip[1]}) ausgewählt zum Umdrehen"
            elif self.selected_position:
                instruction = f"Nachziehstapel aufgedeckt → Aufgedeckte Karte an Position ({self.selected_position[0]}, {self.selected_position[1]}) wird getauscht"
            else:
                instruction = "Nachziehstapel aufgedeckt → Wähle eine Karte: Verdeckte zum Umdrehen, Aufgedeckte zum Tauschen"
            color = COLORS['warning']
        elif self.card_in_hand:
            instruction = "Du hast eine Karte → Klicke auf eine Position um sie zu platzieren"
            color = COLORS['accent']
        elif self.selected_position:
            instruction = f"Position ({self.selected_position[0]}, {self.selected_position[1]}) ausgewählt → Klicke auf Ablagestapel zum Tauschen"
            color = COLORS['warning']
        elif self.selected_card_for_flip:
            instruction = f"Verdeckte Karte an Position ({self.selected_card_for_flip[0]}, {self.selected_card_for_flip[1]}) ausgewählt → Klicke 'Karte umdrehen' oder wähle Ablagestapel"
            color = COLORS['accent']
        else:
            instruction = "Dein Zug: Klicke auf Nachziehstapel um zu beginnen, oder wähle eine Karte für den Ablagestapel"
            color = COLORS['text_primary']
        
        # Instruction Box
        instruction_y = self.HEIGHT - 140
        pygame.draw.rect(self.screen, COLORS['button_bg'], 
                        (20, instruction_y - 10, self.WIDTH - 40, 40), border_radius=5)
        
        FONTS['normal'].render_to(
            self.screen,
            (30, instruction_y),
            instruction,
            color
        )
    
    def _render_piles(self, snapshot, events, is_my_turn):
        """Rendert Draw und Discard Pile"""
        # Store snapshot for hover checking
        self._current_snapshot = snapshot
        
        pile_y = 300
        draw_x = self.WIDTH - 300
        discard_x = self.WIDTH - 450
        
        # Draw Pile
        draw_pile = snapshot.get("Draw Pile", [])
        if draw_pile:
            # Get the top card of the draw pile
            top_card = draw_pile[0] if draw_pile else None
            
            # Check if draw pile is checked (top card visible)
            self.draw_pile_checked = top_card and top_card.get_visible()
            
            # Show the card face if it's visible, otherwise show the back
            if self.draw_pile_checked:
                draw_image = self.card_images.get(str(top_card.get_value()))
                label_text = "Nachziehstapel"
            else:
                draw_image = self.card_images.get("back")
                label_text = "Nachziehstapel"
            
            if draw_image:
                draw_rect = pygame.Rect(draw_x, pile_y, LAYOUT['card_width'], LAYOUT['card_height'])
                self.screen.blit(draw_image, draw_rect)
                
                # Hover highlight - different logic based on state
                if (self.hovered_pile == "draw" and is_my_turn and not self.initial_phase and 
                    (not self.draw_pile_checked or self.selected_position or self.selected_card_for_flip)):
                    pygame.draw.rect(self.screen, COLORS['accent'], draw_rect, 4)
                    # Tooltip based on draw pile state
                    if self.draw_pile_checked and self.selected_position:
                        tooltip_text = "Klicken: Karte tauschen"
                    elif self.draw_pile_checked:
                        tooltip_text = "Aufgedeckt - Wähle Karte zum Tauschen oder Umdrehen"
                    else:
                        tooltip_text = "Klicken: Nachziehstapel aufdecken"
                    
                    FONTS['small'].render_to(
                        self.screen,
                        (draw_x, pile_y + LAYOUT['card_height'] + 5),
                        tooltip_text,
                        COLORS['accent']
                    )
                
                # Label with state info
                label_color = COLORS['warning'] if self.draw_pile_checked else COLORS['text_primary']
                FONTS['small'].render_to(
                    self.screen,
                    (draw_x, pile_y - 25),
                    label_text,
                    label_color
                )
                
                # Click handling - updated logic for new game rules
                if (events and is_my_turn and not self.initial_phase):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if draw_rect.collidepoint(event.pos):
                                if not self.draw_pile_checked:
                                    # Check/reveal the draw pile - no position selection needed yet
                                    print("Checking draw pile...")
                                    return ("Check Draw Pile", True)
                                else:
                                    # Draw pile is checked - check if a position is selected for swapping
                                    if self.selected_position:
                                        print(f"Taking from draw pile to position {self.selected_position}")
                                        self.card_in_hand = True
                                        action = ("Take from Draw Pile", self.selected_position)
                                        # Reset selections
                                        self.selected_position = None
                                        self.selected_card_for_flip = None
                                        return action
                                    else:
                                        print("Draw pile already checked - select a card position first")
                                        return None
            else:
                print(f"No image found for draw pile card")
        
        # Discard Pile
        discard_pile = snapshot.get("Discard Pile", [])
        if discard_pile:
            # Server uses discard_pile[0] as the top card, not [-1]
            top_card = discard_pile[0]
            discard_image = self.card_images.get(str(top_card.get_value()))
            if discard_image:
                discard_rect = pygame.Rect(discard_x, pile_y, LAYOUT['card_width'], LAYOUT['card_height'])
                self.screen.blit(discard_image, discard_rect)
                
                # Hover highlight
                if (self.hovered_pile == "discard" and is_my_turn and not self.initial_phase and 
                    (self.selected_position or self.selected_card_for_flip)):
                    pygame.draw.rect(self.screen, COLORS['accent'], discard_rect, 4)
                    # Tooltip
                    tooltip_text = "Klicken: Karte nehmen und tauschen"
                    
                    FONTS['small'].render_to(
                        self.screen,
                        (discard_x, pile_y + LAYOUT['card_height'] + 5),
                        tooltip_text,
                        COLORS['accent']
                    )
                
                # Label
                FONTS['small'].render_to(
                    self.screen,
                    (discard_x, pile_y - 25),
                    "Ablagestapel",
                    COLORS['text_primary']
                )
                
                # Click handling - requires position selection first
                if (events and is_my_turn and not self.initial_phase):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if discard_rect.collidepoint(event.pos):
                                # Check if either a position or card for flip is selected
                                target_position = self.selected_position or self.selected_card_for_flip
                                if target_position:
                                    print(f"Taking from discard pile to position {target_position}")
                                    self.card_in_hand = True
                                    action = ("Take from Discard Pile", target_position)
                                    # Reset selections
                                    self.selected_position = None
                                    self.selected_card_for_flip = None
                                    return action
                                else:
                                    print("Bitte zuerst eine Position zum Tauschen auswählen")
                                    return None
            else:
                print(f"No image found for discard pile card value: {top_card.get_value()}")
        
        return None
    
    def _render_player_cards(self, snapshot, events, is_my_turn):
        """Rendert die Karten des aktuellen Spielers"""
        players = snapshot.get("Players", [])
        current_player = None
        
        for player in players:
            if player.name == self.client_name:
                current_player = player
                break
        
        if not current_player:
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
        # Card grid positioning
        grid_start_x = 50
        grid_start_y = 200
        card_spacing = LAYOUT['card_spacing']
        
        # Get mouse position but don't reset hover state yet
        mouse_pos = pygame.mouse.get_pos()
        current_hovered_card = None
        
        # Add right-click to clear selections
        if events:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                    print("Right click detected - clearing all selections")
                    self.selected_position = None
                    self.selected_card_for_flip = None
        
        card_deck = current_player.card_deck
        for row_idx, card_row in enumerate(card_deck):
            for col_idx, card in enumerate(card_row):
                x = grid_start_x + col_idx * (LAYOUT['card_width'] + card_spacing)
                y = grid_start_y + row_idx * (LAYOUT['card_height'] + card_spacing)
                
                # Check if card was removed (three in a column)
                if card is None:
                    # Render empty space for removed card
                    card_rect = pygame.Rect(x, y, LAYOUT['card_width'], LAYOUT['card_height'])
                    # Draw a subtle border to show where the card was
                    pygame.draw.rect(self.screen, COLORS['text_secondary'], card_rect, 2)
                    # Draw an X or some indicator
                    pygame.draw.line(self.screen, COLORS['text_secondary'], 
                                   (x + 10, y + 10), (x + LAYOUT['card_width'] - 10, y + LAYOUT['card_height'] - 10), 3)
                    pygame.draw.line(self.screen, COLORS['text_secondary'], 
                                   (x + LAYOUT['card_width'] - 10, y + 10), (x + 10, y + LAYOUT['card_height'] - 10), 3)
                    
                    # Check for hover and handle mouse events for removed cards
                    if events:
                        for event in events:
                            if event.type == pygame.MOUSEMOTION:
                                if card_rect.collidepoint(event.pos):
                                    current_hovered_card = (row_idx, col_idx, None)
                    
                    # Check if mouse is currently over this removed card
                    if card_rect.collidepoint(mouse_pos):
                        current_hovered_card = (row_idx, col_idx, None)
                    
                    # Show tooltip on hover for removed cards
                    if (current_hovered_card and current_hovered_card[0] == row_idx and 
                        current_hovered_card[1] == col_idx and current_hovered_card[2] is None):
                        FONTS['small'].render_to(
                            self.screen,
                            (x, y + LAYOUT['card_height'] + 5),
                            "Karte entfernt (3 gleiche in Spalte)",
                            COLORS['text_secondary']
                        )
                    continue
                
                # Get card image for normal cards
                if card.get_visible():
                    card_image = self.card_images.get(str(card.get_value()))
                else:
                    card_image = self.card_images.get("back")
                
                if card_image:
                    card_rect = pygame.Rect(x, y, LAYOUT['card_width'], LAYOUT['card_height'])
                    self.screen.blit(card_image, card_rect)
                    
                    # Highlight selected position
                    if self.selected_position == (row_idx, col_idx):
                        pygame.draw.rect(self.screen, COLORS['selected'], card_rect, 4)
                    
                    # Highlight selected card for flipping
                    if self.selected_card_for_flip == (row_idx, col_idx):
                        pygame.draw.rect(self.screen, COLORS['selected'], card_rect, 4)
                    
                    # Check if mouse is currently over this card
                    if card_rect.collidepoint(mouse_pos):
                        current_hovered_card = (row_idx, col_idx, card)
                    
                    # Hover highlights and tooltips for intuitive interaction
                    if current_hovered_card and current_hovered_card[0] == row_idx and current_hovered_card[1] == col_idx:
                        if self.initial_phase:
                            if not card.get_visible():
                                pygame.draw.rect(self.screen, COLORS['success'], card_rect, 3)
                                FONTS['small'].render_to(
                                    self.screen,
                                    (x, y + LAYOUT['card_height'] + 5),
                                    "Klicken: Für Umdrehen auswählen",
                                    COLORS['success']
                                )
                            else:
                                pygame.draw.rect(self.screen, COLORS['text_secondary'], card_rect, 2)
                                FONTS['small'].render_to(
                                    self.screen,
                                    (x, y + LAYOUT['card_height'] + 5),
                                    "Bereits aufgedeckt",
                                    COLORS['text_secondary']
                                )
                        elif is_my_turn:
                            if self.draw_pile_checked:
                                # Special mode: draw pile is checked, allow both flipping and swapping
                                if not card.get_visible():
                                    # Hidden card - can be flipped
                                    pygame.draw.rect(self.screen, COLORS['success'], card_rect, 3)
                                    FONTS['small'].render_to(
                                        self.screen,
                                        (x, y + LAYOUT['card_height'] + 5),
                                        "Klicken: Zum Umdrehen auswählen",
                                        COLORS['success']
                                    )
                                else:
                                    # Visible card - can be swapped
                                    pygame.draw.rect(self.screen, COLORS['warning'], card_rect, 3)
                                    FONTS['small'].render_to(
                                        self.screen,
                                        (x, y + LAYOUT['card_height'] + 5),
                                        "Klicken: Zum Tauschen auswählen",
                                        COLORS['warning']
                                    )
                            elif not card.get_visible():
                                pygame.draw.rect(self.screen, COLORS['success'], card_rect, 3)
                                FONTS['small'].render_to(
                                    self.screen,
                                    (x, y + LAYOUT['card_height'] + 5),
                                    "Klicken: Umdrehen oder für Ablagestapel wählen",
                                    COLORS['success']
                                )
                            elif card.get_visible() and not self.card_in_hand:
                                pygame.draw.rect(self.screen, COLORS['warning'], card_rect, 3)
                                FONTS['small'].render_to(
                                    self.screen,
                                    (x, y + LAYOUT['card_height'] + 5),
                                    "Klicken: Für Tausch mit Ablagestapel wählen",
                                    COLORS['warning']
                                )
                            elif self.card_in_hand:
                                pygame.draw.rect(self.screen, COLORS['accent'], card_rect, 3)
                                FONTS['small'].render_to(
                                    self.screen,
                                    (x, y + LAYOUT['card_height'] + 5),
                                    "Klicken: Karte platzieren",
                                    COLORS['accent']
                                )
                        else:
                            # Not my turn, but show hover feedback
                            pygame.draw.rect(self.screen, COLORS['text_secondary'], card_rect, 2)
                            FONTS['small'].render_to(
                                self.screen,
                                (x, y + LAYOUT['card_height'] + 5),
                                "Nicht dein Zug",
                                COLORS['text_secondary']
                            )
                    
                    # Click handling - check conditions more thoroughly
                    if events:
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                if card_rect.collidepoint(event.pos):
                                    print(f"Card clicked at ({row_idx}, {col_idx}) - is_my_turn: {is_my_turn}, initial_phase: {self.initial_phase}")
                                    
                                    # Allow interaction in initial phase or on our turn
                                    if self.initial_phase or is_my_turn:
                                        return self._handle_card_click(row_idx, col_idx, card)
                                    else:
                                        print("Not your turn and not in initial phase")
                                        return None
                            elif event.type == pygame.MOUSEMOTION:
                                if card_rect.collidepoint(event.pos):
                                    current_hovered_card = (row_idx, col_idx, card)
        
        # Update hover state at the end
        self.hovered_card = current_hovered_card
        
        return None
    
    def _handle_card_click(self, row, col, card):
        """Behandelt Kartenklicks"""
        # Don't allow interaction with removed cards
        if card is None:
            print(f"Cannot interact with removed card at ({row}, {col})")
            return None
            
        if self.initial_phase:
            # In initial phase, select cards for flipping (don't flip immediately)
            if not card.get_visible():
                print(f"Selected card at ({row}, {col}) for flipping during initial phase")
                # Reset any previous selections to avoid multiple selections
                self.selected_position = None
                self.selected_card_for_flip = (row, col)
                return None
            else:
                print("Card already visible during initial phase - cannot flip again")
                return None
        
        elif self.draw_pile_checked:
            # Special mode: draw pile is checked, player can choose between swap or flip
            # Allow both actions for ALL cards (visible and hidden)
            if not card.get_visible():
                # Hidden card - can be flipped
                print(f"Draw pile checked - choosing to flip hidden card at ({row}, {col})")
                self.selected_card_for_flip = (row, col)
                self.selected_position = None
                return None
            else:
                # Visible card - can be swapped (set position for swapping, don't execute immediately)
                print(f"Draw pile checked - choosing to swap visible card at ({row}, {col})")
                self.selected_position = (row, col)
                self.selected_card_for_flip = None
                # Don't execute the action immediately, let the user confirm by clicking draw pile again
                return None
        
        elif self.card_in_hand:
            # Player has card in hand - place it
            print(f"Placing card at position ({row}, {col})")
            self.card_in_hand = False
            self.selected_position = None
            self.selected_card_for_flip = None
            return None  # Server handles placement automatically
        
        elif not card.get_visible():
            # Face-down card in normal game phase - can be flipped OR selected for discard pile swap
            print(f"Selected face-down card at ({row}, {col}) - can be flipped or swapped with discard pile")
            # Reset any previous selections to avoid multiple selections
            self.selected_position = None
            self.selected_card_for_flip = (row, col)
            return None
        
        else:
            # Face-up card in normal game phase - can be selected for discard pile swap
            print(f"Selected face-up card at ({row}, {col}) for discard pile swap")
            # Reset any previous selections to avoid multiple selections
            self.selected_card_for_flip = None
            self.selected_position = (row, col)
            return None
    
    def _render_other_players(self, snapshot):
        """Rendert andere Spieler"""
        players = snapshot.get("Players", [])
        other_players = [p for p in players if p.name != self.client_name]
        
        start_x = self.WIDTH - 600
        start_y = 50
        
        for i, player in enumerate(other_players):
            y_offset = i * 120
            
            # Player name
            FONTS['normal'].render_to(
                self.screen,
                (start_x, start_y + y_offset),
                f"Spieler: {player.name}",
                COLORS['text_primary']
            )
            
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
            return
        
        try:
            self.sock = network.connect_to_server(
                self.client_name, self.game_name, self.max_players, self.server_ip
            )
            
            if self.sock:
                self.sock.settimeout(2.0)  # Increase timeout to 2 seconds
                self.menu_state = Menu_State.GAME
                
        except Exception as e:
            pass
    
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
            test_sock.connect((self.server_ip, 65432))
            test_sock.close()
            return True
        except Exception:
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
