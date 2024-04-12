from tkinter import *
from PIL import Image, ImageTk

class Splash:

    def __init__(self) -> None:
        # Set up blank screen
        width = 1000
        height = 700
        self.root = Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)

        # Adjust where it pops up
        self.root.geometry("%dx%d+%d+%d" %
                           (width, height, x_coordinate, y_coordinate))

        # Remove the page heading
        self.root.overrideredirect(1)

        Frame(self.root, width=427, height=241, bg='black').place(x=50, y=100)

        # Add logo
        im = Image.open("logo.jpg")
        logo = im.resize((width, height))
        LOGO = ImageTk.PhotoImage(logo)

        # Insert logo
        logo_label = Label(image=LOGO, bg='black')
        logo_label.place(x=0, y=0)

        self.root.after(3000, lambda: self.root.destroy())
        mainloop()
