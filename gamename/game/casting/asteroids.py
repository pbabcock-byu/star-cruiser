
import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Asteriod(Actor):
    """
    Asteriod are objects that will be flying in space
    different size asteriod will do diffent amounts of damage if they hit the space ship
    Also the bigger an the less points the player will get for shooting it

    Attributes:
        _type (String): "LRG" or "MED" or "SML"
    """

    def __init__(self):
        super().__init__()
        self._type = "SML"

    def get_type(self):
        """Gets the Asteriod's size
        Returns:
            string: The type.
        """
        return self._type

    def set_type(self, type):
        """Updates Asteriod's size.
        Args:
            type (string): The Asteriod's size.
        """
        self._type = type
