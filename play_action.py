from tkinter import *

class playAction:
    def __init__(self, green_players, red_players):
        # Set up blank screen (using width/height variables for easy access)
        self.root = Tk()
        self.root.title("Play Action")
        screen_width = 720
        screen_height = 540
        self.root.geometry(str(screen_width) + "x" + str(screen_height))

        # Set up green player list
        self.green_frame = Frame(self.root, bd=2, relief="groove")
        self.green_frame.pack(fill=BOTH, expand=True)
        Label(self.green_frame, text="Green Team", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Display green team names
        for name in green_players:
            Label(self.green_frame, text=name).pack()

        # Set up red team player list
        self.red_frame = Frame(self.root, bd=2, relief="groove")
        self.red_frame.pack(fill=BOTH, expand=True)
        Label(self.red_frame, text="Red Team", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Display red team names
        for name in red_players:
            Label(self.red_frame, text=name).pack()

        # Set up green side player feed
        self.green_feed = Frame(self.root, bd=2, relief="groove")
        self.green_feed.pack(fill=BOTH, expand=True)
        Label(self.green_feed, text="Green Team Feed", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Set up red side player feed
        self.red_feed = Frame(self.root, bd=2, relief="groove")
        self.red_feed.pack(fill=BOTH, expand=True)
        Label(self.red_feed, text="Red Team Feed", font=("Helvetica", 16, "bold")).pack(pady=5)

        # Place frames in their respective corners
        self.root.geometry("+0+0")
        self.green_frame.place(x=0, y=0, width=screen_width/2, height=screen_height/2)  # Top-left corner
        self.red_frame.place(x=screen_width - screen_width/2, y=0, width=screen_width/2, height=screen_height/2)  # Top-right corner
        self.green_feed.place(x=0, y=screen_height - screen_height/2, width=screen_width/2, height=screen_height/2)  # Bottom-left corner
        self.red_feed.place(x=screen_width - screen_width/2, y=screen_height - screen_height/2, width=screen_width/2, height=screen_height/2)  # Bottom-right corner

        self.root.mainloop()

