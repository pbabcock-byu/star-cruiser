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
        self._player_direction = Point(0, 0)

    def execute(self, cast, script):
        """Executes the control actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """

        # default is not moving
        self._player_direction = Point(0, 0)

        # left
        if self._keyboard_service.is_key_down('a'):
            self._player_direction = Point(-constants.CELL_SIZE, 0)
            key_pressed = True

        # right
        if self._keyboard_service.is_key_down('d'):
            self._player_direction = Point(constants.CELL_SIZE, 0)
            key_pressed = True

        # apply direction to player
        ship = cast.get_first_actor("ships")
        ship.control_ship(self._player_direction)
