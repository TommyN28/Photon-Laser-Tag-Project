from tkinter import *
from datetime import datetime, timedelta

class playAction:
    def __init__(self, green_players, red_players):
        # Set up blank screen (using width/height variables for easy access)
        self.root = Tk()
        self.root.title("Play Action")
        screen_width = 1200
        screen_height = 900
        self.root.geometry(str(screen_width) + "x" + str(screen_height))

        # Initialize game duration and countdown variables
        self.game_duration = timedelta(minutes=6)
        self.countdown_duration = timedelta(seconds=30)
        self.start_time = datetime.now()
        self.end_time = self.start_time + self.game_duration
        self.warning_time = self.end_time - self.countdown_duration

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
        for name in green_players:
            player_frame = Frame(self.green_frame, bg="black")
            player_frame.pack(fill=X)
            Label(player_frame, fg="green yellow", bg="black", text=" - " + name.upper(), font=("Helvetica", 12, "bold")).pack(side=LEFT)
            Label(player_frame, fg="green yellow", bg="black", text=score, font=("Helvetica", 12, "bold")).pack(side=RIGHT)

        # Set up red team player list
        self.red_frame = Frame(self.root, bg="black", bd=1)
        self.red_frame.pack(fill=BOTH, expand=True)
        Label(self.red_frame, fg="red2", bg="black", text="ALPHA RED", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Display red team names
        for name in red_players:
            player_frame = Frame(self.red_frame, bg="black")
            player_frame.pack(fill=X)
            Label(player_frame, fg="red2", bg="black", text=" - " + name.upper(), font=("Helvetica", 12, "bold")).pack(side=LEFT)
            Label(player_frame, fg="red2", bg="black", text=score, font=("Helvetica", 12, "bold")).pack(side=RIGHT)

        # Set up middle screen
        self.middle_screen = Frame(self.root, bg="gray25", bd=1)
        self.middle_screen.pack(fill=BOTH, expand=True)
        Label(self.middle_screen, fg = "white", bg = "gray25", text="Action Log", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Set up timer label at the bottom row
        self.timer_label_bottom = Label(self.root, fg = "white", bg="gray25", text="", font=("Helvetica", 16, "bold"))
        self.timer_label_bottom.pack(side=BOTTOM)

        # Place frames in their respective corners
        self.root.geometry("+0+0")
        self.green_frame.place(x=0, y=0, width=screen_width/2, height=screen_height/2)  # Top-left corner
        self.red_frame.place(x=screen_width - screen_width/2, y=0, width=screen_width/2, height=screen_height/2)  # Top-right corner
        self.middle_screen.place(x=0, y=screen_height/2, width=screen_width, height=screen_height/2)  # Middle
        self.timer_label_bottom.place(x=0, y=screen_height - 50, width=screen_width)  # Bottom

        # Start updating the timer
        self.update_timer()

        self.root.mainloop()

    def update_timer(self):
        # Calculate remaining time
        remaining_time = self.end_time - datetime.now()

        if remaining_time <= timedelta(seconds=0):
            # Game over
            self.timer_label_bottom.config(text="Game Over")
        elif remaining_time <= self.countdown_duration:
            # 30-second warning
            self.timer_label_bottom.config(text="Game starts in: " + str(remaining_time)[2:7])  # Format as mm:ss
            self.timer_label_bottom.after(1000, self.update_timer)
        else:
            # Display normal countdown
            self.timer_label_bottom.config(text="Time remaining: " + str(remaining_time)[2:7])  # Format as mm:ss
            self.timer_label_bottom.after(1000, self.update_timer)

