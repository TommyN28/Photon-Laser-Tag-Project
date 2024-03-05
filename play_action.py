from tkinter import *

class playAction:
    def __init__(self, green_players, red_players):
        # Set up blank screen (using width/height variables for easy access)
        self.root = Tk()
        self.root.title("Play Action")
        screen_width = 1200
        screen_height = 900
        self.root.geometry(str(screen_width) + "x" + str(screen_height))

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

        # Set up green side player feed
        self.green_feed = Frame(self.root,  bg="gray40", bd=1)
        self.green_feed.pack(fill=BOTH, expand=True)
        Label(self.green_feed, bg="gray40", text="Green Feed Placeholder", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Set up red side player feed
        self.red_feed = Frame(self.root,  bg="gray40", bd=1)
        self.red_feed.pack(fill=BOTH, expand=True)
        Label(self.red_feed,  bg="gray40", text="Red Feed Placeholder", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Set up middle screen
        self.middle_screen = Frame(self.root, bg="gray25", bd=1)
        self.middle_screen.pack(fill=BOTH, expand=True)
        Label(self.middle_screen, bg="gray25", text="Fifth Frame Placeholder", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Place frames in their respective corners
        self.root.geometry("+0+0")
        self.green_frame.place(x=0, y=0, width=screen_width/2, height=screen_height/2)  # Top-left corner
        self.red_frame.place(x=screen_width - screen_width/2, y=0, width=screen_width/2, height=screen_height/2)  # Top-right corner
        self.green_feed.place(x=0, y=screen_height - screen_height/2, width=screen_width/3, height=screen_height/2)  # Bottom-left corner
        self.red_feed.place(x=screen_width - screen_width/3 - 1, y=screen_height - screen_height/2, width=screen_width/3 + 1, height=screen_height/2)  # Bottom-right corner (+/- 1 to counteract rounding)
        self.middle_screen.place(x=screen_width/3, y=screen_height - screen_height/2, width=screen_width/3, height=screen_height/2)

        self.root.mainloop()