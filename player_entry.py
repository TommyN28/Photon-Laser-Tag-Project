import tkinter as tk
from tkinter import messagebox
import supabase


class PlayerEntry:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Player Entry Screen")
        self.window.configure(bg='grey')
        width = 1000
        height = 700

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)

        # Adjust where it pops up
        self.window.geometry("%dx%d+%d+%d" %
                           (width, height, x_coordinate, y_coordinate))

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

        self.add_player_button = tk.Button(self.window, text="Add Player", command=self.handle_add_player)
        self.add_player_button.grid(row=2, columnspan=4, padx=10, pady=10)

        # Supabase connection
        self.supabase_url = 'https://xsqxdgtmmlfjubodeinc.supabase.co'
        self.supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhzcXhkZ3RtbWxmanVib2RlaW5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjI4MjYsImV4cCI6MjAyMjk5ODgyNn0.tDnhgypAgUx4XL1pN9KLvQqY4QjfxjRZYD0VDX845cI'
        self.client = supabase.create_client(self.supabase_url, self.supabase_key)

        self.window.mainloop()

    def add_green_player(self, name, player_id):
        tk.Label(self.green_table, text=name, bg='olivedrab').grid(row=len(self.green_names) + 1, column=0, padx=5, pady=5, sticky='nw')
        tk.Label(self.green_table, text=player_id, bg='olivedrab').grid(row=len(self.green_names) + 1, column=1, padx=5, pady=5, sticky='nw')
        self.green_names[name] = player_id

    def add_red_player(self, name, player_id):
        tk.Label(self.red_table, text=name, bg='maroon').grid(row=len(self.red_names) + 1, column=0, padx=5, pady=5, sticky='nw')
        tk.Label(self.red_table, text=player_id, bg='maroon').grid(row=len(self.red_names) + 1, column=1, padx=5, pady=5, sticky='nw')
        self.red_names[name] = player_id

    def handle_new_player(self):
        name = self.new_name_entry.get()
        player_id = self.new_id_entry.get()
        team = self.team_var.get()
        if team == 'Green':
            self.add_green_player(name, player_id)
            self.add_player_to_supabase(name, player_id, 'Green')
        else:
            self.add_red_player(name, player_id)
            self.add_player_to_supabase(name, player_id, 'Red')
        self.new_popup.destroy()

    def handle_existing_player(self):
        name = self.existing_name_entry.get()
        player_data = self.fetch_player_data_by_name(name)
        if player_data:
            player_id = player_data['ID']
            team = player_data['Team']
            if team == 'Green':
                self.add_green_player(name, player_id)
            else:
                self.add_red_player(name, player_id)
            self.new_popup.destroy()  # Close the pop-up window
        else:
            messagebox.showerror("Error", "Player not found in database.")

    def fetch_player_data_by_name(self, name):
        response = self.client.from_('LaserTag').select('ID, Name, Team').eq('Name', name).execute()
        if response.data:
            return response.data[0]
        else:
            return None

    def add_player_to_supabase(self, name, player_id, team):
        data = self.client.table('LaserTag').insert([{
            'ID': int(player_id),
            'Name': name,
            'Team': team,
            'Score': 0
        }]).execute()

    def handle_add_player(self):
        self.new_popup = tk.Toplevel()
        width = 300
        height = 240
        screen_width = self.new_popup.winfo_screenwidth()
        screen_height = self.new_popup.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)


        # Adjust where it pops up
        self.new_popup.geometry("%dx%d+%d+%d" %
                             (width, height, x_coordinate, y_coordinate))

        self.new_popup.title("Add Player")

        tk.Label(self.new_popup, text="Player Name:").grid(row=0, column=0, padx=10, pady=5)
        self.new_name_entry = tk.Entry(self.new_popup)
        self.new_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.new_popup, text="Player ID:").grid(row=1, column=0, padx=10, pady=5)
        self.new_id_entry = tk.Entry(self.new_popup)
        self.new_id_entry.grid(row=1, column=1, padx=10, pady=5)

        self.team_var = tk.StringVar()
        self.team_var.set("Green")  # Default selection is green
        tk.Label(self.new_popup, text="Select Team:").grid(row=2, column=0, padx=10, pady=5)
        tk.OptionMenu(self.new_popup, self.team_var, "Green", "Red").grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.new_popup, text="Add New Player", command=self.handle_new_player).grid(row=3, columnspan=2, padx=10, pady=5)

        tk.Label(self.new_popup, text="Existing Player Name:").grid(row=4, column=0, padx=10, pady=5)
        self.existing_name_entry = tk.Entry(self.new_popup)
        self.existing_name_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.new_popup, text="Add Existing Player", command=self.handle_existing_player).grid(row=5, columnspan=2, padx=10, pady=10)
