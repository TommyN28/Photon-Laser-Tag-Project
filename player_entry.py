import tkinter as tk
from tkinter import messagebox
from player_udp import PlayerUDP
import supabase
from play_action import playAction
import time


class PlayerEntry:
    def __init__(self):
        self.window = tk.Tk()
        self.player_udp = PlayerUDP()
        self.window.title("Player Entry Screen")
        self.window.configure(bg='grey')

        # Calculate screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Set window size
        window_width = 570  # Adjust as needed
        window_height = 800  # Adjust as needed

        # Calculate x and y coordinates for the top-left corner of the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the geometry of the window
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # Add empty rows for spacing at the top
        for i in range(2):
            tk.Label(self.window, text="", bg='grey').grid(row=i, column=0)

        title = tk.Label(self.window, text="Get Ready!", bg='grey', fg='white', font=("Quantum", 32, "bold"))
        # Center the title on the screen
        title.grid(row=0, column=0, columnspan=4)

        # Frame to hold the title and tables
        frame = tk.Frame(self.window, bg='lightgrey')
        frame.grid(row=1, column=0, columnspan=4, sticky ='nsew')

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
        self.add_new_player_button = tk.Button(self.window, text="Add New Player", command=self.handle_add_new_player_popup, relief=tk.RIDGE, font=("Helvetica", 12, "bold"), bg="white", fg="navy", borderwidth=5, highlightthickness=0)
        self.add_new_player_button.grid(row=2, columnspan=4, padx=10, pady=5)

        # Set to keep track of used equipment IDs
        self.used_equipment_ids = set()

        self.add_existing_player_button = tk.Button(self.window, text="Add Existing Player", command=self.handle_add_existing_player, relief=tk.RIDGE, font=("Helvetica", 12, "bold"), bg="white", fg="navy", borderwidth=5, highlightthickness=0)
        self.add_existing_player_button.grid(row=3, columnspan=4, padx=10, pady=5)

        # Supabase connection
        self.supabase_url = 'https://xsqxdgtmmlfjubodeinc.supabase.co'
        self.supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhzcXhkZ3RtbWxmanVib2RlaW5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjI4MjYsImV4cCI6MjAyMjk5ODgyNn0.tDnhgypAgUx4XL1pN9KLvQqY4QjfxjRZYD0VDX845cI'
        self.client = supabase.create_client(self.supabase_url, self.supabase_key)

        # Bind F5 key to start the game
        self.window.bind("<F5>", self.start_game)
        self.window.bind("<F12>", self.clear_all_entries)
        self.window.mainloop()

    # Destroys the player entry screen after 30 seconds and creates the player action screen
    def start_game(self, event):
        # Check if both teams have at least one player
        if not self.green_names or not self.red_names:
            messagebox.showerror("Error", "Both teams must have at least one player.")
            return
        # Collect equipment IDs for green team
        green_equipment_ids = [equipment_id for equipment_id in self.green_ids.values()]
        # Collect equipment IDs for red team
        red_equipment_ids = [equipment_id for equipment_id in self.red_ids.values()]

        # Disable the buttons during the countdown
        self.add_new_player_button.config(state=tk.DISABLED)
        self.add_existing_player_button.config(state=tk.DISABLED)

        # Set the game status to indicate that the game is active
        self.game_active = True

        self.time_remaining = 1
        tk.Label(self.window, text="Time till game start: ", bg='grey', fg='yellow', font=("Helvetica", 14)).grid(row=2, column=3, columnspan=4, padx=10, pady=(0, 10))

        # Define a function to update the label every second
        def update_label():
            if self.time_remaining >= 0:
                label.config(text=self.time_remaining)
                self.time_remaining -= 1
                # Schedule the update again after 1 second
                self.window.after(1000, update_label)
            else:
                self.destroy_window()
                # Re-enable the buttons after the countdown
                self.add_new_player_button.config(state=tk.NORMAL)
                self.add_existing_player_button.config(state=tk.NORMAL)
                # Set the game status to indicate that the game is not active
                self.game_active = False

        label = tk.Label(self.window, text=self.time_remaining, bg='grey', fg='yellow', font=("Helvetica", 14))
        label.grid(row=3, column=3, columnspan=4, padx=10, pady=(0, 10))

        # Start updating the label
        update_label()

        # Disable the F12 function during the countdown
        self.window.unbind("<F12>")

    def destroy_window(self):
        self.window.destroy()
        game_window = playAction(self.green_names, self.red_names)

    def clear_all_entries(self, event):
        # Clear all player entries
        if not self.used_equipment_ids:
            messagebox.showinfo("Info", "No entries to clear.")
        else:
            self.clear_entries(self.green_table)
            self.clear_entries(self.red_table)
            self.used_equipment_ids.clear()

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

    def add_green_player(self, name, player_id, equipment_id):
        row_index = len(self.green_names) + 1

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
        self.player_udp.broadcast_equipment_id(equipment_id)


    def add_red_player(self, name, player_id, equipment_id):
        row_index = len(self.red_names) + 1

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
        self.player_udp.broadcast_equipment_id(equipment_id)


    def handle_add_new_player_popup(self):
        self.add_new_player_button.config(state=tk.DISABLED)
        self.new_player_popup = tk.Toplevel()
        self.new_player_popup.title("Add New Player")

        x_position = 425
        y_position = 200
        self.new_player_popup.geometry("+{}+{}".format(x_position, y_position))

        # Label and Entry for Player ID
        tk.Label(self.new_player_popup, text="Player ID:").grid(row=0, column=0, padx=10, pady=5)
        self.new_player_id = tk.Entry(self.new_player_popup, validate="key")
        self.new_player_id.grid(row=0, column=1, padx=10, pady=5)
        self.new_player_id.config(validatecommand=(self.new_player_id.register(self.validate_player_id_input), '%P'))

        # Label and Entry for Player Name
        tk.Label(self.new_player_popup, text="Player Name:").grid(row=1, column=0, padx=10, pady=5)
        self.new_player_name = tk.Entry(self.new_player_popup)
        self.new_player_name.grid(row=1, column=1, padx=10, pady=5)

        # Label and Entry for Equipment ID
        tk.Label(self.new_player_popup, text="Equipment ID:").grid(row=2, column=0, padx=10, pady=5)
        self.equipment_id_entry = tk.Entry(self.new_player_popup, validate="key")
        self.equipment_id_entry.grid(row=2, column=1, padx=10, pady=5)
        self.equipment_id_entry.config(validatecommand=(self.equipment_id_entry.register(self.validate_equipment_id_input), '%P'))

        # Label and Dropdown for Selecting Team
        tk.Label(self.new_player_popup, text="Select Team:").grid(row=3, column=0, padx=10, pady=5)
        self.team_var = tk.StringVar(self.new_player_popup)
        self.team_var.set("Green")  # Default team selection
        teams = ["Green", "Red"]  # List of teams
        team_dropdown = tk.OptionMenu(self.new_player_popup, self.team_var, *teams)
        team_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Confirm Button
        confirm_button = tk.Button(self.new_player_popup, text="Confirm", command=self.check_and_add_new_player)
        confirm_button.grid(row=4, columnspan=2, padx=10, pady=10)

        # Associate the enable_button method with the window close event
        self.new_player_popup.protocol("WM_DELETE_WINDOW", lambda: (self.enable_button(self.add_new_player_button), self.new_player_popup.destroy()))

    def enable_button(self, button):
        # Enable the button
        button.config(state=tk.NORMAL)

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
            self.new_player_popup.destroy()

    def handle_add_existing_player(self):
        # Disable the button to prevent multiple clicks
        self.add_existing_player_button.config(state=tk.DISABLED)
        # Create a new popup window for adding an existing player
        self.existing_popup = tk.Toplevel()
        self.existing_popup.title("Add Existing Player")

        x_position = 425
        y_position = 200
        self.existing_popup.geometry("+{}+{}".format(x_position, y_position))

        # Label and entry for Player ID
        tk.Label(self.existing_popup, text="Player ID:").grid(row=0, column=0, padx=10, pady=5)
        self.existing_player_id = tk.Entry(self.existing_popup, validate="key")
        self.existing_player_id.grid(row=0, column=1, padx=10, pady=5)
        self.existing_player_id.config(validatecommand=(self.existing_player_id.register(self.validate_player_id_input), '%P'))

        # Label and entry for Equipment ID
        tk.Label(self.existing_popup, text="Equipment ID:").grid(row=1, column=0, padx=10, pady=5)
        self.existing_equipment_id = tk.Entry(self.existing_popup, validate="key")
        self.existing_equipment_id.grid(row=1, column=1, padx=10, pady=5)
        self.existing_equipment_id.config(validatecommand=(self.existing_equipment_id.register(self.validate_equipment_id_input), '%P'))

        # Confirm button
        tk.Button(self.existing_popup, text="Confirm", command=self.add_existing_player).grid(row=2, columnspan=2, padx=10, pady=10)

        # Enable the button and destroy popup when closed
        self.existing_popup.protocol("WM_DELETE_WINDOW", lambda: (self.enable_button(self.add_existing_player_button), self.existing_popup.destroy()))

    def add_new_player(self):
        player_name = self.new_player_name.get()
        player_id = self.new_player_id.get()
        equipment_id = self.equipment_id_entry.get()
        team = self.team_var.get()

        # Check if the team has reached the maximum number of players
        if team == "Green" and len(self.green_names) >= 15:
            messagebox.showerror("Error", "Maximum number of players reached for the Green team.")
            return
        elif team == "Red" and len(self.red_names) >= 15:
            messagebox.showerror("Error", "Maximum number of players reached for the Red team.")
            return
        # Check if the equipment ID is already used
        if equipment_id in self.used_equipment_ids:
            messagebox.showerror("Error", "Equipment ID already in use. Please choose a different one.")
            self.enable_button(self.add_new_player_button)
            return

        # Add the player to the appropriate team
        if team == "Green":
            self.add_green_player(player_name, player_id, equipment_id)
        else:
            self.add_red_player(player_name, player_id, equipment_id)

        self.insert_to_supabase(player_name, player_id, team)
        self.new_player_popup.destroy()  # Close the new player popup
        self.enable_button(self.add_new_player_button)  # Re-enable the button
        self.used_equipment_ids.add(equipment_id)

    def add_existing_player(self):
        player_id = self.existing_player_id.get()
        equipment_id = self.existing_equipment_id.get()
        player_name, team = self.get_player_info_from_supabase(player_id)

        # Check if the team has reached the maximum number of players
        if team == "Green" and len(self.green_names) >= 15:
            messagebox.showerror("Error", "Maximum number of players reached for the Green team.")
            return
        elif team == "Red" and len(self.red_names) >= 15:
            messagebox.showerror("Error", "Maximum number of players reached for the Red team.")
            return

        # Check if the equipment ID is already used
        if equipment_id in self.used_equipment_ids:
            messagebox.showerror("Error", "Equipment ID already in use. Please choose a different one.")
            self.enable_button(self.add_new_player_button)
            return

        # Add the player to the appropriate team
        if team == 'Green':
            self.add_green_player(player_name, player_id, equipment_id)
        else:
            self.add_red_player(player_name, player_id, equipment_id)

        # Add the equipment ID to the set of used IDs
        self.used_equipment_ids.add(equipment_id)

        # Close the existing player popup
        self.existing_popup.destroy()
        self.enable_button(self.add_existing_player_button)


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

    def validate_player_id_input(self, input_text):
        if input_text.isdigit() or input_text == "":
            return True
        else:
            messagebox.showerror("Error", "Please enter a valid player ID (numeric characters only).")
            return False

    def validate_equipment_id_input(self, input_text):
        if input_text.isdigit() or input_text == "":
            return True
        else:
            messagebox.showerror("Error", "Please enter a valid equipment ID (numeric characters only).")
            return False