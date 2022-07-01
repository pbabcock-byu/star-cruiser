
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
        _type (String): "LRG" or "MED" or "SML" or "HUGE"
    """

    def __init__(self, cast, type):
        super().__init__()
        self._cast = cast
        # default attributes
        self._type = type
        self._move_wait = 4
        self._move_timer = 0
        self._parts = [self]
        self._health = constants.ASTEROID_SINGLE_HEALTH

    def get_parts(self):
        return self._parts

    def get_type(self):
        """Gets the Asteriod's size
        Returns:
            string: The type.
        """
        return self._type

    def set_up_parts(self):
        """Updates Asteriod's size.
        Args:
            type (string): The Asteriod's size.
        """
        # update attributes based on type
        if self._type == "SML":
            self._move_wait = random.choice([2, 3, 4])

        if self._type == "MED":
            self._move_wait = random.choice([3, 4])

        if self._type == "LRG":
            self._move_wait = 4

        if self._type in ["HUGE"]:
            # this astroid is structure of multiple actors
            # self._parts.clear()

            #self._health = constants.ASTEROIDS_HUGE_HEALTH
            self._move_wait = 2
            self._prepare_huge_asteroid_body()

    def _prepare_huge_asteroid_body(self):
        """
        Creates the structure of actors to form a huge asteroid
        self._parts
        """
        # set origin position
        origin = self.get_position()

        # set layout information
        asteroid_layout = [["@", 0, 0, 0], ["@", 1, 0, 0], ["@", -1, 0, 0], ["@", 0, 1, 0], ["@", 0, -1, 0],
                           ["@", -1, -1, 0], ["@", 1, -1, 0],
                           ["@", -1, 1, 0], ["@", 1, 1, 0],
                           ["@", -2, 0, 0], ["@", 0, -2, 0], ["@", 2, 0, 0], ["@", 0, 2, 0]]
        asteroid_colors = [constants.BROWN]

        # generate parts list from layout
        self._parts = self._generate_structure(
            origin, self._velocity, asteroid_layout, asteroid_colors)

    def move_next(self):
        """ (OVERRIDE) Moves the actor to its next position according to its velocity. Will wrap the position 
        from one side of the screen to the other when it reaches the given maximum (X ONLY FOR LASER).

        Args:
            max_x (int): The maximum x value.
        """
        if self._move_timer == 0:
            # reset move timer
            self._move_timer = self._move_wait

            # if asteroid is off screen
            if self._position.get_y() >= constants.MAX_Y + constants.CELL_SIZE * 5:
                # delete it
                self._cast.remove_actor("asteroids", self)
            else:
                # apply movement to all parts
                for part in self._parts:
                    x = (part._position.get_x() +
                         self._velocity.get_x()) % constants.MAX_X
                    y = (part._position.get_y() + self._velocity.get_y())
                    # move part
                    part._position = Point(x, y)

        else:
            # waiting a few frames before moving again
            self._move_timer -= 1
