"""
Game Renderer - Handles all game-related rendering (cards, piles, players)
"""

import pygame
from pygame import freetype
from Common import card

class GameRenderer:
    def __init__(self, screen, colors, fonts, layout, card_images):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.COLORS = colors
        self.FONTS = fonts
        self.LAYOUT = layout
        self.card_images = card_images
    
    def render_game_header(self, snapshot, client_name, game_name, is_my_turn, initial_phase):
        """Rendert Game Header"""
        # Game Title
        title_text = f"Spiel: {game_name}"
        self.FONTS['subtitle'].render_to(
            self.screen,
            (50, 30),
            title_text,
            self.COLORS['text_primary']
        )

        player = self._get_my_player(snapshot, client_name)
        
        # Player Status
        self.FONTS['normal'].render_to(
            self.screen,
            (50, 70),
            f"Spieler: {client_name}",
            self.COLORS['text_primary']
        )
        if player:
            # Player Status
            self.FONTS['normal'].render_to(
                self.screen,
                (50, 100),
                f"Scorer: {player.visible_round_score}",
                self.COLORS['text_primary']
            )
        
        # Turn Status
        active_player = snapshot.get("Active")
        if is_my_turn:
            turn_text = "Du bist am Zug!"
            color = self.COLORS['success']
        elif active_player:
            turn_text = f"{active_player} ist am Zug"
            color = self.COLORS['text_secondary']
        else:
            turn_text = "Kein aktiver Spieler (alle decken Karten auf)"
            color = self.COLORS['warning']
        
        self.FONTS['normal'].render_to(
            self.screen,
            (50, 130),
            turn_text,
            color
        )
    
    def render_game_instructions(self, instruction_in):
        """Rendert Spielanweisungen"""
        instruction = instruction_in
        color = self.COLORS['text_primary']
        
        # Instruction Box
        instruction_y = self.HEIGHT - 140
        pygame.draw.rect(self.screen, self.COLORS['button_bg'], 
                        (20, instruction_y - 10, self.WIDTH - 40, 40), border_radius=5)
        
        self.FONTS['normal'].render_to(
            self.screen,
            (30, instruction_y),
            instruction,
            color
        )
    
    def render_piles(self, snapshot, draw_pile_checked, hovered_pile, is_my_turn, initial_phase):
        """Rendert Draw und Discard Pile"""
        pile_y = 300
        draw_x = self.WIDTH - 800
        discard_x = self.WIDTH - 950
        
        # Draw Pile
        draw_pile = snapshot.get("Draw Pile", [])
        draw_rect = None
        if draw_pile:
            top_card = draw_pile[0] if draw_pile else None
            
            if draw_pile_checked:
                draw_image = self.card_images.get(str(top_card.get_value()))
                label_text = "Nachziehstapel"
            else:
                draw_image = self.card_images.get("back")
                label_text = "Nachziehstapel"
            
            if draw_image:
                draw_rect = pygame.Rect(draw_x, pile_y, self.LAYOUT['card_width'], self.LAYOUT['card_height'])
                self.screen.blit(draw_image, draw_rect)
                
                # Hover highlight
                if (hovered_pile == "draw" and is_my_turn and not initial_phase):
                    pygame.draw.rect(self.screen, self.COLORS['selected'], draw_rect, 4)
                
                # Label
                label_color = self.COLORS['warning'] if draw_pile_checked else self.COLORS['text_primary']
                self.FONTS['small'].render_to(
                    self.screen,
                    (draw_x, pile_y - 25),
                    label_text,
                    label_color
                )
        
        # Discard Pile
        discard_pile = snapshot.get("Discard Pile", [])
        discard_rect = None
        if discard_pile:
            top_card = discard_pile[0]
            discard_image = self.card_images.get(str(top_card.get_value()))
            if discard_image:
                discard_rect = pygame.Rect(discard_x, pile_y, self.LAYOUT['card_width'], self.LAYOUT['card_height'])
                self.screen.blit(discard_image, discard_rect)
                
                # Hover highlight
                if (hovered_pile == "discard" and is_my_turn and not initial_phase):
                    pygame.draw.rect(self.screen, self.COLORS['selected'], discard_rect, 4)
                
                # Label
                self.FONTS['small'].render_to(
                    self.screen,
                    (discard_x, pile_y - 25),
                    "Ablagestapel",
                    self.COLORS['text_primary']
                )
        
        return draw_rect, discard_rect
    
    def render_player_cards(self, snapshot, client_name, selected_card, is_my_turn, 
                          initial_phase, draw_pile_checked):
        """Rendert die Karten des aktuellen Spielers"""
        players = snapshot.get("Players", [])
        current_player = None
        
        for player in players:
            if player.name == client_name:
                current_player = player
                break
        
        if not current_player:
            return None, []
        
        # Card grid positioning
        grid_start_x = 50
        grid_start_y = 200
        card_spacing = self.LAYOUT['card_spacing']
        
        mouse_pos = pygame.mouse.get_pos()
        current_hovered_card = None
        card_rects = []
        
        card_deck = current_player.card_deck
        for row_idx, card_row in enumerate(card_deck):
            for col_idx, card in enumerate(card_row):
                x = grid_start_x + col_idx * (self.LAYOUT['card_width'] + card_spacing)
                y = grid_start_y + row_idx * (self.LAYOUT['card_height'] + card_spacing)
                
                # Check if card was removed (three in a column)
                if card is None:
                    card_rect = pygame.Rect(x, y, self.LAYOUT['card_width'], self.LAYOUT['card_height'])
                    # Draw a subtle border to show where the card was
                    pygame.draw.rect(self.screen, self.COLORS['text_secondary'], card_rect, 2)
                    # Draw an X
                    pygame.draw.line(self.screen, self.COLORS['text_secondary'], 
                                   (x + 10, y + 10), (x + self.LAYOUT['card_width'] - 10, y + self.LAYOUT['card_height'] - 10), 3)
                    pygame.draw.line(self.screen, self.COLORS['text_secondary'], 
                                   (x + self.LAYOUT['card_width'] - 10, y + 10), (x + 10, y + self.LAYOUT['card_height'] - 10), 3)
                    
                    card_rects.append(((row_idx, col_idx), card_rect, None))
                    
                    if card_rect.collidepoint(mouse_pos):
                        current_hovered_card = (row_idx, col_idx, None)
                    
                    continue
                
                # Get card image for normal cards
                if card.get_visible():
                    card_image = self.card_images.get(str(card.get_value()))
                else:
                    card_image = self.card_images.get("back")
                
                if card_image:
                    card_rect = pygame.Rect(x, y, self.LAYOUT['card_width'], self.LAYOUT['card_height'])
                    self.screen.blit(card_image, card_rect)
                    
                    # Highlight selected card
                    if selected_card['position'] == (row_idx, col_idx):
                        pygame.draw.rect(self.screen, self.COLORS['selected'], card_rect, 4)
                    
                    # Check if mouse is currently over this card
                    if card_rect.collidepoint(mouse_pos):
                        current_hovered_card = (row_idx, col_idx, card)
                    
                    # Hover highlights
                    if current_hovered_card and current_hovered_card[0] == row_idx and current_hovered_card[1] == col_idx:
                        if initial_phase:
                            if not card.get_visible():
                                pygame.draw.rect(self.screen, self.COLORS['selected'], card_rect, 3)
                            else:
                                pygame.draw.rect(self.screen, self.COLORS['selected'], card_rect, 2)
                        elif is_my_turn:
                            if draw_pile_checked:
                                pygame.draw.rect(self.screen, self.COLORS['selected'], card_rect, 3)
                            elif not card.get_visible():
                                pygame.draw.rect(self.screen, self.COLORS['selected'], card_rect, 3)
                            elif card.get_visible():
                                pygame.draw.rect(self.screen, self.COLORS['selected'], card_rect, 3)
                        else:
                            pygame.draw.rect(self.screen, self.COLORS['selected'], card_rect, 2)
                    
                    card_rects.append(((row_idx, col_idx), card_rect, card))
        
        return current_hovered_card, card_rects
    
    def render_other_players(self, snapshot, client_name):
        """Rendert andere Spieler"""
        players = snapshot.get("Players", [])
        other_players = [p for p in players if p.name != client_name]
        
        start_x = self.WIDTH - 400
        start_y = 50
        
        for i, player in enumerate(other_players):
            y_offset = i * 220
            
            # Player name
            self.FONTS['normal'].render_to(
                self.screen,
                (start_x, start_y + y_offset),
                f"Spieler: {player.name}",
                self.COLORS['text_primary']
            )
            #Player score
            self.FONTS['normal'].render_to(
                self.screen,
                (start_x, start_y + y_offset + 30),
                f"Score: {player.visible_round_score}",
                self.COLORS['text_primary']
            )
            
            # Small card grid
            card_size = 25
            for row_idx, card_row in enumerate(player.card_deck):
                for col_idx, card in enumerate(card_row):
                    x = start_x + col_idx * (card_size + 2)
                    y = start_y + y_offset + 60 + row_idx * (card_size + 2)
                    
                    # Handle removed cards (None)
                    if card is None:
                        pygame.draw.rect(self.screen, self.COLORS['button_bg'], (x, y, card_size, card_size))
                        pygame.draw.rect(self.screen, self.COLORS['text_secondary'], (x, y, card_size, card_size), 1)
                        pygame.draw.line(self.screen, self.COLORS['text_secondary'], (x + 5, y + 5), (x + card_size - 5, y + card_size - 5), 1)
                        pygame.draw.line(self.screen, self.COLORS['text_secondary'], (x + card_size - 5, y + 5), (x + 5, y + card_size - 5), 1)
                    elif card.get_visible():
                        color = self.COLORS['card_bg']
                        text_color = self.COLORS['text_primary']
                        text = str(card.get_value())
                        pygame.draw.rect(self.screen, color, (x, y, card_size, card_size))
                        pygame.draw.rect(self.screen, self.COLORS['text_primary'], (x, y, card_size, card_size), 1)
                        
                        if len(text) <= 2:
                            self.FONTS['small'].render_to(
                                self.screen,
                                (x + 2, y + 2),
                                text,
                                text_color
                            )
                    else:
                        color = self.COLORS['text_secondary']
                        text_color = self.COLORS['card_bg']
                        text = "?"
                        pygame.draw.rect(self.screen, color, (x, y, card_size, card_size))
                        pygame.draw.rect(self.screen, self.COLORS['text_primary'], (x, y, card_size, card_size), 1)
                        
                        if len(text) <= 2:
                            self.FONTS['small'].render_to(
                                self.screen,
                                (x + 2, y + 2),
                                text,
                                text_color
                            )
    
    def render_action_buttons(self, selected_card, initial_phase, is_my_turn, draw_pile_checked):
        """Rendert Action Buttons"""
        show_flip_button = (selected_card['position'] and 
                           (selected_card['action'] == 'flip' or selected_card['action'] == 'swap_and_flip') and
                           (initial_phase or (is_my_turn and draw_pile_checked)))
        
        flip_button_rect = None
        if show_flip_button:
            pile_y = 300
            button_x = self.WIDTH - 925
            button_y = pile_y + self.LAYOUT['card_height'] + 40
            button_w = 200
            button_h = 50
            
            # Button background
            button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
            pygame.draw.rect(self.screen, self.COLORS['button_bg'], button_rect)
            pygame.draw.rect(self.screen, self.COLORS['text_primary'], button_rect, 2)
            
            # Button text
            button_text = "Karte umdrehen"
            text_rect = self.FONTS['button'].get_rect(button_text)
            text_x = button_x + (button_w - text_rect.width) // 2
            text_y = button_y + (button_h - text_rect.height) // 2
            
            self.FONTS['button'].render_to(
                self.screen,
                (text_x, text_y),
                button_text,
                self.COLORS['text_primary']
            )
            
            flip_button_rect = button_rect
        
        return flip_button_rect
    
    def render_text(self, position, text, color, font_size=16, centered=False):
        """Rendert Text mit spezifischer Schriftgröße"""
        # Use appropriate font based on size
        if font_size >= 24:
            font = self.FONTS['title']
        elif font_size >= 18:
            font = self.FONTS['subtitle'] 
        else:
            font = self.FONTS['normal']
        
        if centered:
            # Get text dimensions for centering
            text_rect = font.get_rect(text)
            x = position[0] - text_rect.width // 2
            y = position[1]
        else:
            x, y = position
        
        font.render_to(self.screen, (x, y), text, color)

    def _get_my_player(self, snapshot, client_name):
        """Findet den eigenen Spieler im Snapshot"""
        players = snapshot.get("Players", [])
        for player in players:
            if player.name == client_name:
                return player
        return None
    
    def _count_flipped_cards(self, player):
        """Zählt aufgedeckte Karten eines Spielers"""
        flipped_cards = 0
        for row in player.card_deck:
            for card in row:
                if card is not None and card.get_visible():
                    flipped_cards += 1
        return flipped_cards
    
    # Endscreen: Not ready as if now
    '''def render_endscreen_overlay(self, end_scores, client_name, snapshot=None):
        """Rendert das Endscreen-Overlay mit Endergebnissen"""    
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Main endscreen box
        box_width = 600
        box_height = 500
        box_x = (self.WIDTH - box_width) // 2
        box_y = (self.HEIGHT - box_height) // 2
        
        # Background box
        pygame.draw.rect(self.screen, self.COLORS['bg_secondary'], 
                        (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, self.COLORS['text_primary'], 
                        (box_x, box_y, box_width, box_height), 3, border_radius=10)
        
        # Title
        title_y = box_y + 30
        self.render_text(
            (box_x + box_width // 2, title_y),
            "SPIEL BEENDET",
            self.COLORS['accent'],
            font_size=24,
            centered=True
        )
        
        # Sort scores by points (ascending - lower is better)
        sorted_scores = sorted(end_scores, key=lambda x: x[1])
        
        # Winner announcement
        winner_y = title_y + 50
        if sorted_scores:
            winner_name = sorted_scores[0][0]
            winner_score = sorted_scores[0][1]
            if winner_name == client_name:
                winner_text = f"GEWONNEN! Du hast mit {winner_score} Punkten gewonnen!"
                winner_color = self.COLORS['success']
            else:
                winner_text = f"{winner_name} hat mit {winner_score} Punkten gewonnen!"
                winner_color = self.COLORS['warning']
            
            self.render_text(
                (box_x + box_width // 2, winner_y),
                winner_text,
                winner_color,
                font_size=16,
                centered=True
            )
        
        # Game info
        info_y = winner_y + 40
        if snapshot:
            game_round = snapshot.get("Game Round", 0)
            game_name = snapshot.get("Game Name", "Unbekannt")
            self.render_text(
                (box_x + box_width // 2, info_y),
                f"Spiel: {game_name} | Runde: {game_round}",
                self.COLORS['text_secondary'],
                font_size=14,
                centered=True
            )
        
        # Results header
        results_y = info_y + 40
        self.render_text(
            (box_x + 30, results_y),
            "ENDERGEBNISSE:",
            self.COLORS['text_primary'],
            font_size=18
        )
        
        # Player results
        for i, (player_name, score) in enumerate(sorted_scores):
            player_y = results_y + 40 + (i * 40)
            
            # Highlight current player
            if player_name == client_name:
                highlight_rect = pygame.Rect(box_x + 20, player_y - 5, box_width - 40, 35)
                pygame.draw.rect(self.screen, self.COLORS['accent'], highlight_rect, border_radius=5)
                text_color = self.COLORS['bg_primary']
                name_color = self.COLORS['bg_primary']
            else:
                text_color = self.COLORS['text_primary']
                name_color = self.COLORS['text_primary']
            
            # Player name
            self.render_text(
                (box_x + 70, player_y),
                player_name,
                name_color,
                font_size=16
            )
            
            # Score
            score_text = f"{score} Punkte"
            self.render_text(
                (box_x + box_width - 130, player_y),
                score_text,
                text_color,
                font_size=16
            )
        
        # Statistics
        if len(sorted_scores) > 1:
            stats_y = results_y + 40 + len(sorted_scores) * 40 + 20
            self.render_text(
                (box_x + 30, stats_y),
                f"Teilnehmer: {len(sorted_scores)} | Niedrigste Punktzahl: {sorted_scores[0][1]} | Höchste Punktzahl: {sorted_scores[-1][1]}",
                self.COLORS['text_secondary'],
                font_size=12
            )
        
        # Play again button
        button_width = 200
        button_height = 50
        button_x = box_x + (box_width - button_width) // 2
        button_y = box_y + box_height - 80
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, self.COLORS['button_bg'], button_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.COLORS['accent'], button_rect, 3, border_radius=8)
        
        self.render_text(
            (button_x + button_width // 2, button_y + 15),
            "NOCHMAL SPIELEN",
            self.COLORS['text_primary'],
            font_size=16,
            centered=True
        )
        
        # Exit button
        exit_button_width = 150
        exit_button_height = 40
        exit_button_x = box_x + (box_width - exit_button_width) // 2
        exit_button_y = button_y + button_height + 10
        
        exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)
        pygame.draw.rect(self.screen, self.COLORS['bg_primary'], exit_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.COLORS['text_secondary'], exit_button_rect, 2, border_radius=8)
        
        self.render_text(
            (exit_button_x + exit_button_width // 2, exit_button_y + 10),
            "Zum Hauptmenü",
            self.COLORS['text_secondary'],
            font_size=14,
            centered=True
        )
        
        return button_rect, exit_button_rect'''
