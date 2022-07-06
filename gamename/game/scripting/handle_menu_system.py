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
        _keyboard_service (KeyboardService): An instance of KeyboardService.
    """

    def __init__(self, keyboard_service, draw_actors_instance, video_service):
        """Constructs a new handleMenuSystem using the specified KeyboardService.

        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
        """
        self._keyboard_service = keyboard_service
        self._draw_actors_instance = draw_actors_instance
        self._video_service = video_service
        self._control_actions_action = 0
        self._move_actors_action = 0
        self._handle_collision_action = 0
        self._handle_enemy_creation_action = 0
        self._paused = False
        self._game_over = False
        self._end_score = 0

        self._menu_state = "start"  # start, highscore
        self._menu_populated = False
        self._menu_items = [Actor(), Actor(), Actor()]
        self._menu_item_highlighted = 0
        self._key_is_pressed = False
        # high score data
        self._high_scores = []
        self._initials = ["A", "A", "A"]
        self._initials_actors = []
        self._initial_highlighted = -1

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

    def set_game_over(self, game_over):
        self._game_over = game_over
        self._handle_enemy_creation_action.set_paused(True)

    def set_menu_state(self, menu_state):
        self._menu_state = menu_state
        self._menu_populated = False

    def _update_menu_items(self, cast, values, heights):
        # populate menu
        for i in range(0, 3):
            # get center screen position
            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y * heights[i])
            position = Point(x, y)
            # create a game over message at that position
            menu = self._menu_items[i]
            menu.set_text(values[i])
            menu.set_position(position)
            if i == self._menu_item_highlighted:
                menu.set_color(constants.YELLOW)
            cast.add_actor("menus", menu)
            self._menu_items.append(menu)

    def execute(self, cast, script):
        """Executes the handle menu system
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if self._menu_state != "none" and self._menu_populated == False:
            # set to true
            self._menu_populated = True

            if self._menu_state == "start":
                # update menu to start menu
                self._update_menu_items(
                    cast, self._start_menu_values, self._start_menu_heights)
                # create game title
                position = Point(int(constants.MAX_X / 2),
                                 int(constants.MAX_Y * 0.1))
                # create a game over message at that position
                title = Actor()
                title.set_text("STAR CRUISER 5000")
                title.set_position(position)
                title.set_font_size(30)
                title.set_color(constants.AQUA)
                cast.add_actor("menus", title)

            if self._menu_state == "highscore":
                # pause the enemy creator
                self._handle_enemy_creation_action.set_paused(True)
                # update end score
                self._end_score = cast.get_first_actor("scores").get_points()
                # display highscore table
                made_it = self._load_highscore_table()
                if made_it >= 0:  # if we made it to the highscore table
                    if made_it == 1:
                        self._highscore_menu_values[0] = "NEW HIGH SCORE!!!"
                    else:
                        self._highscore_menu_values[0] = "You made it to the high score table!"
                    self._highscore_menu_values[1] = "Enter your initials then press ENTER"
                    # select none of the menu items
                    self._menu_item_highlighted = -1
                    self._initial_highlighted = 0
                else:
                    # do not display enter initials
                    self._highscore_menu_values[0] = "You did not get a high score."
                    self._highscore_menu_values[1] = ""
                    # select none of the menu items
                    self._menu_item_highlighted = 2
                    self.__initial_highlighted = 1

                # update menu to high score menu
                self._update_menu_items(
                    cast, self._highscore_menu_values, self._highscore_menu_heights)
                self._update_menu_item_highlighted()
                # display the highscore table
                self._display_highscore_table(cast)
                # HIGH SCORE TABLE title
                position = Point(int(constants.MAX_X / 2),
                                 int(constants.MAX_Y * 0.1))
                # create a game over message at that position
                title = Actor()
                title.set_text("HIGH SCORE TABLE")
                title.set_position(position)
                title.set_font_size(20)
                title.set_color(constants.PINK)
                cast.add_actor("menus", title)
                # stop game completely
                self._reset_game(cast, script)

        if self._menu_state == "highscore":
            # if we are still selecting initials
            if self._initial_highlighted >= 0:
                if self._key_is_pressed == False:
                    try_letter_key = self._keyboard_service.is_any_letter_key_down()
                    if try_letter_key != False:
                        # a letter key has been pressed
                        self._key_is_pressed = True
                        self._initials_actors[self._initial_highlighted].set_text(
                            try_letter_key.upper())
                        self._initials[self._initial_highlighted] = try_letter_key.upper(
                        )
                        self._initial_highlighted += 1

                    elif self._keyboard_service.is_key_down('right'):
                        self._key_is_pressed = True
                        self._initial_highlighted = (
                            self._initial_highlighted + 1) % 3

                    elif self._keyboard_service.is_key_down('left'):
                        self._key_is_pressed = True
                        self._initial_highlighted = (
                            self._initial_highlighted - 1) % 3

                    elif self._keyboard_service.is_key_down('back'):
                        self._key_is_pressed = True
                        self._initial_highlighted -= 1

                    if self._key_is_pressed == True:
                        if self._initial_highlighted > 2:
                            self._initial_highlighted = 2
                        if self._initial_highlighted < 0:
                            self._initial_highlighted = 0
                        # update which initials is highlighted
                        self._update_initials_highlighted()

                    elif self._keyboard_service.is_key_down('enter'):
                        self._key_is_pressed = True
                        # DONE ENTERING INTITIALS
                        self._initial_highlighted = -1
                        self._update_initials_highlighted()
                        self._menu_item_highlighted = 2
                        self._update_menu_item_highlighted()
                        # do not display instructions text for entering initials after we are done
                        self._highscore_menu_values[0] = ""
                        self._highscore_menu_values[1] = ""
                        self._update_menu_items(
                            cast, self._highscore_menu_values, self._highscore_menu_heights)

                else:
                    try_letter_key = self._keyboard_service.is_any_letter_key_down()
                    if try_letter_key == False:
                        if self._keyboard_service.is_key_up('enter') and self._keyboard_service.is_key_up('right') and self._keyboard_service.is_key_up('left'):
                            self._key_is_pressed = False
            else:
                if self._key_is_pressed == False:
                    if self._keyboard_service.is_key_down('enter'):
                        self._key_is_pressed = True
                        # done looking at high score table
                        cast.remove_actors("highscores")
                        self._save_highscore_data()
                        # reset high score data
                        self._high_scores = []
                        self._initials = ["A", "A", "A"]
                        self._initials_actors = []
                        self._initial_highlighted = 0
                        # reset menu
                        self._close_menu(cast)
                        # reopen start menu
                        self._menu_state = "start"
                        self._menu_item_highlighted = 0  # highlight the "ENTER TO START" menu item
                        self._update_menu_item_highlighted()

                else:
                    if self._keyboard_service.is_key_up('enter'):
                        self._key_is_pressed = False

        if self._menu_state == "start" or self._menu_state == "credits" or self._menu_state == "none":
            if self._key_is_pressed == False:
                if self._keyboard_service.is_key_down('enter'):
                    self._key_is_pressed = True
                    if self._menu_state == "start":
                        if self._menu_item_highlighted == 0:
                            self._start_game(cast, script)
                            # close the menu system
                            self._close_menu(cast)
                        elif self._menu_item_highlighted == 1:
                            self._menu_state = "credits"
                            self._menu_item_highlighted = 2  # highlight the "BACK" menu item
                            self._update_menu_item_highlighted()
                            self._update_menu_items(
                                cast, self._credits_menu_values, self._credits_menu_heights)
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

                    elif self._menu_state == "none":

                        if self._game_over != True:
                            # as long as it's not game over enable pausing
                            if self._paused == False:
                                self._paused = True
                                # PAUSE GAME
                                # create pause message
                                position = Point(int(constants.MAX_X / 2),
                                                 int(constants.MAX_Y * 0.45))
                                # create a game over message at that position
                                pause_message = Actor()
                                pause_message.set_text("paused")
                                pause_message.set_color(constants.YELLOW)
                                pause_message.set_position(position)
                                cast.add_actor("menus", pause_message)

                                self.pause_game(script)
                            else:
                                self._paused = False
                                self._start_game(cast, script, False)
                                self._close_menu(cast)
                                self._handle_enemy_creation_action.set_paused(
                                    False)

                if self._menu_state == "start":
                    if self._keyboard_service.is_key_down('up'):
                        self._key_is_pressed = True
                        self._menu_item_highlighted = (
                            self._menu_item_highlighted - 1) % 3
                        self._update_menu_item_highlighted()

                    if self._keyboard_service.is_key_down('down'):
                        self._key_is_pressed = True
                        self._menu_item_highlighted = (
                            self._menu_item_highlighted + 1) % 3
                        self._update_menu_item_highlighted()

            else:
                if self._keyboard_service.is_key_up('enter') and self._keyboard_service.is_key_up('up') and self._keyboard_service.is_key_up('down'):
                    self._key_is_pressed = False

    def _update_initials_highlighted(self):
        for idx, initial in enumerate(self._initials_actors):
            if idx == self._initial_highlighted:
                initial.set_color(constants.YELLOW)
            else:
                initial.set_color(constants.WHITE)

    def pause_game(self, script):
        if self._control_actions_action != 0 and self._move_actors_action != 0 and self._handle_collision_action != 0 and self._handle_enemy_creation_action != 0:
            # remove action scripts
            script.remove_action(
                "input", self._control_actions_action)
            script.remove_action(
                "update", self._move_actors_action)
            script.remove_action(
                "update", self._handle_collision_action)
            self._handle_enemy_creation_action.set_paused(True)

    def _reset_game(self, cast, script):
        # remove all pause actions
        self.pause_game(script)
        # remove additional persistent acitons
        script.remove_action("update", self._handle_enemy_creation_action)
        # reset variables
        self._control_actions_action = 0
        self._move_actors_action = 0
        self._handle_collision_action = 0
        self._handle_enemy_creation_action = 0
        # remove gameplay actors
        cast.remove_actors("ships")
        cast.remove_actors("scores")
        cast.remove_actors("shields")
        cast.remove_actors("")
        self._draw_actors_instance.set_game_started(False)

    def _close_menu(self, cast):
        cast.remove_actors("menus")
        self._menu_state = "none"
        self._menu_items.clear
        self._menu_item_highlighted = 0
        self._menu_populated = False

    def _update_menu_item_highlighted(self):
        for i in range(0, 3):
            if i == self._menu_item_highlighted:
                self._menu_items[i].set_color(constants.YELLOW)
            else:
                self._menu_items[i].set_color(constants.WHITE)

    def _start_game(self, cast, script, initialStart=True):
        """Start the game by setting scripts to run and creating instances of classes"""
        # create instances of actions
        self._control_actions_action = ControlActorsAction(
            self._keyboard_service)
        self._move_actors_action = MoveActorsAction()
        self._handle_collision_action = HandleCollisionsAction(
            self._keyboard_service, self)

        # add scripts to run
        script.add_action(
            "input", self._control_actions_action)
        script.add_action("update", self._move_actors_action)
        script.add_action(
            "update", self._handle_collision_action)

        if initialStart == True:

            # enemy creator remains persistent
            self._handle_enemy_creation_action = HandleEnemyCreation()
            script.add_action("update", self._handle_enemy_creation_action)

            # create player ship
            cast.add_actor("ships", Ship())
            # create display elements
            scores = Score(cast)
            shields = Shields()
            scores.set_color(constants.BLACK)
            shields.set_color(constants.BLACK)
            cast.add_actor("scores", scores)
            cast.add_actor("shields", shields)
            # tell the draw actors the game has started
            self._draw_actors_instance.set_game_started(True)

    def _load_highscore_table(self):
        """load highscore table from file"""

        # load from file
        with open("gamename/game/data/highscores.txt") as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        # defauls status is -1 (did not make it to high score table)
        inserted = -1
        # go through every line "AAA 001"
        for idx, line in enumerate(lines):
            # split it into a 2D array ["AAA", "001"]
            score_split = line.split()
            # if our end score was higher than this one
            if self._end_score >= int(score_split[1]) and inserted == -1:
                if idx == 0:
                    # new high score
                    inserted = 1
                else:
                    # made it to the high score table
                    inserted = 0
                lines.insert(idx, "")

        # set to new version with our score inserted
        self._high_scores = lines
        # return whether we made it to the highscore table or not
        return inserted

    def _save_highscore_data(self):
        with open("gamename/game/data/highscores.txt", 'w') as file:
            for i in range(0, 5):
                if self._high_scores[i] != "":
                    file.write(self._high_scores[i])
                else:
                    file.write(
                        f'{self._initials[0]}{self._initials[1]}{self._initials[2]}  {str(self._end_score)}')
                # new line after each score
                file.write("\n")

    def _display_highscore_table(self, cast):
        # display five high score things
        for i in range(0, 5):
            # set default position
            position = Point(int(constants.MAX_X * 0.425),
                             int(constants.MAX_Y * 0.35) + 50 * i)
            # if it's a past score
            if self._high_scores[i] != "":

                text = self._high_scores[i]
            else:
                # create an initials actors
                for j in range(0, 3):
                    initial = Actor()
                    initial.set_text(self._initials[j])
                    initial.set_position(
                        Point(position.get_x() + j * 14, position.get_y()))
                    initial.set_font_size(20)
                    if j == 0:
                        initial.set_color(constants.YELLOW)
                    cast.add_actor("highscores", initial)
                    self._initials_actors.append(initial)

                # set up string and position for score value
                text = str(self._end_score)
                # it's our new score
                position = Point(int(constants.MAX_X * 0.518),
                                 int(constants.MAX_Y * 0.35) + 50 * i)

            # create a display for it
            highscore = Actor()
            highscore.set_text(text)
            highscore.set_position(position)
            highscore.set_font_size(20)
            cast.add_actor("highscores", highscore)
