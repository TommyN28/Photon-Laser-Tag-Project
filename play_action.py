from tkinter import *
from datetime import datetime, timedelta
from player_udp import PlayerUDP
import sys

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
        self.player_frames = {}  # Dictionary to store player frames
        # Initialize game duration and countdown variables
        self.game_duration = timedelta(minutes=6)
        self.countdown_duration = timedelta(seconds=3)
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
            player_name_label = Label(player_frame, fg="green yellow", bg="black", text=" - " + player_info['name'].upper(), font=("Helvetica", 12, "bold"))
            player_name_label.pack(side=LEFT)
            player_score_label = Label(player_frame, fg="green yellow", bg="black", text="0", font=("Helvetica", 12, "bold"))
            player_score_label.pack(side=RIGHT)
            self.label_names[player_info['name']] = player_score_label  # Store the label widget
            self.player_frames[player_info['name']] = player_frame  # Store the player frame

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
            player_name_label = Label(player_frame, fg="red2", bg="black", text=" - " + player_info['name'].upper(), font=("Helvetica", 12, "bold"))
            player_name_label.pack(side=LEFT)
            player_score_label = Label(player_frame, fg="red2", bg="black", text="0", font=("Helvetica", 12, "bold"))
            player_score_label.pack(side=RIGHT)
            self.label_names[player_info['name']] = player_score_label
            self.player_frames[player_info['name']] = player_frame

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
        else:
            self.timer_label.config(text="Time remaining: " + str(remaining_time)[2:7])  # Format as mm:ss
            self.timer_label.after(1000, self.update_game_timer)

    def start_traffic_generator(self):
        # Start the traffic generator
        self.player_udp.start_traffic_generator(self.green_players, self.red_players, self.update_scrollable_screen)

    def update_scrollable_screen(self, received_data):
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

        print("Is Same Team:", is_same_team)

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

        # Update GUI to display updated scores and rearrange player rows
        for i, (player, score) in enumerate(sorted(self.player_scores.items(), key=lambda x: x[1], reverse=True)):
            # Update player score label
            if player in self.label_names:
                self.label_names[player].config(text=f"{score}")

            # Retrieve player frame and move it to new position
            if player in self.player_frames:
                player_frame = self.player_frames[player]
                player_frame.pack_forget()  # Remove from previous position
                player_frame.pack(side=TOP, anchor=W)  # Place in new position