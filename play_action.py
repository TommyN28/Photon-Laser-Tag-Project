from tkinter import *
from datetime import datetime, timedelta
from player_udp import PlayerUDP
import sys
from tkinter import messagebox

GREEN_BASE_SCORED_CODE: int = 43
RED_BASE_SCORED_CODE: int = 53

class playAction:
    def __init__(self, green_players, red_players):
        # Set up blank screen (using width/height variables for easy access)
        self.root = Tk()
        self.root.title("Play Action")
        screen_width = 1200
        screen_height = 900
        self.root.geometry(str(screen_width) + "x" + str(screen_height))
        self.player_udp = PlayerUDP()
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.player_scores = {player_info['name']: 0 for player_info in green_players.values()}
        self.player_scores.update({player_info['name']: 0 for player_info in red_players.values()})
        self.label_names = {}
        self.base_hit_labels = {}
        self.player_frames = {}  # Dictionary to store player frames
        # Initialize game duration and countdown variables
        self.game_duration = timedelta(minutes=6)
        self.countdown_duration = timedelta(seconds=30)
        self.start_time = None
        self.end_time = None

        self.green_players = green_players or {}
        self.red_players = red_players or {}

        # Set up blank timer label
        self.timer_label = Label(self.root, text="", font=("Helvetica", 16, "bold"))
        self.timer_label.pack()

        # Set up green player list
        self.green_frame = Frame(self.root, bg="black", bd=1)
        self.green_frame.pack(fill=BOTH, expand=True)
        Label(self.green_frame, fg="green yellow", bg="black", text="ALPHA GREEN", font=("Helvetica", 16, "bold")).pack(pady=5)
        self.green_total_score_label = Label(self.green_frame, fg="green yellow", bg="black", text="Total Score: 0", font=("Helvetica", 12, "bold"))
        self.green_total_score_label.pack(pady=5)

        # Display green team names
        for player_info in green_players.values():
            player_frame = Frame(self.green_frame, bg="black")
            player_frame.pack(fill=X)
            # Create a label for base_hit (initially hidden)
            base_hit_label = Label(player_frame, fg="black", bg="black", text="", font=("Helvetica", 12, "bold"))
            base_hit_label.pack(side=LEFT)  # Base hit label also packed to the left
            base_hit_label.config(state=DISABLED)  # Initially hide the base hit label

            player_name_label = Label(player_frame, fg="green yellow", bg="black", text=" - " + player_info['name'].upper(), font=("Helvetica", 12, "bold"))
            player_name_label.pack(side=LEFT)
            player_score_label = Label(player_frame, fg="green yellow", bg="black", text="0", font=("Helvetica", 12, "bold"))
            player_score_label.pack(side=RIGHT)
            self.label_names[player_info['name']] = player_score_label  # Store the label widget

            self.player_frames[player_info['name']] = player_frame  # Store the player frame
            self.base_hit_labels[player_info['name']] = base_hit_label

        # Set up red team player list
        self.red_frame = Frame(self.root, bg="black", bd=1)
        self.red_frame.pack(fill=BOTH, expand=True)
        Label(self.red_frame, fg="red2", bg="black", text="ALPHA RED", font=("Helvetica", 16, "bold")).pack(pady=5)
        self.red_total_score_label = Label(self.red_frame, fg="red2", bg="black", text="Total Score: 0", font=("Helvetica", 12, "bold"))
        self.red_total_score_label.pack(pady=5)

        # Display red team names
        for player_info in red_players.values():
            player_frame = Frame(self.red_frame, bg="black")
            player_frame.pack(fill=X)
            # Create a label for base_hit (initially hidden)
            base_hit_label = Label(player_frame, fg="black", bg="black", text="", font=("Helvetica", 12, "bold"))
            base_hit_label.pack(side=LEFT)  # Base hit label also packed to the left
            base_hit_label.config(state=DISABLED)  # Initially hide the base hit label

            player_name_label = Label(player_frame, fg="red2", bg="black", text=" - " + player_info['name'].upper(), font=("Helvetica", 12, "bold"))
            player_name_label.pack(side=LEFT)
            player_score_label = Label(player_frame, fg="red2", bg="black", text="0", font=("Helvetica", 12, "bold"))
            player_score_label.pack(side=RIGHT)
            self.label_names[player_info['name']] = player_score_label
            self.player_frames[player_info['name']] = player_frame

            self.base_hit_labels[player_info['name']] = base_hit_label

            # Set up middle screen
        self.middle_screen = Frame(self.root, bg="gray25", bd=1)
        self.middle_screen.pack(fill=BOTH, expand=True)

        # Scrollable text area for play-by-play action
        self.play_by_play_text = Text(self.middle_screen, fg="white", bg="gray25", font=("Helvetica", 12), wrap=WORD)
        self.play_by_play_text.pack(fill=BOTH, expand=True)

        # Place frames in their respective corners
        self.root.geometry("+0+0")
        self.green_frame.place(x=0, y=0, width=screen_width/2, height=screen_height/2)  # Top-left corner
        self.red_frame.place(x=screen_width - screen_width/2, y=0, width=screen_width/2, height=screen_height/2)  # Top-right corner
        self.middle_screen.place(x=0, y=screen_height/2, width=screen_width, height=screen_height/2)  # Middle

        # Set up timer label
        self.timer_label = Label(self.middle_screen, fg="white", bg="gray25", text="", font=("Helvetica", 16, "bold"))
        self.timer_label.pack(side=BOTTOM)

        # Start updating the timer
        self.start_countdown()

        self.root.mainloop()

    def start_countdown(self):
        # Start the 30-second countdown
        self.countdown_end_time = datetime.now() + self.countdown_duration
        self.update_countdown()

    def on_window_close(self):
        # Send the end code message to terminate the process
        self.player_udp.send_end_code()
        # Determine and display the winner
        self.display_winner()
        sys.exit()

    def update_countdown(self):
        # Update the countdown timer label
        remaining_time = self.countdown_end_time - datetime.now()
        if remaining_time <= timedelta(seconds=0):
            # Start the game timer after the countdown finishes
            self.start_game_timer()
            # Start the traffic generator
            self.start_traffic_generator()
        else:
            self.timer_label.config(text="Game starts in: " + str(remaining_time)[2:7])  # Format as mm:ss
            self.timer_label.after(1000, self.update_countdown)

    def start_game_timer(self):
        # Start the game timer for 6 minutes
        self.game_end_time = datetime.now() + self.game_duration
        self.update_game_timer()

    def update_game_timer(self):
        # Update the game timer label
        remaining_time = self.game_end_time - datetime.now()
        if remaining_time <= timedelta(seconds=0):
            # Game over
            self.timer_label.config(text="Game Over")
            # Send end code when the game is over
            self.player_udp.send_end_code()
            self.display_winner()
            self.create_return_button()

        else:
            self.timer_label.config(text="Time remaining: " + str(remaining_time)[2:7])  # Format as mm:ss
            self.timer_label.after(1000, self.update_game_timer)

    def start_traffic_generator(self):
        # Start the traffic generator
        self.player_udp.start_traffic_generator(self.green_players, self.red_players, self.update_scrollable_screen)

    def update_scrollable_screen(self, received_data):
        if received_data.startswith("Base scored code:"):
            # Parse the received data to extract base code and player information
            base_code = int(received_data.split()[3])
            player_info = received_data.split(" and player ")[1].strip()

            # Extract equipment ID from player information
            equipment_id = player_info.split(": ")[1]  # Assuming the equipment ID follows "E ID: " in the message

             # Check if the base code matches the green base scored code
            if base_code == GREEN_BASE_SCORED_CODE:
                # Search for the player with the matching equipment ID in the green_players dictionary
                player_name = None
                for player_info in self.green_players.values():
                    if player_info['equipment_id']['equipment_id'] == equipment_id:
                        player_name = player_info['name']
                        break
                if player_name is not None:
                    # Player found, update their score and display message
                    player_info['equipment_id']['score'] += 100
                    player_info['equipment_id']['base_hit'] = True  # Set base_hit attribute to True
                    self.player_scores[player_info['name']] = player_info['equipment_id']['score']
                    self.play_by_play_text.insert(END, f"{player_name} has scored the red base\n")

                else:
                    print("Player not found with equipment ID:", equipment_id)
            elif base_code == RED_BASE_SCORED_CODE:
                # Search for the player with the matching equipment ID in the red_players dictionary
                player_name = None
                for player_info in self.red_players.values():
                    if player_info['equipment_id']['equipment_id'] == equipment_id:
                        player_name = player_info['name']
                        break
                if player_name is not None:
                    # Player found, update their score and display message
                    player_info['equipment_id']['score'] += 100
                    player_info['equipment_id']['base_hit'] = True  # Set base_hit attribute to True
                    self.player_scores[player_info['name']] = player_info['equipment_id']['score']
                    self.play_by_play_text.insert(END, f"{player_name} has scored the green base\n")

                else:
                    print("Player not found with equipment ID:", equipment_id)

        else:
            # Extract equipment IDs from the received data
            interaction = received_data.split(" Tag ")
            tagging_equipment_id = interaction[0].split("E ID: ")[1].split(" ")[0]
            tagged_equipment_id = interaction[1].split("E ID: ")[1].split(" ")[0]

            # Find player names using equipment IDs
            tagging_player_name = None
            tagged_player_name = None

            for player_info in self.green_players.values():
                if player_info['equipment_id']['equipment_id'] == tagging_equipment_id:
                    tagging_player_name = player_info['name']
                elif player_info['equipment_id']['equipment_id'] == tagged_equipment_id:
                    tagged_player_name = player_info['name']

            for player_info in self.red_players.values():
                if player_info['equipment_id']['equipment_id'] == tagging_equipment_id:
                    tagging_player_name = player_info['name']
                elif player_info['equipment_id']['equipment_id'] == tagged_equipment_id:
                    tagged_player_name = player_info['name']

            if tagging_player_name is None or tagged_player_name is None:
                print("Error: Unable to find player names for the given equipment IDs.")
                return

            # Update the play-by-play text with player names
            self.play_by_play_text.insert(END, f"{tagging_player_name} Tag {tagged_player_name}\n")

            # Check if players are from the same team
            is_same_team = (tagging_player_name in self.green_players and tagged_player_name in self.green_players) \
                           or (tagging_player_name in self.red_players and tagged_player_name in self.red_players)

            # Update scores for tagging player on the green team
            for player_info in self.green_players.values():
                if player_info['name'] == tagging_player_name:
                    if is_same_team:
                        player_info['equipment_id']['score'] -= 10
                    else:
                        player_info['equipment_id']['score'] += 10
                    # Update player score in self.player_scores
                    self.player_scores[player_info['name']] = player_info['equipment_id']['score']

            # Update scores for tagging player on the red team
            for player_info in self.red_players.values():
                if player_info['name'] == tagging_player_name:
                    if is_same_team:
                        player_info['equipment_id']['score'] -= 10
                    else:
                        player_info['equipment_id']['score'] += 10
                    # Update player score in self.player_scores
                    self.player_scores[player_info['name']] = player_info['equipment_id']['score']

            # Recalculate total scores for both green and red teams
            green_total_score = sum(player_info['equipment_id']['score'] for player_info in self.green_players.values())
            red_total_score = sum(player_info['equipment_id']['score'] for player_info in self.red_players.values())

            # Update the text of the total score labels for both teams
            self.green_total_score_label.config(text=f"Total Score: {green_total_score}")
            self.red_total_score_label.config(text=f"Total Score: {red_total_score}")

            # Compare total scores to determine which team's label should flash
            if green_total_score > red_total_score:
                self.flash_label(self.green_total_score_label)
                self.stop_flash_label(self.red_total_score_label)
            elif green_total_score < red_total_score:
                self.flash_label(self.red_total_score_label)
                self.stop_flash_label(self.green_total_score_label)
            else:
                # If scores are equal, stop flashing both labels
                self.stop_flash_label(self.green_total_score_label)
                self.stop_flash_label(self.red_total_score_label)

            # Update GUI to display updated scores and rearrange player rows
            players_with_b = set()  # Maintain a set of players who have "B" appended
            for i, (player, score) in enumerate(sorted(self.player_scores.items(), key=lambda x: x[1], reverse=True)):
                # Update player score label
                if player in self.label_names:
                    self.label_names[player].config(text=f"{score}")
                    # Check if the player has "B" appended and add them to the set
                    if self.label_names[player].cget("text").endswith(" B"):
                        players_with_b.add(player)

                # Update base hit label visibility
                base_hit = False
                for player_info in self.green_players.values():
                    if player_info['name'] == player and player_info['equipment_id']['base_hit']:
                        base_hit = True
                        break

                for player_info in self.red_players.values():
                    if player_info['name'] == player and player_info['equipment_id']['base_hit']:
                        base_hit = True
                        break

                # Update base hit label visibility
                base_hit_label = self.base_hit_labels[player]
                if base_hit:
                    base_hit_label.config(state=NORMAL)  # Show base hit label if base_hit is True
                    base_hit_label.config(fg="yellow", text="B")
                else:
                    base_hit_label.config(state=DISABLED)  # Hide base hit label if base_hit is False
            # Retrieve player frames and move them to new positions
            for player in self.player_frames:
                player_frame = self.player_frames[player]
                player_frame.pack_forget()  # Remove from previous position
                player_frame.pack(side=TOP, anchor=W)  # Place in new position


    def flash_label(self, label):
        # Toggle the label's background color between two colors
        if hasattr(self, "flash_timer"):
            # If a flash timer is already running, stop it first
            self.root.after_cancel(self.flash_timer)

        def toggle_color():
            if label.cget("bg") == "black":
                label.configure(bg="yellow")
            else:
                label.configure(bg="black")
            self.flash_timer = self.root.after(200, toggle_color)  # Flashing interval: 500 milliseconds

        toggle_color()

    def stop_flash_label(self, label):
        # Stop flashing the label and reset its background color
        if hasattr(self, "flash_timer"):
            self.root.after_cancel(self.flash_timer)
        label.configure(bg="black")  # Reset background color to black

    def display_winner(self):
        # Calculate total scores for green and red teams
        green_total_score = sum(player_info['equipment_id']['score'] for player_info in self.green_players.values())
        red_total_score = sum(player_info['equipment_id']['score'] for player_info in self.red_players.values())

        # Determine the winner based on total scores
        if green_total_score > red_total_score:
            winner = "Green Team"
        elif green_total_score < red_total_score:
            winner = "Red Team"
        else:
            winner = "It's a tie!"

        # Display the winner
        winner_label = Label(self.root, text=f"The winner is: {winner}", font=("Helvetica", 16, "bold"))
        winner_label.pack()

        # Place the winner label at the bottom of the screen
        winner_label.place(relx=0.5, rely=0.9, anchor=CENTER)

    def create_return_button(self):
        # Close the current window
        self.root.destroy()

        # Show a message box to indicate returning to player_entry.py
        messagebox.showinfo("Return", "Returning to Player Entry screen...")
