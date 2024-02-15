import tkinter as tk

def submit_entry():
    for row_index in range(1, 16):
        green_name = f'Green_{row_index}'
        green_id = int(green_ids.get(green_name))
        red_name = f'Red_{row_index}'
        red_id = int(red_ids.get(red_name))

        # You can use the following lines to insert green_name and green_id into your database
        # ...

        # You can use the following lines to insert red_name and red_id into your database
        # ...

    # Close the window upon submission
    window.destroy()

window = tk.Tk()
window.title("Player Entry Screen")
window.configure(bg='grey')

# Add empty rows for spacing at the top
for i in range(2):
    tk.Label(window, text="", bg='grey').grid(row=i, column=0)

title = tk.Label(window, text="Get Ready!", bg='grey', fg='white', font=("Quantum", 32, "bold"))
# Center the title on the screen
title.grid(row=0, column=0, columnspan=4)

# Frame to hold the title and tables
frame = tk.Frame(window, bg='grey')
frame.grid(row=1, column=0, columnspan=4)

greenTitle = tk.Label(frame, text="Green Team", bg='olivedrab', fg='white', font=("Quantum", 24, "bold"))
greenTitle.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

redTitle = tk.Label(frame, text="Red Team", bg='maroon', fg='white', font=("Quantum", 24, "bold"))
redTitle.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Creation the green table
green_table = tk.Frame(frame, bg='olivedrab')
green_table.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

# Creation of the red table
red_table = tk.Frame(frame, bg='maroon')
red_table.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

green_names = {}
green_ids = {}
red_names = {}
red_ids = {}

for row_index in range(1, 16):
    tk.Label(green_table, text=f'Player {row_index}', bg='olivedrab').grid(row=row_index, column=0, padx=5, pady=5, sticky='nw')
    green_name = f'Green_{row_index}'
    green_names[green_name] = tk.StringVar()
    tk.Entry(green_table, textvariable=green_names[green_name]).grid(row=row_index, column=1, padx=5, pady=5, sticky='nw')

    tk.Label(green_table, text='ID:', bg='olivedrab').grid(row=row_index, column=2, padx=5, pady=5, sticky='nw')
    green_id = f'ID_Green_{row_index}'
    green_ids[green_id] = tk.StringVar()
    tk.Entry(green_table, textvariable=green_ids[green_id]).grid(row=row_index, column=3, padx=5, pady=5, sticky='nw')

    tk.Label(red_table, text=f'Player {row_index}', bg='maroon').grid(row=row_index, column=0, padx=5, pady=5, sticky='nw')
    red_name = f'Red_{row_index}'
    red_names[red_name] = tk.StringVar()
    tk.Entry(red_table, textvariable=red_names[red_name]).grid(row=row_index, column=1, padx=5, pady=5, sticky='nw')

    tk.Label(red_table, text='ID:', bg='maroon').grid(row=row_index, column=2, padx=5, pady=5, sticky='nw')
    red_id = f'ID_Red_{row_index}'
    red_ids[red_id] = tk.StringVar()
    tk.Entry(red_table, textvariable=red_ids[red_id]).grid(row=row_index, column=3, padx=5, pady=5, sticky='nw')

continue_button = tk.Button(window, text="Continue", command=submit_entry)
continue_button.grid(row=2, columnspan=4)

window.mainloop()
