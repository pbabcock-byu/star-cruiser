import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Ship(Actor):
    """
    A spaceship

    The responsibility of Ship is to move itself.

    Attributes:

    """

    def __init__(self):
        super().__init__()
        self._parts = []
        self._prepare_ship()
        self._is_hurt = False

    def get_is_hurt(self):
        return self._is_hurt

    def set_is_hurt(self, is_hurt):
        self._is_hurt = is_hurt

    def get_parts(self):
        return self._parts

    def remove_parts(self):
        self._parts.clear()

    def reset_ship(self):
        self._prepare_ship()

    def move_next(self):
        # if the body exists
        if len(self._parts) > 0:
            # move all parts
            for part in self._parts:
                part.move_next()
            # animate thrust
            if self._parts[7].get_text() == '*':
                self._parts[7].set_text("'")
                self._parts[7].set_color(constants.ORANGE)
            else:
                self._parts[7].set_text('*')
                self._parts[7].set_color(constants.RED)

    def control_ship(self, velocity):
        for part in self._parts:
            part.set_velocity(velocity)

    def _prepare_ship(self):
        """
        Creates the ship by making a list of ship parts relative to the x,y starting position
        self._parts
        """
        # set origin position
        x = int(constants.MAX_X * 0.5)
        y = int(constants.MAX_Y - constants.CELL_SIZE * 8)
        # set ship layout
        ship_layout = [["+", 0, 0, 0], ["A", 0, 1, 0], ["H", 0, 2, 1], [
            "=", -1, 2, 0], ["=", 1, 2, 0], ["_", -2, 2, 0], ["_", 2, 2, 0], ['*', 0, 3, 2]]
        ship_colors = [constants.BLUE, constants.WHITE, constants.RED]
        # generate parts list based on layout
        self._parts = self._generate_structure(
            Point(x, y), Point(0, 0), ship_layout, ship_colors)
