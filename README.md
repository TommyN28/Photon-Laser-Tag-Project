# CSCE-3513 Laser Tag Project
## Project Members:
Gabriel Miranda: gam010

Eduardo Tenorio: eduardot26

Tommy Ngo: TommyN28

Cole Goodwin: cag029
### Instructions to Run:

The user must first start by downloading the required Python packages needed for the program's functionality. 
The user will need to update the Ubuntu platform, 
--sudo apt-get update. 

Also, due to some extra libraries being used, the user will need to have pip3 installed on their device, 
--sudo apt install python3-pip

To be able to use the Tkinker library the user will need to install pillow,
--pip3 install pillow

Since a database library is also being used the user will need to install the library for Supabase,
--pip3 install supabase

The main file for this project is called main.py, and it needs to be run using python3. In case there are some errors due to missing imports with tkinker, additional commands need to be run to install the missing packages.

--sudo apt-get install python3-tk

--sudo apt-get install python3-pil python3-pil.imagetk

Then the user, using the command python3 main.py, should execute the code.

### Interacting with the Program:

The program simulates a 1980s-style laser tag game. Upon starting the program, the user is greeted by a short splash screen before the player entry screen is presented. On the player entry screen, the player will click a button to enter their ID and codename. 
That information will then be displayed on the list of players within the specified team, red or green. The information of the player is also stored in the game's database. This allows for a new game to be started and a player can retrieve their already existing player information to easily join the new game.

The currently present version of the game is only a small part of a larger implementation that will be added later. The primary game will allow a player to score by hitting players on the opposing team and its base.
