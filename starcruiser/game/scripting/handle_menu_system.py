import enum
import constants
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.actor import Actor
from game.casting.score import Score
from game.casting.shields import Shields
from game.casting.ship import Ship
from game.scripting.control_actors_action import ControlActorsAction
from game.scripting.move_actors_action import MoveActorsAction
from game.scripting.handle_collisions_action import HandleCollisionsAction
from game.scripting.handle_enemy_creation import HandleEnemyCreation


class handleMenuSystem(Action):
    """
    Controls the game start menu

    Attributes:
        _(name)_service (Service): An instance of a Service.

    """

    def __init__(self, keyboard_service, draw_actors_instance, video_service, audio_service):
        """Constructs a new handleMenuSystem using the specified KeyboardService.

        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService to control menu with keys
            video_service (VideoService): An instance of VideoService to close window if player selects "exit"
            audio_service (AudioService): An instance of AudioService to make menu sounds and control game music
            draw_actors_instance (Action): communicate when we start playing the game to draw ship, enemies, etc.

            control_actions_action     (store these actions so we can stop/start them when player starts the game)
            move_actors_action
            handle_collision_action
            handle_enemy_creation_action

            paused (bool): Tracks when the player pauses the game
            game_over (bool): Tracks when the game is over so we can control music and things
            end_score (int): stores the players score after game ends

            menu_state (string): "start", "highscore", "credits" or "none" if the game is in action
            menu_populated (bool): Is used to know when we need to repopulate the menu with it's correct text, colors, etc.
            menu_items (array of Actor): Stores the three display elements of the menu
            menu_item_highlighted (int): Tracks which menu item is selected/highlighted

            key_is_pressed (bool): Makes sure we only allows one key press at a time (on menu system)

            high_scores (list of strings): List of highscore strings loaded from a file (ex score string: ABC 100) 
            initials (list of strings): List of three letters the user will change by typing their initials
            initials_actors (list of Actor): Three display elements used to display the letters the player is entering
            initial_highlighted (int): keeps track of which of the three initials the player is editing

            menu values (list of strings) to display for a given menu
            menu heights (factor between zero and one) percentage of screen height as location to display the three menu elements
            
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._audio_service = audio_service
        self._draw_actors_instance = draw_actors_instance
        #class instances stored for game play
        self._control_actions_action = 0
        self._move_actors_action = 0
        self._handle_collision_action = 0
        self._handle_enemy_creation_action = 0
        # game control variables
        self._paused = False
        self._game_over = False
        self._end_score = 0
        # menu state variables
        self._menu_state = "start"  # start, highscore
        self._menu_populated = False
        self._menu_items = [Actor(), Actor(), Actor()]
        self._menu_item_highlighted = 0
        # menu control variables
        self._key_is_pressed = False
        # high score data
        self._high_scores = []
        self._initials = ["A", "A", "A"]
        self._initials_actors = []
        self._initial_highlighted = -1

        # MENU TEXT VALUES AND LAYOUTS - - -
        # start menu
        self._start_menu_values = [
            "ENTER TO START", "CREDITS / CONTROLS", "EXIT"]
        self._start_menu_heights = [0.4, 0.6, 0.8]
        # credits menu
        self._credits_menu_values = [
            "\t\t\t\t\t\t\t\tCONTROLS:\nmove = left/right arrow keys \n \t\t\t\t\t\tshoot = space \n \t\t\t\t\t\tpause = enter \n \t\t\t\tA-Z type highscore name", "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCREDITS:\n Kyle Coulon, Rachel Knight, Peter Babcock", "BACK"]
        self._credits_menu_heights = [0.4, 0.6, 0.8]
        # highscore menu
        self._highscore_menu_values = [
            "", "", "MAIN MENU"]
        self._highscore_menu_heights = [0.15, 0.3, 0.85]
        # - - - - - - - - - - - - - - - - -


    def set_game_over(self, game_over):
        self._game_over = game_over
        # tell the enemy creation action that we paused the game so it's timer stops
        self._handle_enemy_creation_action.set_paused(True)

    def set_menu_state(self, menu_state):
        self._menu_state = menu_state
        # reset menu populated so it runs it's update
        self._menu_populated = False

    def execute(self, cast, script):
        """Executes the handle menu system
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        # handle music
        self._handle_music()
        # handle menu populating
        self._handle_menu_populating(cast)
        # handle checking for keyboard input when displaying highscore table
        self._handle_highscore_input_checks(cast, script)
        # handle checking for keyboard input when dislpaying start or credits menu
        self._handle_start_and_credit_input_checks(cast, script)

    def _update_menu_items(self, cast, values, heights):
        """Updates the display elements of the manu with the given list of values and heights
        values (list of strings): text values of each of the three menu items
        heights (list of floats (zero to one range)): percentage of screen height to display each menu item
        """
        # for each of the three menu items
        for i in range(0, 3):
            # find it's new position
            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y * heights[i])
            position = Point(x, y)
            # get reference to the actor
            menu = self._menu_items[i]
            # set it's attributes
            menu.set_text(values[i])
            menu.set_position(position)
            # check which one is highlighted
            if i == self._menu_item_highlighted:
                # if it is this one, make it yellow
                menu.set_color(constants.YELLOW)
            # add menu items to menus group so they are displayed
            cast.add_actor("menus", menu)

    def _handle_music(self):
        """Make sure we're playing the correct music"""
        # if the game isn't over
        if not self._game_over:
            # play music depending on game/menu state
            if self._menu_state == "start"  or self._menu_state == "credits": 
                # play game music
                self._audio_service.set_music("menu-music")

            if self._menu_state == "none":
                # play menu music
                self._audio_service.set_music("game-music")

    def _handle_menu_populating(self, cast, script):
        """Handle population of menu when the state has been set but menu isn't populated yet
        """
        # if the menu has not yet been populated
        if self._menu_state != "none" and self._menu_populated == False:
            # set populated to true (so this only runs once)
            self._menu_populated = True
            
            # if the desired menu state is the "start" menu
            if self._menu_state == "start":
                # update menu to start menu text values / display heights
                self._update_menu_items(cast, self._start_menu_values, self._start_menu_heights)
                # find position for game title
                position = Point(int(constants.MAX_X / 2),
                                 int(constants.MAX_Y * 0.2))
                # create a game title display at that position
                title = Actor()
                title.set_text(constants.GAME_TITLE)
                title.set_position(position)
                title.set_font_size(30)
                title.set_color(constants.AQUA)
                # add it to menus cast list so it gets drawn
                cast.add_actor("menus", title)

            # if the desired menu state is the "highscore" menu
            if self._menu_state == "highscore":
                # pause the enemy creator
                self._handle_enemy_creation_action.set_paused(True)
                # get end score value and save it
                self._end_score = cast.get_first_actor("scores").get_points()

                # load the new highscore table and figure out if we are on it
                made_it = self._load_highscore_table()

                # if we made it to the highscore table
                if made_it >= 0:
                    # if we have the new top highscore
                    if made_it == 1:
                        # display this message at the top of the screen
                        self._highscore_menu_values[0] = "NEW HIGH SCORE!!!"
                    else:
                        # if we made it to the table, but it's not the highest score
                        # display this message
                        self._highscore_menu_values[0] = "You made it to the high score table!"

                    # give player instructions to enter initials
                    self._highscore_menu_values[1] = "Enter your initials (A-Z) then press ENTER"
                    # play sound made it to high score
                    self._audio_service.play_sound("new-highscore")
                    # highlight the first initial so player can start inputing
                    self._initial_highlighted = 0
                    # do not hightlight the main menu items yet (because they are entering initials now)
                    self._menu_item_highlighted = -1
                
                else:
                    # did not get a highscore
                    self._highscore_menu_values[0] = "You did not get a high score."
                    self._highscore_menu_values[1] = ""
                    # select the "DONE" menu item
                    self._menu_item_highlighted = 2

                # update menu display text to high score menu
                self._update_menu_items(cast, self._highscore_menu_values, self._highscore_menu_heights)
                self._update_menu_item_highlighted()
                # display the highscore table
                self._display_highscore_table(cast)
                # get position to display "HIGH SCORE TABLE" at the top of the scren
                position = Point(int(constants.MAX_X / 2),
                                 int(constants.MAX_Y * 0.1))
                # create a message actor at that position
                title = Actor()
                title.set_text("HIGH SCORE TABLE")
                title.set_position(position)
                title.set_font_size(20)
                title.set_color(constants.PINK)
                # add it to menus cast group so it gets drawn
                cast.add_actor("menus", title)
                # stop gameplay completely and prepare to potentially restart the game soon
                self._reset_game(cast, script)

    def _handle_highscore_input_checks(self, cast):
        """Handle checking for keyboard input when the highscore table is being displayed
        """
        if self._menu_state == "highscore":
            # if we are still selecting initials
            if self._initial_highlighted >= 0:

                if self._key_is_pressed == False:

                    # check for letter key presses (A-Z)
                    try_letter_key = self._keyboard_service.is_any_letter_key_down()
                    # if a letter key has been pressed
                    if try_letter_key != False:
                        self._key_is_pressed = True
                        # set the selected initials text value to that letter
                        self._initials[self._initial_highlighted] = try_letter_key.upper()
                        # set the actors text value to match
                        self._initials_actors[self._initial_highlighted].set_text(try_letter_key.upper())
                        # cursor forward to highlight the next initial
                        self._initial_highlighted += 1
                        # play initial enter sound
                        self._audio_service.play_sound("enter-initial")

                    elif self._keyboard_service.is_key_down('right'):
                        self._key_is_pressed = True
                        # cursor forward to highlight the next initial
                        self._initial_highlighted = (self._initial_highlighted + 1) % 3

                    elif self._keyboard_service.is_key_down('left'):
                        self._key_is_pressed = True
                        # cursor forward to highlight the previous initial
                        self._initial_highlighted = (self._initial_highlighted - 1) % 3

                    elif self._keyboard_service.is_key_down('back'):
                        self._key_is_pressed = True
                        # cursor forward to highlight the next initial
                        self._initial_highlighted -= 1
                        # clamp backspace to stop at first initial
                        if self._initial_highlighted < 0:
                            self._initial_highlighted = 0

                    if self._key_is_pressed == True:
                        # update which initials is highlighted if a key was pressed
                        self._update_initials_highlighted()

                    elif self._keyboard_service.is_key_down('enter'):
                        # player is done entering initials
                        self._key_is_pressed = True
                        # remove highlighted initial
                        self._initial_highlighted = -1
                        # apply colors
                        self._update_initials_highlighted()
                        # highlight the "DONE" menu item
                        self._menu_item_highlighted = 2
                        # apply colors
                        self._update_menu_item_highlighted()
                        # hide the highscore instructions text display after we are done
                        self._highscore_menu_values[0] = ""
                        self._highscore_menu_values[1] = ""
                        # apply text values/colors
                        self._update_menu_items(cast, self._highscore_menu_values, self._highscore_menu_heights)
                        # play menu select sound
                        self._audio_service.play_sound("menu-select")

                else:
                    if self._keyboard_service.is_any_letter_key_down() == False:
                        # reset key_is_pressed if none of the relevant keys are still down
                        if self._keyboard_service.is_key_up('enter') and self._keyboard_service.is_key_up('right') and self._keyboard_service.is_key_up('left'):
                            self._key_is_pressed = False
            else:
                # if we are done entering initials
                if self._key_is_pressed == False:
                    if self._keyboard_service.is_key_down('enter'):
                        self._key_is_pressed = True
                        # pressed enter to close highscore table
                        cast.remove_actors("highscores")
                        # save new highscore table
                        self._save_highscore_data()
                        # reset default highscore and initials variables
                        self._high_scores = []
                        self._initials = ["A", "A", "A"]
                        self._initials_actors = []
                        self._initial_highlighted = 0
                        # reset game over to start music again
                        self._game_over = False
                        # reset menu to get rid of all display elements
                        self._close_menu(cast)
                        # open start menu
                        self._menu_state = "start"
                        # highlight the "ENTER TO START" menu item by default
                        self._menu_item_highlighted = 0 
                        # apply color
                        self._update_menu_item_highlighted()
                        # play menu select sound
                        self._audio_service.play_sound("menu-select")

                else:
                    if self._keyboard_service.is_key_up('enter'):
                        # reset key_is_pressed if enter key is not still down
                        self._key_is_pressed = False

    def _handle_start_and_credit_input_checks(self, cast, script):
        """Handle checking for keyboard input when displaying the start or credits menu
        """
        # As long as the highscore menu is not being displayed
        if self._menu_state == "start" or self._menu_state == "credits" or self._menu_state == "none":

            # Only allow one key press at a time
            if self._key_is_pressed == False:
                if self._keyboard_service.is_key_down('enter'):
                    self._key_is_pressed = True

                    if self._menu_state == "start":
                        # selected first menu item "START GAME"
                        if self._menu_item_highlighted == 0:
                            # start the game
                            self._start_game(cast, script)
                            # close the menu system
                            self._close_menu(cast)
                            # play start game sound
                            self._audio_service.play_sound("menu-start")

                        # selected second menu item "CREDITS/CONTROLS"
                        elif self._menu_item_highlighted == 1:
                            # change menu state
                            self._menu_state = "credits"
                            # highlight "BACK" menu item by default
                            self._menu_item_highlighted = 2
                            # apply highlight color
                            self._update_menu_item_highlighted()
                            # update menu text values / positions
                            self._update_menu_items(cast, self._credits_menu_values, self._credits_menu_heights)
                            # play menu select sound
                            self._audio_service.play_sound("menu-select")

                        # selected third menu item "EXIT"
                        elif self._menu_item_highlighted == 2:
                            # exit game
                            self._video_service.close_window()

                    elif self._menu_state == "credits":
                        if self._menu_item_highlighted == 2:
                            # go back to start menu
                            self._menu_state = "start"
                            self._menu_item_highlighted = 0  # highlight the "ENTER TO START" menu item
                            self._update_menu_item_highlighted()
                            # update menu to start menu
                            self._update_menu_items(
                                cast, self._start_menu_values, self._start_menu_heights)
                            # play menu select sound
                            self._audio_service.play_sound("menu-select")

                    # If the menu is not being displayed and enter has been pressed
                    elif self._menu_state == "none":

                        # as long as it's not game over
                        if self._game_over != True:
                            
                            # play pause sound
                            self._audio_service.play_sound("menu-select")

                            # if we are not paused
                            if self._paused == False:
                                # PAUSE the game
                                self._paused = True
                                # find position for pause message
                                position = Point(int(constants.MAX_X / 2),
                                                 int(constants.MAX_Y * 0.45))
                                # create pause message at that position
                                pause_message = Actor()
                                pause_message.set_text("paused")
                                pause_message.set_color(constants.YELLOW)
                                pause_message.set_position(position)
                                cast.add_actor("menus", pause_message)
                                # run pause game method to stop gameplay action scripts
                                self.pause_game(script)
                            else:
                                # UNPAUSE the game
                                self._paused = False
                                # start action scripts
                                self._start_game(cast, script, False)
                                # get rid of pause display message
                                self._close_menu(cast)
                                # tell the enemy creator to start it's timer again
                                self._handle_enemy_creation_action.set_paused(False)

                # if we are looking at the start menu
                if self._menu_state == "start":

                    if self._keyboard_service.is_key_down('up'):
                        self._key_is_pressed = True
                        # when the player presses the up arrow, change the menu selection
                        self._menu_item_highlighted = (self._menu_item_highlighted - 1) % 3
                        # update text colors
                        self._update_menu_item_highlighted()

                    if self._keyboard_service.is_key_down('down'):
                        self._key_is_pressed = True
                        # when the player presses the down arrow, change the menu selection
                        self._menu_item_highlighted = (self._menu_item_highlighted + 1) % 3
                        # update text colors
                        self._update_menu_item_highlighted()

                    if self._key_is_pressed:
                        # play menu select sound if up or down was pressed
                        self._audio_service.play_sound("menu-select")

            else:
                # reset key pressed when the player lets up of the key
                if self._keyboard_service.is_key_up('enter') and self._keyboard_service.is_key_up('up') and self._keyboard_service.is_key_up('down'):
                    self._key_is_pressed = False


    def _update_initials_highlighted(self):
        """Updates the color values of initial actors to display current selection
        """
        for idx, initial in enumerate(self._initials_actors):
            # if this initial is the selected index
            if idx == self._initial_highlighted:
                # make it yellow
                initial.set_color(constants.YELLOW)
            else:
                # otherwise make it white
                initial.set_color(constants.WHITE)

    def pause_game(self, script):
        """Stops action scripts from running by removing them
        """
        # remove action scripts to stop gameplay
        script.remove_action("input", self._control_actions_action)
        script.remove_action("update", self._move_actors_action)
        script.remove_action("update", self._handle_collision_action)
        # tell the enemy creator to pause it's timer
        self._handle_enemy_creation_action.set_paused(True)

    def _reset_game(self, cast, script):
        """Get ready to start game over again. Gets rid of all gameplay actions and actors and display elements. 
        Stops drawing them.
        """
        # remove all gameplay actions
        self.pause_game(script)
        # remove additional persistent action (enemy creator)
        script.remove_action("update", self._handle_enemy_creation_action)
        # reset references to those actions
        self._control_actions_action = 0
        self._move_actors_action = 0
        self._handle_collision_action = 0
        self._handle_enemy_creation_action = 0
        # remove gameplay actors
        cast.remove_actors("ships")
        cast.remove_actors("scores")
        cast.remove_actors("shields")
        cast.remove_actors("")
        # tell drawer to stop drawing gameplay elements
        self._draw_actors_instance.set_game_started(False)

    def _close_menu(self, cast):
        """Closes menu by removing menu display elements to start the game. Resets variables for reuse later."""
        # remove menu display elements
        cast.remove_actors("menus")
        # turn our state off
        self._menu_state = "none"
        # clear our menu display items
        self._menu_items.clear
        # reset menu control variables
        self._menu_item_highlighted = 0
        self._menu_populated = False

    def _update_menu_item_highlighted(self):
        """Updates the color values of the menu actors to display current selection
        """        
        for i in range(0, 3):
            # if this index is selected
            if i == self._menu_item_highlighted:
                # turn the actors color yellow
                self._menu_items[i].set_color(constants.YELLOW)
            else:
                # turn the actors color white
                self._menu_items[i].set_color(constants.WHITE)

    def _start_game(self, cast, script, initialStart=True):
        """Start the game by setting scripts to run and creating instances of gameplay actor classes.
        """
        # create instances of actions - - -
        self._control_actions_action = ControlActorsAction(self._keyboard_service, self._audio_service)
        self._move_actors_action = MoveActorsAction()
        self._handle_collision_action = HandleCollisionsAction(self, self._audio_service)

        # add scripts to run
        script.add_action("input", self._control_actions_action)
        script.add_action("update", self._move_actors_action)
        script.add_action("update", self._handle_collision_action)

        # if we are first setting up the game (as opposed to unpausing)
        if initialStart == True:
            # enemy creator action remains persistent so it's only created once here
            self._handle_enemy_creation_action = HandleEnemyCreation(self._audio_service)
            # add it to scripts
            script.add_action("update", self._handle_enemy_creation_action)

            # create player ship
            cast.add_actor("ships", Ship())
            # create display elements (black colored at start)
            scores = Score(cast)
            shields = Shields()
            scores.set_color(constants.BLACK)
            shields.set_color(constants.BLACK)
            cast.add_actor("scores", scores)
            cast.add_actor("shields", shields)
            # tell the draw actors the game has started and to draw gameplay elements (ship, enemies, etc.)
            self._draw_actors_instance.set_game_started(True)

    def _load_highscore_table(self):
        """load highscore table values from file
        inserted (int): -1 did not make it to highscore table
                         0 made it to highscore table
                         1 new highest score!
        """
        # set to default value
        inserted = -1

        # load from file line by line into an array
        with open("gamename/game/data/highscores.txt") as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        # go through every line (ex line: "AAA 001")
        for idx, line in enumerate(lines):
            # split it into a 2D array ["AAA", "001"]
            score_split = line.split()

            # if our end score was higher than this one
            if self._end_score >= int(score_split[1]) and inserted == -1:
                if idx == 0:
                    inserted = 1 # new high score!
                else:
                    inserted = 0 # made it to the high score table
                # insert a blank line into this index of the list to make space for player initials display
                lines.insert(idx, "")
        # save this new edited version of the list
        self._high_scores = lines
        # return whether we got new highscore, made it to the highscore table, or not
        return inserted

    def _save_highscore_data(self):
        """opens highscores.txt file and saves the current list of highscore strings line by line
        """
        with open("gamename/game/data/highscores.txt", 'w') as file:
            # save top five highscore strings in list
            for i in range(0, 5):
                # if it's not blank
                if self._high_scores[i] != "":
                    # write it to the file
                    file.write(self._high_scores[i])
                else:
                    # write the new player initials and new score to the file
                    file.write(f'{self._initials[0]}{self._initials[1]}{self._initials[2]}  {str(self._end_score)}')
                # new line after each score
                file.write("\n")

    def _display_highscore_table(self, cast):
        """Display the highscore table by setting up menu items
        """
        # display top five high score strings
        for i in range(0, 5):

            # find position for this score
            position = Point(int(constants.MAX_X * 0.425),
                             int(constants.MAX_Y * 0.35) + 50 * i)
            # if it's an old score loaded into our list
            if self._high_scores[i] != "":
                # display it's text
                text = self._high_scores[i]
            else:
                # create three actors to display initials the player can edit
                for j in range(0, 3):
                    initial = Actor()
                    # set text to default initials array ("A","A","A")
                    initial.set_text(self._initials[j])
                    initial.set_position(Point(position.get_x() + j * 14, position.get_y()))
                    initial.set_font_size(20)
                    # set the first initial to yellow to show we are editing it
                    if j == 0:
                        initial.set_color(constants.YELLOW)
                    # add it to cast group and save it to array
                    cast.add_actor("highscores", initial)
                    self._initials_actors.append(initial)

                # After three initials display the end score (Ex: AAA 100)
                text = str(self._end_score)
                # modify the position so it's just to the right of the three letters
                position = Point(int(constants.MAX_X * 0.518),
                                 int(constants.MAX_Y * 0.35) + 50 * i)

            # create a display for the score string
            highscore = Actor()
            highscore.set_text(text)
            highscore.set_position(position)
            highscore.set_font_size(20)
            cast.add_actor("highscores", highscore)
