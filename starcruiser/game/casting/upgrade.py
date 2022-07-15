import constants
from game.casting.actor import Actor
from game.shared.point import Point




class Upgrade(Actor):
    """
    

    Attributes:

    """

    def __init__(self, cast):
        super().__init__()
        self._cast = cast
        self._type = "shield"
        self._wait_timer = 0
        self._wait_amount = 3

    def get_type(self):
        return self._type
        
    def set_type(self, type):
        self._type = type
        
    def set_wait_amount(self, wait_amount):
        self._wait_amount = wait_amount

        

    def move_next(self):
        """ (OVERRIDE) moves sparks and destroys when outside window
        """
        if self._position._x > constants.MAX_X or self._position._x < 0 or self._position._y < 0 or self._position._y > constants.MAX_Y:
            # after animation is complete delete ourself
            self._cast.remove_actor("upgrades", self)
        else:
            if self._wait_timer > self._wait_amount:
                self._wait_timer = 0
                # move
                x = round(self._position.get_x() + self._velocity.get_x())
                y = round(self._position.get_y() + self._velocity.get_y())
                self._position = Point(x, y)
        
            self._wait_timer += 1



