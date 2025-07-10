"""
Game State Manager - Handles game state logic and selections
"""

from Common import card


class GameStateManager:
    def __init__(self):
        # Game State
        self.current_action = None
        self.initial_phase = True  # Tracks if we're in initial card-flipping phase
        self.draw_pile_checked = False  # Tracks if draw pile top card is visible
        
        # Simplified card selection system
        self.selected_card = {
            'position': None,  # (row, col) of selected card
            'action': None     # 'flip', 'swap', 'swap_and_flip'
        }
    
    def set_selection(self, position, action):
        """Setzt eine Kartenauswahl"""
        self.selected_card['position'] = position
        self.selected_card['action'] = action
    
    def clear_selection(self):
        """Löscht die aktuelle Kartenauswahl"""
        self.selected_card['position'] = None
        self.selected_card['action'] = None
    
    def get_my_player(self, snapshot, client_name):
        """Findet den eigenen Spieler im Snapshot"""
        players = snapshot.get("Players", [])
        for player in players:
            if player.name == client_name:
                return player
        return None
    
    def count_flipped_cards(self, player):
        """Zählt aufgedeckte Karten eines Spielers"""
        flipped_cards = 0
        for row in player.card_deck:
            for card_obj in row:
                if card_obj is not None and card_obj.get_visible():
                    flipped_cards += 1
        return flipped_cards
    
    def update_initial_phase(self, snapshot, client_name):
        """Aktualisiert den Initial-Phase-Status"""
        my_player = self.get_my_player(snapshot, client_name)
        if my_player:
            flipped_cards = self.count_flipped_cards(my_player)
            self.initial_phase = flipped_cards < 2
        else:
            # If we can't find our player, assume we're in initial phase
            self.initial_phase = True
    
    def is_my_turn(self, snapshot, client_name):
        """Prüft, ob der aktuelle Spieler am Zug ist"""
        active_player = snapshot.get("Active")
        return active_player == client_name
    
    def can_draw_pile_be_clicked(self, is_my_turn, initial_phase, draw_pile_checked):
        """Prüft, ob der Draw-Pile geklickt werden kann"""
        return is_my_turn and not initial_phase and not draw_pile_checked
    
    def can_discard_pile_be_clicked(self, is_my_turn, initial_phase, selected_card):
        """Prüft, ob der Discard-Pile geklickt werden kann"""
        return (is_my_turn and not initial_phase and 
                selected_card['position'] and 
                (selected_card['action'] == 'swap' or selected_card['action'] == 'swap_and_flip'))
    
    def can_card_be_flipped(self, is_my_turn, initial_phase, draw_pile_checked, 
                           selected_card):
        """Prüft, ob eine Karte umgedreht werden kann"""
        return (selected_card['position'] and 
                (selected_card['action'] == 'flip' or selected_card['action'] == 'swap_and_flip') and
                (initial_phase or (is_my_turn and draw_pile_checked)))
    
    def get_instruction_text(self, is_my_turn, initial_phase, draw_pile_checked, 
                            selected_card):
        """Gibt den aktuellen Instruktionstext zurück"""
        if initial_phase:
            return "SPIELSTART: Decke 2 Karten auf! Klicke auf verdeckte Karten und dann 'Karte umdrehen'. Rechtsklick = Auswahl löschen"
        elif not is_my_turn:
            return "Warte auf deinen Zug..."
        elif draw_pile_checked:
            if selected_card['position'] and selected_card['action'] == 'flip':
                pos = selected_card['position']
                return f"Karte {pos[0]}, {pos[1]} umdrehen"
            elif selected_card['position'] and selected_card['action'] == 'swap_and_flip':
                pos = selected_card['position']
                return f"Karte {pos[0]}, {pos[1]} tauschen oder umdrehen"
            elif selected_card['position'] and selected_card['action'] == 'swap':
                pos = selected_card['position']
                return f"Karte {pos[0]}, {pos[1]} tauschen"
            else:
                return "Wähle eine Karte"
        elif selected_card['position'] and (selected_card['action'] == 'swap' or selected_card['action'] == 'swap_and_flip'):
            pos = selected_card['position']
            return f"Position ({pos[0]}, {pos[1]}) ausgewählt → Klicke auf Ablagestapel zum Tauschen"
        elif selected_card['position'] and selected_card['action'] == 'flip':
            pos = selected_card['position']
            return f"Karte {pos[0]}, {pos[1]} drehen oder Ablagestapel aufdecken"
        else:
            return "Wähle eine Karte oder decke den Nachziehstapel auf"
    
    def process_card_action(self, action_type, position, action=None):
        """Verarbeitet eine Kartenaktion"""
        if action_type == "select_card":
            self.set_selection(position, action)
            return None
        elif action_type == "flip_card":
            self.current_action = ("Flip Card", position)
            self.clear_selection()
            self.draw_pile_checked = False
            return self.current_action
        elif action_type == "draw_pile_click":
            self.current_action = ("Draw Card", None)
            self.draw_pile_checked = True
            return self.current_action
        elif action_type == "draw_pile_swap":
            if self.selected_card['action'] == 'swap_and_flip':
                # Swap with draw pile and flip the card
                self.current_action = ("Take from Draw Pile", position)
            else:
                # Regular swap with draw pile
                self.current_action = ("Take from Draw Pile", position)
            self.clear_selection()
            self.draw_pile_checked = False  # Reset draw pile state after swap
            return self.current_action
        elif action_type == "discard_pile_swap":
            self.current_action = ("Swap with Discard", position)
            self.clear_selection()
            return self.current_action
        elif action_type == "clear_selection":
            self.clear_selection()
            return None
        
        return None
    
    def reset_turn_state(self):
        """Setzt den Zustand für einen neuen Zug zurück"""
        self.clear_selection()
        self.draw_pile_checked = False
        self.current_action = None
    
    def reset_after_action(self):
        """Setzt den Zustand nach einer gesendeten Aktion zurück"""
        self.clear_selection()
        self.current_action = None
    
    def reset_draw_pile_state(self):
        """Setzt nur den Draw-Pile-Zustand zurück"""
        self.draw_pile_checked = False
    
    def set_draw_pile_checked(self, checked):
        """Setzt den Status, ob der Draw-Pile aufgedeckt ist"""
        self.draw_pile_checked = checked
