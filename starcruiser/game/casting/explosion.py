from math import floor
import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Explosion(Actor):
    """
    An explosion

    The responsibility of Explosion is to animate then disappear

    Attributes:
        frame (int): the frame of the animation
        frame_text_animation (list of strings): text characters that are dislpayed in succession as an animation
        frame_color_animation (list of ints): references to colors that are displayed in succession as an animation
        frame_colors (list of Colors): list of the colors used by this animation
        animate_speed (float): the rate at which to progress the animation frames
    """

    def __init__(self, cast):
        super().__init__()
        self._cast = cast

        self._frame = 0
        self._frame_text_animation = [".", "*", "@", "0", "()"]
        self._frame_color_animation = [0, 1, 2, 3, 3]
        self._frame_colors = [constants.WHITE,constants.YELLOW, constants.ORANGE, constants.RED]
        self._animate_speed = 1

    def set_animate_speed(self, speed):
        self._animate_speed = speed

    def move_next(self):
        """ (OVERRIDE) Animates an explosion that also moves
        """
        if self._frame >= len(self._frame_text_animation):
            # after animation is complete delete ourself
            self._cast.remove_actor("explosions", self)
        else:  
            # continue animation (update visuals)
            self.set_text(self._frame_text_animation[floor(self._frame)])
            self.set_color(self._frame_colors[self._frame_color_animation[floor(self._frame)]])
            # increment frame by speed
            self._frame += self._animate_speed
            # move location
            x = (self._position.get_x() + self._velocity.get_x()) % constants.MAX_X
            y = (self._position.get_y() + self._velocity.get_y()) % constants.MAX_Y
            self._position = Point(x, y)
