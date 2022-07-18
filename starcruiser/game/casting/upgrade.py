import constants
from game.casting.actor import Actor
from game.shared.point import Point
from game.shared.color import Color
from math import cos, sin, radians


class Upgrade(Actor):
    """
    Upgrade is an Actor that slowly moves down the screen and when the player touches it they get an upgrade.
    The job of upgrade class is to move itself, animate it's color, and remove itself if it goes off screen.

    Attributes:
    type (string): used to keep track of the type of upgrade
    color_fade (float): used to oscillate the color to make it noticable to the player
    """

    def __init__(self, cast):
        super().__init__()
        self._cast = cast
        self._type = "shield"
        self._color_fade = 0

    def get_type(self):
        return self._type
        
    def set_type(self, type):
        self._type = type
        # change appearence based on type
        if self._type == "gun-rapid":
            self.set_text("><")
        # change appearence based on type
        if self._type == "gun-shotgun":
            self.set_text("}{")


    def move_next(self):
        """ (OVERRIDE) moves sparks and destroys when outside window
        """
        if self._position._x > constants.MAX_X or self._position._x < 0 or self._position._y < 0 or self._position._y > constants.MAX_Y:
            # after animation is complete delete ourself
            self._cast.remove_actor("upgrades", self)
        else:
                # move
                x = round(self._position.get_x() + self._velocity.get_x())
                y = round(self._position.get_y() + self._velocity.get_y())
                self._position = Point(x, y)


        # make the upgrade oscillate its color as it falls
        self._color_fade += 0.3
        # generate values
        r = abs(round(cos(self._color_fade)*255))
        g = abs(round(sin(self._color_fade)*255))
        b = 0
        # update the color
        self.set_color(Color(r,g,b))
        



