
import constants
import random
from game.casting.actor import Actor
from game.shared.point import Point


class Asteroid(Actor):
    """
    Asteriod are objects that will be flying in space
    different size asteriod will do diffent amounts of damage if they hit the space ship
    Also the bigger an the less points the player will get for shooting it

    Attributes:
        _type (String): "LRG" or "MED" or "SML"
    """

    def __init__(self, cast):
        super().__init__()
        self._cast = cast
        # default attributes
        self._type = "SML"
        self._move_wait = 4
        self._move_timer = 0

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
        # update attributes based on type
        if self._type == "SML":
            self._move_wait = random.choice([2, 3, 4])
            self._move_timer = 0

        if self._type == "MED":
            self._move_wait = random.choice([3, 4])
            self._move_timer = 0

        if self._type == "LRG":
            self._move_wait = 4
            self._move_timer = 0

    def move_next(self):
        """ (OVERRIDE) Moves the actor to its next position according to its velocity. Will wrap the position 
        from one side of the screen to the other when it reaches the given maximum (X ONLY FOR LASER).

        Args:
            max_x (int): The maximum x value.
        """

        if self._move_timer == 0:
            # reset move timer
            self._move_timer = self._move_wait
            # determine movement (wrap x)
            x = (self._position.get_x() + self._velocity.get_x()) % constants.MAX_X
            y = (self._position.get_y() + self._velocity.get_y())

            # if asteroid goes off screen
            if y >= constants.MAX_Y:
                # delete it
                self._cast.remove_actor("asteroids", self)
            else:
                # apply movement
                self._position = Point(x, y)
        else:
            # waiting a few frames before moving again
            self._move_timer -= 1
