# game name

Game description

## Getting Started

---

Make sure you have Python 3.8.0 or newer and Raylib Python CFFI 3.7 installed and running on your machine. You can install Raylib Python CFFI by opening a terminal and running the following command.

```
python3 -m pip install raylib
```

After you've installed the required libraries, open a terminal and browse to the project's root folder. Start the program by running the following command.```

python3 cycle

```
You can also run the program from an IDE like Visual Studio Code. Start your IDE and open the
project folder. Select the main module inside the hunter folder and click the "run" icon.

## Project Structure
---
The project files and folders are organized as follows:
```

root (project root folder)
+-- GAME NAME HERE (source code for game)
+-- game (specific game classes)
+-- **main**.py (entry point for program)
+-- README.md (general info)

```

## Required Technologies
---
* Python 3.8.0
* Raylib Python CFFI 3.7

## Authors
---
Kyle Coulon (kylejcoulon@gmail.com)
* TODO: Add your name and email here



```

DESIGN DOCUMENT:

# Peter

# Rachel

# Kyle

# Alex

- - - - - - - - SPACE SHIP

Starts out with number of shields (health points) - possibly get more

Space ship that draws more than one text

Spaceship drawing:
-front`A`
-mid`<=#=>`
-thrst`"`
(thrust animates between `"` and `'`)

Movement: moves left and right (arrow keys)
collision between ship and enemies

- - - - - - - - BULLETS

either `|` or `^`
possibly upgrade to multiple lasers at once

Fire key (space bar)
timer to control rapid fire
collision between laser and enemies

- - - - - - - - ENEMIES (Parent class)

Enemies are children of parent class

different enemies have movement patterns

Types:
Asteroids ( different sizes)
Snake enemy (moves back and forth coming down screen) Splits when shot?

- - - - - - - - ENEMY DIFFICULTY CONTROLLER

timer
minute 1 small asteroids
minute 2 big asteroids
minute 3 snakes

- - - - - - - - SCORE

array of top five scores
highscore board with name - enter in initials

- - - - - - - - COLLISION
                between:
                all enemies (use parent class) and ship
                all enemies and ship bullets

- - - - - - - - ADDITIONAL TASKS

- Screen not so wide
- Higher resolution? (smaller grid size and font)
