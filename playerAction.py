import tkinter as tk

class PlayerAction:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Player Action")
        self.root.geometry("400x300")

        # Add game elements, buttons, labels, etc.
        self.label = tk.Label(self.root, text="Game is running!", font=("Arial", 18))
        self.label.pack(pady=20)

        # Start the game loop
        self.root.mainloop()