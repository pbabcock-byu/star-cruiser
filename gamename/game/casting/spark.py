from math import cos, sin, radians
import constants
from game.casting.actor import Actor
from game.shared.point import Point
from game.shared.color import Color
import random


class Spark(Actor):
    """
    A small spark

    The responsibility of Explosion is to animate then disappear

    Attributes:

    """

    def __init__(self, cast):
        super().__init__()
        self._cast = cast
        self._bright = 255
        self._dim_speed = random.choice([5, 8, 12])
        self._speed = 10
        self._direction = radians(random.random()*360)

    def set_speed(self, speed):
        self._speed = speed

    def set_direction(self, direction):
        self._direction = radians(direction)

    def move_next(self):
        """ (OVERRIDE) moves sparks and destroys when outside window
        """
        if self._position._x >= constants.MAX_X or self._position._x <= 0 or self._position._y <= 0 or self._position._y >= constants.MAX_Y or self._bright <= 0:
            # after animation is complete delete ourself
            self._cast.remove_actor("sparks", self)
        else:

            self._velocity._x = self._speed * cos(self._direction)
            self._velocity._y = self._speed * sin(self._direction)

            # move
            x = round(self._position.get_x() + self._velocity.get_x())
            y = round(self._position.get_y() + self._velocity.get_y())
            self._position = Point(x, y)

            # dim over time
            self._bright -= self._dim_speed
            if(self._bright < 0):
                self._bright = 0
            self.set_color(Color(self._bright, self._bright, self._bright))
