import constants
from game.scripting.action import Action
from game.shared.point import Point


class ControlActorsAction(Action):
    """
    An input action that controls the snake.

    The responsibility of ControlActorsAction is to get the direction and move the snake's head.

    Attributes:
        _keyboard_service (KeyboardService): An instance of KeyboardService.
    """

    def __init__(self, keyboard_service):
        """Constructs a new ControlActorsAction using the specified KeyboardService.

        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
        """
        self._keyboard_service = keyboard_service
        self._first_player_direction = Point(0, -constants.CELL_SIZE)
        self._second_player_direction = Point(0, constants.CELL_SIZE)

    def execute(self, cast, script):
        """Executes the control actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        # Player 1 controls
        p1_key_pressed = False

        # left
        if self._keyboard_service.is_key_down('a'):
            self._first_player_direction = Point(-constants.CELL_SIZE, 0)
            p1_key_pressed = True

        # right
        if self._keyboard_service.is_key_down('d'):
            self._first_player_direction = Point(constants.CELL_SIZE, 0)
            p1_key_pressed = True

        # up
        if self._keyboard_service.is_key_down('w'):
            self._first_player_direction = Point(0, -constants.CELL_SIZE)
            p1_key_pressed = True

        # down
        if self._keyboard_service.is_key_down('s'):
            self._first_player_direction = Point(0, constants.CELL_SIZE)
            p1_key_pressed = True

        # player 2 controls
        p2_key_pressed = False

        # left
        if self._keyboard_service.is_key_down('j'):
            self._second_player_direction = Point(-constants.CELL_SIZE, 0)
            p2_key_pressed = True

        # right
        if self._keyboard_service.is_key_down('l'):
            self._second_player_direction = Point(constants.CELL_SIZE, 0)
            p2_key_pressed = True

        # up
        if self._keyboard_service.is_key_down('i'):
            self._second_player_direction = Point(0, -constants.CELL_SIZE)
            p2_key_pressed = True

        # down
        if self._keyboard_service.is_key_down('k'):
            self._second_player_direction = Point(0, constants.CELL_SIZE)
            p2_key_pressed = True

        # apply directions to player
        # snakes = cast.get_actors("snakes")
        # for snake in snakes:
        #     if snake.get_player() == "first":
        #         if p1_key_pressed:
        #             snake.turn_head(self._first_player_direction)
        #     if snake.get_player() == "second":
        #         if p2_key_pressed:
        #             snake.turn_head(self._second_player_direction)
