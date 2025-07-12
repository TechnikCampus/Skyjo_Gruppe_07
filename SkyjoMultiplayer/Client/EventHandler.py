"""
Event Handler - Handles all pygame event processing for the game
"""

import pygame
from Common import card


class EventHandler:
    def __init__(self, screen, colors, layout):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.COLORS = colors
        self.LAYOUT = layout
    
    def handle_game_card_click(self, events, card_rects, selected_card, is_my_turn, 
                              initial_phase, draw_pile_checked):
        """Behandelt Klicks auf Spielerkarten"""
        if not events:
            return None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                for (pos, rect, card_obj) in card_rects:
                    if rect.collidepoint(event.pos):
                        return self._handle_card_selection(
                            pos, card_obj, is_my_turn, 
                            initial_phase, draw_pile_checked
                        )
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                # Clear selection on right click
                return "clear_selection"
        
        return None
    
    def handle_pile_click(self, events, draw_rect, discard_rect, selected_card, 
                         is_my_turn, initial_phase, draw_pile_checked):
        """Behandelt Klicks auf Draw- und Discard-Pile"""
        if not events:
            return None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                # Draw pile click
                if draw_rect and draw_rect.collidepoint(event.pos):
                    if is_my_turn and not initial_phase:
                        if not draw_pile_checked:
                            return "draw_pile_click"
                        elif selected_card['position'] and (selected_card['action'] == 'swap_and_flip' or selected_card['action'] == 'swap'):
                            return "draw_pile_swap"
                
                # Discard pile click
                if discard_rect and discard_rect.collidepoint(event.pos):
                    if selected_card['position'] and (selected_card['action'] == 'swap' or selected_card['action'] == 'swap_and_flip'):
                        return "discard_pile_swap"
        
        return None
    
    def handle_flip_button_click(self, events, flip_button_rect, selected_card):
        """Behandelt Klicks auf den Flip-Button"""
        if not events or not flip_button_rect:
            return None
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if flip_button_rect.collidepoint(event.pos):
                    if selected_card['position'] and (selected_card['action'] == 'flip' or selected_card['action'] == 'swap_and_flip'):
                        return "flip_card"
        
        return None
    
    def update_hover_state(self, events, card_rects, draw_rect, discard_rect, 
                          is_my_turn, initial_phase):
        """Aktualisiert den Hover-Status basierend auf Mausposition"""
        if not events:
            return None, None
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Check card hover
        hovered_card = None
        for (pos, rect, card_obj) in card_rects:
            if rect.collidepoint(mouse_pos):
                hovered_card = (pos[0], pos[1], card_obj)
                break
        
        # Check pile hover
        hovered_pile = None
        if draw_rect and draw_rect.collidepoint(mouse_pos):
            if is_my_turn and not initial_phase:
                hovered_pile = "draw"
        elif discard_rect and discard_rect.collidepoint(mouse_pos):
            if is_my_turn and not initial_phase:
                hovered_pile = "discard"
        
        return hovered_card, hovered_pile
    
    def _handle_card_selection(self, pos, card_obj, is_my_turn, 
                              initial_phase, draw_pile_checked):
        
        # Handle removed cards (None)
        if card_obj is None:
            return None
        
        # Initial phase: Allow flipping face-down cards
        if initial_phase:
            if not card_obj.get_visible():
                return ("select_card", pos, "flip")
            else:
                return None  # Can't select face-up cards during initial phase
        
        # Not my turn: no selection allowed
        if not is_my_turn:
            return None
        
        # Normal turn logic
        if draw_pile_checked:
            # After drawing, can select face-down cards to flip or face-up to swap
            if not card_obj.get_visible():
                return ("select_card", pos, "swap_and_flip")
            else:
                return ("select_card", pos, "swap")
        else:
            # Before drawing, can select both face-up and face-down cards for discard pile swap
            return ("select_card", pos, "swap")
    
    def get_card_interaction_type(self, card_obj, is_my_turn, initial_phase, 
                                 draw_pile_checked):
        """Bestimmt den Interaktionstyp für eine Karte"""
        if card_obj is None:
            return None
        
        if initial_phase:
            return "flip" if not card_obj.get_visible() else None
        
        if not is_my_turn:
            return None
        
        if draw_pile_checked:
            return "swap_and_flip" if not card_obj.get_visible() else "swap"
        
        # Before drawing, both face-up and face-down cards can be swapped with discard pile
        return "swap"
