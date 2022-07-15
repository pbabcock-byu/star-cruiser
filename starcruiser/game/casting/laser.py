import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Laser(Actor):
    """
    A Laser

    The responsibility of Laser is to move upwards and delete itself when offscreen.

    Attributes:
        damage (int): how powerful this laser is (how much damage it does to enemies)
    """

    def __init__(self, cast):
        super().__init__()
        self._cast = cast
        # default
        self._damage = 1

    def get_damage(self):
        return self._damage
        
    def set_damage(self, damage):
        self._damage = damage

    
    def move_next(self):
        """ (OVERRIDE) Moves the laser to its next position according to its velocity. 
        Will wrap the x position from one side of the screen to the other when it reaches the given maximum x.
        Args:
            max_x (int): The maximum x value.
        """
        # determine movement (wrap x)
        x = (self._position.get_x() + self._velocity.get_x()) % constants.MAX_X
        y = (self._position.get_y() + self._velocity.get_y())
        # if laser goes off the top of the screen
        if y <= 0:
            # delete it
            self._cast.remove_actor("lasers", self)
        else:
            # apply movement
            self._position = Point(x, y)
