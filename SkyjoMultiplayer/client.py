##### Neuer verbesserter Client mit neuer GUI #####
import ctypes
# Set the DPI awareness to ensure proper scaling on high DPI displays
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import pygame
import pygame_widgets
import sys
import socket
import time
import threading
import queue

# Import Client modules
import Client as clnt
from Client.MenuState import Menu_State
from Client.GUI import SkyjoGUI

# Pygame initialization
pygame.init()
pygame.display.set_caption("Skyjo Multiplayer - Kartenspiel")
clock = pygame.time.Clock()
display = pygame.display.set_mode((1920, 1080))

# Global game state
game_state = {
    'menu_state': Menu_State.MAIN_MENU,
    'client_name': "",
    'client_game': "",
    'server_ip': "",
    'sock': None,
    'snapshot': None,
    'running': True
}

# Threading components
command_queue = queue.Queue()
send_list = []

# Initialize GUI
gui = SkyjoGUI(display)

def main_game_loop():
    """Main game loop - processes GUI commands"""
    global send_list
    
    print(f"main_game_loop called - current send_list: {send_list}")
    
    # Don't clear old commands immediately - let connection handler process them first
    # send_list.clear()
    
    # Get new commands from queue
    new_commands = []
    while not command_queue.empty():
        try:
            command = command_queue.get_nowait()
            if command is not None:
                new_commands.append(command)
                print(f"Command queued: {command}")
        except queue.Empty:
            break
    
    # Add new commands to send_list
    if new_commands:
        send_list.extend(new_commands)
        print(f"Added {len(new_commands)} commands to send_list. Total: {len(send_list)}")
    
    # Debug: Show current send_list state
    if send_list:
        print(f"Commands ready to send: {send_list}")
    # No automatic commands - let the player initiate actions

def connection_handler():
    """Handles server communication in background thread"""
    global game_state, send_list
    
    print("Connection handler started")
    
    while game_state['running']:
        # Only communicate when in game and connected
        if (game_state['menu_state'] != Menu_State.GAME or 
            game_state['sock'] is None or 
            not game_state['client_name'] or 
            not game_state['client_game']):
            time.sleep(0.01)  # Reduced sleep time for faster response
            continue
        
        print(f"Connection handler active - send_list has {len(send_list)} items")
        
        try:
            # Send commands if any
            if send_list:
                print(f"Sending to server: {send_list}")
                clnt.send_to_server(
                    game_state['sock'], 
                    send_list, 
                    game_state['client_name'], 
                    game_state['client_game']
                )
                
                # Receive server response
                try:
                    received = clnt.receive_from_server(game_state['sock'])
                except Exception as e:
                    print(f"Error receiving from server: {e}")
                    received = None
                
                if received and received != "Nichts gesendet vom Server":
                    print(f"Received valid data from server - Type: {type(received)}")
                    # Debug: Show what we actually received
                    if isinstance(received, dict):
                        print(f"  Active player: {received.get('Active')}")
                        print(f"  Players count: {len(received.get('Players', []))}")
                        print(f"  Running: {received.get('Running')}")
                    
                    # Update game snapshot
                    game_state['snapshot'] = {
                        "Active": received.get("Active"),
                        "Players": received.get("Players"),
                        "Discard Pile": received.get("Discard Pile"),
                        "Draw Pile": received.get("Draw Pile"),
                        "Game Round": received.get("Game Round"),
                        "Running": received.get("Running"),
                        "Final Phase": received.get("Final Phase")
                    }
                    
                    # Check for game end conditions
                    if ("Leave Game", True) in send_list:
                        print("Left the game!")
                        game_state['menu_state'] = Menu_State.MAIN_MENU
                        gui.reset_game_state()
                    
                    if not received.get("Running", True):
                        print("Game ended!")
                        game_state['menu_state'] = Menu_State.MAIN_MENU
                        gui.reset_game_state()
                elif received is None:
                    print("Server communication failed - connection may be lost")
                else:
                    print(f"Server says: {received}")
                
                # Clear sent commands
                print(f"Clearing {len(send_list)} sent commands")
                send_list.clear()
            
            else:
                # Listen for server updates - but don't spam console with timeouts
                try:
                    received = clnt.receive_from_server(game_state['sock'])
                    
                    if received and received != "Nichts gesendet vom Server":
                        print(f"Server update received - Type: {type(received)}")
                        if isinstance(received, dict):
                            print(f"  Update: Active={received.get('Active')}, Players={len(received.get('Players', []))}")
                        
                        game_state['snapshot'] = {
                            "Active": received.get("Active"),
                            "Players": received.get("Players"),
                            "Discard Pile": received.get("Discard Pile"),
                            "Draw Pile": received.get("Draw Pile"),
                            "Game Round": received.get("Game Round"),
                            "Running": received.get("Running"),
                            "Final Phase": received.get("Final Phase")
                        }
                        
                        if not received.get("Running", True):
                            print("Game ended by server!")
                            game_state['menu_state'] = Menu_State.MAIN_MENU
                            gui.reset_game_state()
                    elif received is None:
                        # Connection problem - don't spam console but track it
                        pass
                
                except socket.timeout:
                    # Timeout is normal when waiting for updates - don't spam console
                    pass
                except Exception as e:
                    print(f"Error during server update check: {e}")
                    time.sleep(0.5)
        
        except socket.timeout:
            # Timeout is normal, continue
            pass
        except ConnectionResetError:
            print("Connection to server lost!")
            game_state['menu_state'] = Menu_State.MAIN_MENU
            game_state['sock'] = None
            gui.reset_game_state()
            break
        except Exception as e:
            print(f"Unexpected communication error: {e}")
            time.sleep(1)  # Wait before retrying

