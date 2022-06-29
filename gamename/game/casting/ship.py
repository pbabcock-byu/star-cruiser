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
        self._prepare_shape()
        self._is_dead = False

    def get_parts(self):
        return self._parts

    def get_is_dead(self):
        return self._is_dead

    def set_is_dead(self, is_dead):
        self._is_dead = is_dead

    def move_next(self):
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

    def _prepare_shape(self):
        x = int(constants.MAX_X * 0.5)
        y = int(constants.MAX_Y - constants.CELL_SIZE * 8)

        ship_layout_info = [["+", 0, 0, 0], ["A", 0, 1, 0], ["H", 0, 2, 1], [
            "=", -1, 2, 0], ["=", 1, 2, 0], ["_", -2, 2, 0], ["_", 2, 2, 0], ['*', 0, 3, 2]]
        ship_color_info = [constants.GREEN, constants.BLUE, constants.RED]

        for ship_part in ship_layout_info:
            position = Point(
                x + ship_part[1] * constants.CELL_SIZE, y + ship_part[2] * constants.CELL_SIZE)
            velocity = Point(0, 0)
            text = ship_part[0]
            color = ship_color_info[ship_part[3]]
            part = Actor()
            part.set_position(position)
            part.set_velocity(velocity)
            part.set_text(text)
            part.set_color(color)
            self._parts.append(part)
