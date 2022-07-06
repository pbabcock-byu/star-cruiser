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

        self._menu_state = "start"  # start, highscore
        self._menu_populated = False
        self._menu_items = [Actor(), Actor(), Actor()]
        self._menu_item_highlighted = 0
        self._key_is_pressed = False
        # start menu
        self._start_menu_values = [
            "ENTER TO START", "CREDITS / CONTROLS", "EXIT"]
        self._start_menu_heights = [0.4, 0.5, 0.6]
        # credits menu
        self._credits_menu_values = [
            "\t\t\t\t\t\t\t\tCONTROLS:\nmove = left/right arrow keys \n \t\t\t\t\t\tshoot = space \n \t\t\t\t\t\tpause = enter", "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCREDITS:\n Kyle Coulon, Rachel Knight, Peter Babcock", "BACK"]
        self._credits_menu_heights = [0.4, 0.6, 0.8]
        # high score data
        self._high_scores = []
        # test
        self._load_highscore_table()

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
            # update menu to start menu
            self._update_menu_items(
                cast, self._start_menu_values, self._start_menu_heights)
            # create game title
            position = Point(int(constants.MAX_X / 2),
                             int(constants.MAX_Y * 0.2))
            # create a game over message at that position
            title = Actor()
            title.set_text("STAR CRUISER 5000")
            title.set_position(position)
            title.set_font_size(30)
            cast.add_actor("menus", title)

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
                    if self._paused == False:
                        self._paused = True
                        if self._control_actions_action != 0 and self._move_actors_action != 0:
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

                            # remove action scripts
                            script.remove_action(
                                "input", self._control_actions_action)
                            script.remove_action(
                                "update", self._move_actors_action)
                            script.remove_action(
                                "update", self._handle_collision_action)
                            self._handle_enemy_creation_action.set_paused(True)
                    else:
                        self._paused = False
                        self._start_game(cast, script, False)
                        self._close_menu(cast)
                        self._handle_enemy_creation_action.set_paused(False)

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
            self._keyboard_service)

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
        # reset high scores
        self._high_scores = []

        # load from file
        with open("gamename/game/data/highscores.txt") as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        # append to highscores
        self._high_scores.append(lines)
