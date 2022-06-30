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
        self._points = 30
        self.add_points(0)
        self.set_position(
            Point(constants.CELL_SIZE * 28, constants.CELL_SIZE * 2))

    def add_points(self, points):
        """Adds or removes points from the shield.
        If gets to zero game must end
        Args:
            points (int): The points to add.
        """
        self._points += points
        self.set_text(f"Shields Remaining: {self._points}")
