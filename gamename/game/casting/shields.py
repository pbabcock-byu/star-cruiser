import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Shields(Actor):
    """
    Attributes:
        _points (int): The Shields left.
    """

    def __init__(self):
        super().__init__()
        self._points = 10
        self.add_points(0)
        self.set_position(
            Point(constants.CELL_SIZE * 28, constants.CELL_SIZE * 2))
        self._flash_timer = 0
        self._wait_flash = 0
        self._color_toggle = 0

    def add_points(self, points):
        """Adds or removes points from the shield.
        If gets to zero game must end
        Args:
            points (int): The points to add.
        """
        self._points += points
        self.set_text(f"Shields Remaining: {self._points}")

        if points < 0:
            self._flash_timer = 15

    def get_points(self):
        """Returns the value of self._points"""
        return self._points

    def move_next(self):

        if self.get_color() != constants.BLACK:

            if self._flash_timer > 0:
                self._flash_timer -= 1
                self._wait_flash -= 1
                if self._wait_flash <= 0:
                    self._wait_flash = 2
                    if(self._color_toggle == 0):
                        self._color_toggle = 1
                        self.set_color(constants.RED)
                    else:
                        self._color_toggle = 0
                        self.set_color(constants.WHITE)

            elif self.get_color() != constants.WHITE:
                self.set_color(constants.WHITE)
