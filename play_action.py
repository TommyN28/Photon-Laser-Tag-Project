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
        # Initialize game duration and countdown variables
        self.game_duration = timedelta(minutes=6)
        self.countdown_duration = timedelta(seconds=3)
        self.start_time = None
        self.end_time = None

        self.green_players = green_players or []
        self.red_players = red_players or []

        # Set up blank timer label
        self.timer_label = Label(self.root, text="", font=("Helvetica", 16, "bold"))
        self.timer_label.pack()

        # temp. var. for displaying score
        score = 0

        # Set up green player list
        self.green_frame = Frame(self.root, bg="black", bd=1)
        self.green_frame.pack(fill=BOTH, expand=True)
        Label(self.green_frame, fg="green yellow", bg="black", text="ALPHA GREEN", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Display green team names
        for player_info in green_players.values():
            player_frame = Frame(self.green_frame, bg="black")
            player_frame.pack(fill=X)
            player_name_label = Label(player_frame, fg="green yellow", bg="black", text=" - " + player_info['name'].upper(), font=("Helvetica", 12, "bold"))
            player_name_label.pack(side=LEFT)
            player_score_label = Label(player_frame, fg="green yellow", bg="black", text="0", font=("Helvetica", 12, "bold"))
            player_score_label.pack(side=RIGHT)
            self.label_names[player_info['name']] = player_score_label  # Store the label widget

        # Set up red team player list
        self.red_frame = Frame(self.root, bg="black", bd=1)
        self.red_frame.pack(fill=BOTH, expand=True)
        Label(self.red_frame, fg="red2", bg="black", text="ALPHA RED", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Display red team names
        for player_info in red_players.values():
            player_frame = Frame(self.red_frame, bg="black")
            player_frame.pack(fill=X)
            player_name_label = Label(player_frame, fg="red2", bg="black", text=" - " + player_info['name'].upper(), font=("Helvetica", 12, "bold"))
            player_name_label.pack(side=LEFT)
            player_score_label = Label(player_frame, fg="red2", bg="black", text="0", font=("Helvetica", 12, "bold"))
            player_score_label.pack(side=RIGHT)
            self.label_names[player_info['name']] = player_score_label

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
        # Update the scrollable screen with the received data and update scores
        self.play_by_play_text.insert(END, received_data + '\n')

        # Parse received data to determine player interactions
        # For example:
        # received_data format: "Player1 (E ID: 123) Tag Player2 (E ID: 456)"
        interaction = received_data.split(" Tag ")

        # Extract player names
        tagging_player = interaction[0].split(" (")[0]
        tagged_player = interaction[1].split(" (")[0]

        # Check if players are from the same team
        is_same_team = (tagging_player in self.green_players and tagged_player in self.green_players) \
                       or (tagging_player in self.red_players and tagged_player in self.red_players)

        # Update scores based on team affiliation
        if is_same_team:
            self.player_scores[tagging_player] -= 10
        else:
            self.player_scores[tagging_player] += 10

        # Update GUI to display updated scores
        for player, score in self.player_scores.items():
            self.label_names[player].config(text=f"{score}")



