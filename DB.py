import tkinter as tk
import supabase

class DataBase:
    def __init__(self):
        self.supabase_url = 'https://xsqxdgtmmlfjubodeinc.supabase.co'
        self.supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhzcXhkZ3RtbWxmanVib2RlaW5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjI4MjYsImV4cCI6MjAyMjk5ODgyNn0.tDnhgypAgUx4XL1pN9KLvQqY4QjfxjRZYD0VDX845cI'
        self.client = supabase.create_client(self.supabase_url, self.supabase_key)

    def add_player(self, name, player_id, team):
        # Insert new player into the "LaserTag" table
        data = self.client.table('LaserTag').insert([{
            'ID': player_id,
            'Name': name,
            'Team': team,
            'Score': 0
        }]).execute()

class PlayerEntry:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Player Entry Screen")
        self.window.configure(bg='grey')

        # Add empty rows for spacing at the top
        for i in range(2):
            tk.Label(self.window, text="", bg='grey').grid(row=i, column=0)

        title = tk.Label(self.window, text="Get Ready!", bg='grey', fg='white', font=("Quantum", 32, "bold"))
        # Center the title on the screen
        title.grid(row=0, column=0, columnspan=4)

        # Frame to hold the title and tables
        frame = tk.Frame(self.window, bg='grey')
        frame.grid(row=1, column=0, columnspan=4)

        greenTitle = tk.Label(frame, text="Green Team", bg='olivedrab', fg='white', font=("Quantum", 24, "bold"))
        greenTitle.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        redTitle = tk.Label(frame, text="Red Team", bg='maroon', fg='white', font=("Quantum", 24, "bold"))
        redTitle.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Creation the green table
        self.green_table = tk.Frame(frame, bg='olivedrab')
        self.green_table.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Creation of the red table
        self.red_table = tk.Frame(frame, bg='maroon')
        self.red_table.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.green_names = {}
        self.green_ids = {}
        self.red_names = {}
        self.red_ids = {}

        self.add_player_button = tk.Button(self.window, text="Add Player", command=self.new_player_popup)
        self.add_player_button.grid(row=2, columnspan=4, padx=10, pady=10)

        self.db = DataBase()

        self.window.mainloop()

    def add_green_player(self, name, player_id):
        tk.Label(self.green_table, text=name, bg='olivedrab').grid(row=len(self.green_names) + 1, column=0, padx=5, pady=5, sticky='nw')
        tk.Label(self.green_table, text=player_id, bg='olivedrab').grid(row=len(self.green_names) + 1, column=1, padx=5, pady=5, sticky='nw')
        self.green_names[name] = player_id

        # Add player to Supabase
        self.db.add_player(name, player_id, 'Green')

    def add_red_player(self, name, player_id):
        tk.Label(self.red_table, text=name, bg='maroon').grid(row=len(self.red_names) + 1, column=0, padx=5, pady=5, sticky='nw')
        tk.Label(self.red_table, text=player_id, bg='maroon').grid(row=len(self.red_names) + 1, column=1, padx=5, pady=5, sticky='nw')
        self.red_names[name] = player_id

        # Add player to Supabase
        self.db.add_player(name, player_id, 'Red')

    def handle_new_player(self):
        # Get the player name, ID, and selected team
        name = self.new_name_entry.get()
        player_id = self.new_id_entry.get()
        team = self.team_var.get()

        # Add the player to the respective team
        if team == 'Green':
            self.add_green_player(name, player_id)
        else:
            self.add_red_player(name, player_id)

        # Close the pop-up window
        self.new_popup.destroy()

    def new_player_popup(self):
        # Create a pop-up window to add a new player
        self.new_popup = tk.Toplevel()
        self.new_popup.title("Add New Player")

        # Label for player name
        name_label = tk.Label(self.new_popup, text="Player Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        # Entry field for player name
        self.new_name_entry = tk.Entry(self.new_popup)
        self.new_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label for player ID
        id_label = tk.Label(self.new_popup, text="Player ID:")
        id_label.grid(row=1, column=0, padx=10, pady=5)
        # Entry field for player ID
        self.new_id_entry = tk.Entry(self.new_popup)
        self.new_id_entry.grid(row=1, column=1, padx=10, pady=5)

        # Label for selecting team
        team_label = tk.Label(self.new_popup, text="Select Team:")
        team_label.grid(row=2, column=0, padx=10, pady=5)
        # Dropdown menu for selecting team
        self.team_var = tk.StringVar()
        self.team_var.set("Green")  # Default selection is green
        team_dropdown = tk.OptionMenu(self.new_popup, self.team_var, "Green", "Red")
        team_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Button to confirm adding new player
        confirm_button = tk.Button(self.new_popup, text="Confirm", command=self.handle_new_player)
        confirm_button.grid(row=3, columnspan=2, padx=10, pady=10)