def main():
    """Main application loop"""
    global game_state
    
    # Load card images
    if not gui.load_card_images():
        print("Failed to load card images. Exiting...")
        return
    
    # Start background communication thread
    comm_thread = threading.Thread(target=connection_handler, daemon=True)
    comm_thread.start()
    
    print("Skyjo Multiplayer Client started!")
    
    # Main game loop
    while game_state['running']:
        # Handle pygame events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_state['running'] = False
                break
            elif event.type == pygame.KEYDOWN:
                # Handle Enter key for different screens
                if event.key == pygame.K_RETURN:
                    if game_state['menu_state'] == Menu_State.MAIN_MENU:
                        # Simulate connect button click
                        gui._on_connect_clicked()
                    elif game_state['menu_state'] == Menu_State.HOST_GAME:
                        # Simulate start game button click
                        gui._on_start_game_clicked()
        
        # Check if GUI requested exit
        gui_state = gui.get_state()
        if gui_state['quitting']:
            game_state['running'] = False
            break
        
        # Update game state from GUI
        game_state.update({
            'menu_state': gui_state['menu_state'],
            'client_name': gui_state['client_name'],
            'client_game': gui_state['game_name'],
            'server_ip': gui_state['server_ip'],
            'sock': gui_state['sock']
        })
        
        # Clear screen
        display.fill(gui.COLORS['background'])
        
        # Render appropriate screen
        action = None
        
        if game_state['menu_state'] == Menu_State.MAIN_MENU:
            gui.render_main_menu()
            
        elif game_state['menu_state'] == Menu_State.HOST_GAME:
            gui.render_host_game_menu()
            
        elif game_state['menu_state'] == Menu_State.GAME:
            main_game_loop()  # Process commands
            action = gui.render_game(game_state['snapshot'], events)
            
            # Check for GUI actions
            gui_action = gui.get_action()
            if gui_action:
                print(f"GUI action received: {gui_action}")
                action = gui_action
            
            # Debug current state
            if game_state['snapshot'] is None:
                print("No snapshot available yet - waiting for server data")
            
            # Debug: Show if we received an action from the game render
            if action:
                print(f"Action from game render: {action}")
        
        # Queue any actions
        if action:
            print(f"Queueing action: {action}")
            command_queue.put(action)
        
        # Update pygame widgets
        pygame_widgets.update(events)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    # Cleanup
    if game_state['sock']:
        try:
            game_state['sock'].close()
        except:
            pass
    
    pygame.quit()
    print("Skyjo Client beendet. Auf Wiedersehen!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()
