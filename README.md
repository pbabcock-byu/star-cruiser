# Star Cruiser 5000
Arcade style space shooter game with seven stages, three weapons, seven enemy types, and a highscore table.

Controls:
Left/Right arrow keys: move ship,
Spacebar: shoot laser,
Enter: Pause / select menu item,
A-Z keys: enter initials into highscore table,
Backspace/arrow keys: go back / move initials selection for highscore table input

## Getting Started

---

Make sure you have Python 3.8.0 or newer and Raylib Python CFFI 3.7 installed and running on your machine. You can install Raylib Python CFFI by opening a terminal and running the following command.

```
python3 -m pip install raylib
```

After you've installed the required libraries, open a terminal and browse to the project's root folder. Start the program by running the following command.

```
python3 starcruiser
```
or
```
python starcruiser
```

You can also run the program from an IDE like Visual Studio Code. Start your IDE and open the
project folder. Select the main module inside the hunter folder and click the "run" icon.

## Project Structure
---
The project files and folders are organized as follows:
```
root (project root folder)
+-- starcruiser (source code for game)
+-- game (specific game classes)
+-- **main**.py (entry point for program)
+-- README.md (general info)

```

## Required Technologies
---
* Python 3.8.0
* Raylib Python CFFI 3.7

## Author
---
Kyle Coulon (kylejcoulon@gmail.com) https://github.com/kylecooltron/star-cruiser
Peter Babcock https://github.com/pbabcock-byu/star-cruiser
Rachel Knight https://github.com/orangecat268

```
DESIGN DOCUMENT:

- - - - - - - - ACTOR
                similar to past actor classes, but will create a generate_structure(layout) method that takes an array of structure data and generates a group of actors at the given positions and with the given text values, colors, etc. That way the spaceship and asteroids can be made of more than one piece.

- - - - - - - - SPACE SHIP (actor)
                calls generate_structure to draw a ship

                Spaceship drawing:
                -front`A`
                -mid`<=#=>`
                -thrst`"`
                (thrust animates between `"` and `'`)

- - - - - - - - LASER (actor)
                either `|` or `^`
                green or red
                possibly upgrade to multiple lasers at once
                keeps track of a \_damage variable which will affect the health of the enemy it hits

- - - - - - - - KEYBOARD SERVICE
                Keys used: left/right arrows, space, enter, possibly letters for entering high score initials

- - - - - - - - HANDLE MOVEMENT
                Uses left and right (arrow keys) to apply velocity to the player's ship
                Spacebar creates a laser actor just in front of the ship
                Use timer and key_pressed variables to control rapid-fire and key hold

- - - - - - - - ENEMY DIFFICULTY CONTROLLER
                tracks how long the game has been running
                takes a list of "stages" dictionaries that contain information about a given stage
                as the game keeps running the controller uses information from the stage objects to randomly generate enemies
                looks up the enemy types associated with each stage
                looks up the spawn frequency associated with each stage
                wait timer runs over and over during a stage and generates enemies
                Example stage progression:
                First 10 seconds: small asteroids, creates one every 2 seconds
                next 10 seconds: medium asteroids, create one every 2 seconds
                next 20 seconds: mix os small/medium, create every 1 second
                next 10 seconds: create big asteroids
                etc.

- - - - - - - - ENEMIES (not neccesarily a class)
                different enemies have movement patterns
                override the actor's move_next() methods to customize movement

- - - - - - - - ASTEROID (actor)
                ( different sizes)
                keeps track of their own health value (larger asteroids take more shots)

- - - - - - - - SHIELDS:
                start out with a certain number of shields

- - - - - - - - SERPENT:
                (moves back and forth coming down screen)
                Splits when shot?

- - - - - - - - SCORE
                tracks score,
                score added every time enemy destroyed, possibly add time survived to overall score

- - - - - - - - HIGH SCORE TABLE
                An array of top five scores high score board with name
                use keyboard service to enter in initials
                save to .txt file
                loads from .txt file before displaying

- - - - - - - - HANDLE COLLISION
                between: all enemies and lasers
                between: ship and all enemies
                use actor groups to iterate through different enemy types
                loop through each enemies part list for multi-part structured enemies

- - - - - - - - SOUND EFFECTS

- - - - - - - - MENU SYSTEM
                Probably all we need is a game over screen and high score table and play again screen

- - - - - - - - ADDITIONAL TASKS
                High resolution? (smaller grid size and font, use widths for collision instead of position.equals?)
                Use images?

```
