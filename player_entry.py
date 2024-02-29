import tkinter as tk
from tkinter import messagebox
from player_udp import player_udp
import supabase
from playerAction import PlayerAction

class PlayerEntry:
    def __init__(self):
        self.window = tk.Tk()
        self.udp_manager = player_udp()
        self.window.title("Player Entry Screen")
        self.window.configure(bg='grey')

        self.green_equipment_id_counter = 0
        self.red_equipment_id_counter = 10

        # Add empty rows for spacing at the top
        for i in range(2):
            tk.Label(self.window, text="", bg='grey').grid(row=i, column=0)

        title = tk.Label(self.window, text="Get Ready!", bg='grey', fg='white', font=("Quantum", 32, "bold"))
        # Center the title on the screen
        title.grid(row=0, column=0, columnspan=4)

        # Frame to hold the title and tables
        frame = tk.Frame(self.window, bg='lightgrey')
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

        # Add default rows for each team
        self.add_default_rows(self.green_table, 'Green', 15)
        self.add_default_rows(self.red_table, 'Red', 15)

        # Create Buttons
        tk.Button(self.window, text="Add New Player", command=self.handle_add_new_player_popup, relief=tk.RIDGE, font=("Helvetica", 12, "bold"), bg="white", fg="navy", borderwidth=5, highlightthickness=0).grid(row=2, columnspan=4, padx=10, pady=5)
        tk.Button(self.window, text="Add Existing Player", command=self.handle_add_existing_player, relief=tk.RIDGE, font=("Helvetica", 12, "bold"), bg="white", fg="navy", borderwidth=5, highlightthickness=0).grid(row=3, columnspan=4, padx=10, pady=5)

        # Supabase connection
        self.supabase_url = 'https://xsqxdgtmmlfjubodeinc.supabase.co'
        self.supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhzcXhkZ3RtbWxmanVib2RlaW5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjI4MjYsImV4cCI6MjAyMjk5ODgyNn0.tDnhgypAgUx4XL1pN9KLvQqY4QjfxjRZYD0VDX845cI'
        self.client = supabase.create_client(self.supabase_url, self.supabase_key)

        # Bind F5 key to start the game
        self.window.bind("<F5>", self.start_game)
        self.window.bind("<F12>", self.clear_all_entries)
        self.window.mainloop()

    def start_game(self, event):
        self.window.destroy()

        game_window = PlayerAction()

    def clear_all_entries(self, event):
        # Clear all player entries
        self.clear_entries(self.green_table)
        self.clear_entries(self.red_table)

    def clear_entries(self, table):
        # Clear all widgets in the green team table
        for widget in self.green_table.winfo_children():
            widget.destroy()
        # Clear all widgets in the red team table
        for widget in self.red_table.winfo_children():
            widget.destroy()

        # Reset dictionaries
        self.green_names = {}
        self.green_ids = {}
        self.red_names = {}
        self.red_ids = {}

        # Reset equipment ID counters
        self.green_equipment_id_counter = 0
        self.red_equipment_id_counter = 10

        # Add default rows again
        self.add_default_rows(self.green_table, 'Green', 15)
        self.add_default_rows(self.red_table, 'Red', 15)


    def add_default_rows(self, table, team, num_rows):

        # Determine the background and font color based on the team
        bg_color = 'olivedrab' if team == 'Green' else 'maroon'
        fg_color = 'white' if team == 'Green' else 'white'  # Font color is white for both teams

        tk.Label(table, text="  ", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=5, pady=5, sticky='nw')

        # Label for "ID" in the first row, first column
        id_label = tk.Label(table, text="ID", bg=bg_color, fg=fg_color)
        id_label.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

        # Label for "Player" in the first row, second column
        player_label = tk.Label(table, text="Username", bg=bg_color, fg=fg_color)
        player_label.grid(row=0, column=2, padx=5, pady=5, sticky='nw')

        # Label for "Equipment ID" in the first row, fourth column
        equipment_label = tk.Label(table, text="Equipment ID", bg=bg_color, fg=fg_color)
        equipment_label.grid(row=0, column=3, padx=5, pady=5, sticky='nw')

        tk.Label(self.window, text="Press F5 to start the game", bg='grey', fg='white', font=("Helvetica", 14)).grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 5))
        tk.Label(self.window, text="Press F12 to clear the table", bg='grey', fg='white', font=("Helvetica", 14)).grid(row=5, column=0, columnspan=4, padx=10, pady=(0, 10))

        for i in range(num_rows):
            tk.Label(table, text=f'Player  {i+1}', bg='olivedrab' if team == 'Green' else 'maroon', fg='white').grid(row=i+1, column=0, padx=5, pady=5, sticky='nw')

            # Label for player ID
            id_label = tk.Label(table, bg='olivedrab' if team == 'Green' else 'maroon', fg='white')
            id_label.grid(row=i+1, column=1, padx=5, pady=5, sticky='w')

            # Label for player name
            name_label = tk.Label(table, bg='olivedrab' if team == 'Green' else 'maroon', fg='white')
            name_label.grid(row=i+1, column=2, padx=5, pady=5, sticky='w')

            # Label for equipment ID
            equipment_label = tk.Label(table, bg='olivedrab' if team == 'Green' else 'maroon', fg='white')
            equipment_label.grid(row=i+1, column=3, padx=5, pady=5, sticky='w')

    def add_green_player(self, name, player_id):
        row_index = len(self.green_names) + 1

        # Increment the green equipment ID counter
        self.green_equipment_id_counter += 20

        # Calculate the equipment ID
        equipment_id = self.green_equipment_id_counter

        # Label for player ID
        id_label = tk.Label(self.green_table, text=f"{player_id}", bg='olivedrab', fg='white')
        id_label.grid(row=row_index, column=1, padx=5, pady=5, sticky='w')

        # Label for player name
        name_label = tk.Label(self.green_table, text=f"{name}", bg='olivedrab', fg='white')
        name_label.grid(row=row_index, column=2, padx=5, pady=5, sticky='w')

        # Label for equipment ID
        equipment_label = tk.Label(self.green_table, text=f"{equipment_id}", bg='olivedrab', fg='white')
        equipment_label.grid(row=row_index, column=3, padx=5, pady=5, sticky='w')

        # Label for score
        score_label = tk.Label(self.green_table, text="", bg='olivedrab', fg='white')
        score_label.grid(row=row_index, column=4, padx=5, pady=5, sticky='w')

        # Update the dictionary with the player's information
        self.green_names[name] = player_id

        # Broadcast the equipment ID
        self.udp_manager.broadcast_equipment_id(equipment_id)


    def add_red_player(self, name, player_id):
        row_index = len(self.red_names) + 1

        # Increment the red equipment ID counter
        self.red_equipment_id_counter += 20

        # Calculate the equipment ID
        equipment_id = self.red_equipment_id_counter

        # Label for player ID
        id_label = tk.Label(self.red_table, text=f"{player_id}", bg='maroon', fg='white')
        id_label.grid(row=row_index, column=1, padx=5, pady=5, sticky='w')

        # Label for player name
        name_label = tk.Label(self.red_table, text=f"{name}", bg='maroon', fg='white')
        name_label.grid(row=row_index, column=2, padx=5, pady=5, sticky='w')

        # Label for equipment ID
        equipment_label = tk.Label(self.red_table, text=f"{equipment_id}", bg='maroon', fg='white')
        equipment_label.grid(row=row_index, column=3, padx=5, pady=5, sticky='w')

        # Label for score
        score_label = tk.Label(self.red_table, text="", bg='maroon', fg='white')
        score_label.grid(row=row_index, column=4, padx=5, pady=5, sticky='w')

        # Update the dictionary with the player's information
        self.red_names[name] = player_id

        # Broadcast the equipment ID
        self.udp_manager.broadcast_equipment_id(equipment_id)

    def handle_add_new_player_popup(self):
        # self.new_popup.destroy()  # Close the current popup
        self.new_player_popup = tk.Toplevel()
        self.new_player_popup.title("Add New Player")

        # Label and Entry for Player ID
        tk.Label(self.new_player_popup, text="Player ID:").grid(row=0, column=0, padx=10, pady=5)
        self.new_player_id = tk.Entry(self.new_player_popup)
        self.new_player_id.grid(row=0, column=1, padx=10, pady=5)

        # Label and Entry for Player Name
        tk.Label(self.new_player_popup, text="Player Name:").grid(row=1, column=0, padx=10, pady=5)
        self.new_player_name = tk.Entry(self.new_player_popup)
        self.new_player_name.grid(row=1, column=1, padx=10, pady=5)

        # Label and Dropdown for Selecting Team
        tk.Label(self.new_player_popup, text="Select Team:").grid(row=2, column=0, padx=10, pady=5)
        self.team_var = tk.StringVar(self.new_player_popup)
        self.team_var.set("Green")  # Default team selection
        teams = ["Green", "Red"]  # List of teams
        team_dropdown = tk.OptionMenu(self.new_player_popup, self.team_var, *teams)
        team_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Confirm Button
        tk.Button(self.new_player_popup, text="Confirm", command=self.check_and_add_new_player).grid(row=3, columnspan=2, padx=10, pady=10)

    def check_and_add_new_player(self):
        player_id = self.new_player_id.get()
        player_name = self.new_player_name.get()

        # Check if player ID already exists in the database
        response = self.client.from_('LaserTag').select('ID').eq('ID', player_id).execute()
        if response.data:
            messagebox.showerror("Error", "Player ID already exists in the database. Please try again.")
        else:
            # If player ID is unique, add the player
            self.add_new_player()
            self.new_player_popup.destroy()  # Close the new player popup

    def handle_add_existing_player(self):
        # self.new_popup.destroy()  # Close the current popup
        self.existing_popup = tk.Toplevel()
        self.existing_popup.title("Add Existing Player")

        tk.Label(self.existing_popup, text="Player ID:").grid(row=0, column=0, padx=10, pady=5)
        self.existing_player_id = tk.Entry(self.existing_popup)
        self.existing_player_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.existing_popup, text="Confirm", command=self.add_existing_player).grid(row=1, columnspan=2, padx=10, pady=10)

    def add_new_player(self):
        player_name = self.new_player_name.get()
        player_id = self.new_player_id.get()
        team = self.team_var.get()  # Get the selected team from the dropdown
        self.add_green_player(player_name, player_id) if team == "Green" else self.add_red_player(player_name, player_id)
        self.insert_to_supabase(player_name, player_id, team)
        self.new_player_popup.destroy()  # Close the new player popup


    def add_existing_player(self):
        player_id = self.existing_player_id.get()
        player_name, team = self.get_player_info_from_supabase(player_id)
        if team == 'Green':
            self.add_green_player(player_name, player_id)
        else:
            self.add_red_player(player_name, player_id)
        self.existing_popup.destroy()  # Close the existing player popup

    def insert_to_supabase(self, name, player_id, team):
        # Insert new player into the database
        data = self.client.table('LaserTag').insert([{
            'ID': int(player_id),
            'Name': name,
            'Team': team,  # You may need to specify the team here
            'Score': 0
        }]).execute()

        print('New player added successfully.')

        # Clear the entry fields after adding a new player
        self.new_player_id.delete(0, tk.END)
        self.new_player_id.insert(0, "")  # Clear the entry
        self.new_player_name.delete(0, tk.END)
        self.new_player_name.insert(0, "")  # Clear the entry

    def get_player_info_from_supabase(self, player_id):
        response = self.client.from_('LaserTag').select('Name, Team').eq('ID', player_id).execute()
        if response.data:
            player_info = response.data[0]
            return player_info['Name'], player_info['Team']
        else:
            messagebox.showerror("Error", "Player not found in database.")

