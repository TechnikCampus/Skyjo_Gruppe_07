"""
Widget Manager - Handles UI widget creation and management
"""

from pygame_widgets import button, textbox, slider
import pygame


class WidgetManager:
    def __init__(self, screen, colors, layout):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.COLORS = colors
        self.LAYOUT = layout
        
        # UI Components
        self.widgets = {
            'main_menu': {},
            'host_game': {},
            'game': {}
        }
        
        # Create all widgets
        self._create_all_widgets()
    
    def _create_all_widgets(self):
        """Erstellt alle UI Widgets"""
        self._create_main_menu_widgets()
        self._create_host_game_widgets()
        self._create_game_widgets()
    
    def _create_main_menu_widgets(self):
        """Erstellt Main Menu Widgets"""
        center_x = self.WIDTH // 2
        center_y = self.HEIGHT // 2
        start_y = 120
        spacing = 80
        
        self.widgets['main_menu'] = {
            'ip_textbox': textbox.TextBox(
                self.screen,
                x=center_x - self.LAYOUT['textbox_width'] // 2,
                y=start_y + spacing * 3,
                width=self.LAYOUT['textbox_width'],
                height=self.LAYOUT['textbox_height'],
                placeholderText='Server IP eingeben (z.B. 127.0.0.1)',
                fontSize=20,
                onSubmit=None  # Will be set by GUI
            ),
            'connect_button': button.Button(
                self.screen,
                text='Mit Server verbinden',
                fontSize=20,
                x=center_x - self.LAYOUT['button_width'] // 2,
                y=start_y + spacing * 6,
                width=self.LAYOUT['button_width'],
                height=self.LAYOUT['button_height'],
                onClick=None  # Will be set by GUI
            ),
            'exit_button': button.Button(
                self.screen,
                text='Beenden',
                fontSize=20,
                x=center_x - self.LAYOUT['button_width'] // 2,
                y=start_y + spacing * 7,
                width=self.LAYOUT['button_width'],
                height=self.LAYOUT['button_height'],
                onClick=None  # Will be set by GUI
            )
        }
    
    def _create_host_game_widgets(self):
        """Erstellt Host Game Widgets"""
        center_x = self.WIDTH // 2
        center_y = self.HEIGHT // 2
        start_y = 120
        spacing = 80
        
        self.widgets['host_game'] = {
            'name_textbox': textbox.TextBox(
                self.screen,
                x=center_x - self.LAYOUT['textbox_width'] // 2,
                y=start_y,
                width=self.LAYOUT['textbox_width'],
                height=self.LAYOUT['textbox_height'],
                placeholderText='Dein Name',
                fontSize=20
            ),
            'game_textbox': textbox.TextBox(
                self.screen,
                x=center_x - self.LAYOUT['textbox_width'] // 2,
                y=start_y + spacing,
                width=self.LAYOUT['textbox_width'],
                height=self.LAYOUT['textbox_height'],
                placeholderText='Spielname',
                fontSize=20
            ),
            'players_slider': slider.Slider(
                self.screen,
                x=center_x - self.LAYOUT['slider_width'] // 2,
                y=start_y + spacing * 4,
                width=self.LAYOUT['slider_width'],
                height=self.LAYOUT['slider_height'],
                min=0, max=2, step=1, initial=0
            ),
            'start_button': button.Button(
                self.screen,
                text='Spiel starten',
                fontSize=20,
                x=center_x - self.LAYOUT['button_width'] // 2,
                y=start_y + spacing * 6,
                width=self.LAYOUT['button_width'],
                height=self.LAYOUT['button_height'],
                onClick=None  # Will be set by GUI
            ),
            'back_button': button.Button(
                self.screen,
                text='Zurück',
                fontSize=20,
                x=center_x - self.LAYOUT['button_width'] // 2,
                y=start_y + spacing * 7,
                width=self.LAYOUT['button_width'],
                height=self.LAYOUT['button_height'],
                onClick=None  # Will be set by GUI
            )
        }
    
    def _create_game_widgets(self):
        """Erstellt Game Widgets"""
        # Currently no pygame-widgets needed for game view
        # Game interaction is handled through direct mouse events
        self.widgets['game'] = {}
    
    def show_widgets(self, *widget_groups):
        """Zeigt spezifische Widget-Gruppen an"""
        for group in widget_groups:
            if group in self.widgets:
                for widget in self.widgets[group].values():
                    widget.show()
    
    def hide_widgets(self, *widget_groups):
        """Versteckt spezifische Widget-Gruppen"""
        for group in widget_groups:
            if group in self.widgets:
                for widget in self.widgets[group].values():
                    widget.hide()
    
    def hide_all_widgets(self):
        """Versteckt alle Widgets"""
        for widget_group in self.widgets.values():
            for widget in widget_group.values():
                widget.hide()
    
    def set_widget_callback(self, group, widget_name, callback):
        """Setzt einen Callback für ein Widget"""
        if group in self.widgets and widget_name in self.widgets[group]:
            widget = self.widgets[group][widget_name]
            if hasattr(widget, 'onClick'):
                widget.onClick = callback
            elif hasattr(widget, 'onSubmit'):
                widget.onSubmit = callback
    
    def get_widget(self, group, widget_name):
        """Gibt ein spezifisches Widget zurück"""
        if group in self.widgets and widget_name in self.widgets[group]:
            return self.widgets[group][widget_name]
        return None
    
    def get_widget_text(self, group, widget_name):
        """Gibt den Text eines Widgets zurück"""
        widget = self.get_widget(group, widget_name)
        if widget and hasattr(widget, 'getText'):
            return widget.getText()
        return ""
    
    def get_widget_value(self, group, widget_name):
        """Gibt den Wert eines Widgets zurück (für Slider)"""
        widget = self.get_widget(group, widget_name)
        if widget and hasattr(widget, 'getValue'):
            return widget.getValue()
        return None
    
    def set_widget_text(self, group, widget_name, text):
        """Setzt den Text eines Widgets"""
        widget = self.get_widget(group, widget_name)
        if widget and hasattr(widget, 'setText'):
            widget.setText(text)
    
    def update_action_button_visibility(self, is_my_turn):
        """Aktualisiert die Sichtbarkeit von Action Buttons"""
        # Currently no action buttons as pygame-widgets
        # Action buttons are rendered directly in GameRenderer
        pass
