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
        bright (int): starting brightness value 255=white 0=black
        dim_speed (int): how quickly the brightness of the spark fades
        speed (float): how fast the spark moves
        direction (int): direction in degress the spark is going to move
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
        """ (Override of Actor's method) - Moves sparks and destroys when outside window or brightness is zero
        """
        # if spark goes outside the screen or brightness is zero
        if self._position._x >= constants.MAX_X or self._position._x <= 0 or self._position._y <= 0 or self._position._y >= constants.MAX_Y or self._bright <= 0:
            # delete it
            self._cast.remove_actor("sparks", self)
        else:
            # calculate relative x/y movement based on direction and speed
            self._velocity._x = self._speed * cos(self._direction)
            self._velocity._y = self._speed * sin(self._direction)

            # apply movement
            x = round(self._position.get_x() + self._velocity.get_x())
            y = round(self._position.get_y() + self._velocity.get_y())
            self._position = Point(x, y)

            # dim spark brightness over time
            self._bright -= self._dim_speed
            # no less than zero
            self._bright = max(self._bright, 0)

            # apply new color
            self.set_color(Color(self._bright, self._bright, self._bright))
