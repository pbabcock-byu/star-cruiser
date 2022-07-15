import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Shields(Actor):
    """
    Attributes:
        points (int): The Shields left.
        flash_timer (int): Used to make shields display flash colors for a certain amount of time when player gets hit
        wait_flash (int): used by flash_timer
        color_toggle (int): used by flash_timer
    """

    def __init__(self):
        super().__init__()
        # default amount of points
        self._points = 10
        self._flash_timer = 0
        self._wait_flash = 0
        self._color_toggle = 0
        # call on creation
        self._set_up_shields_display()

    def get_points(self):
        return self._points

    def _set_up_shields_display(self):
        # set it's position on the screen
        self.set_position(Point(constants.CELL_SIZE * 28, constants.CELL_SIZE * 2))
        # set text value
        self.set_text(f"Shields Remaining: {self._points}")

    def add_points(self, points):
        """Adds or removes points from the shield.
        If gets to zero game must end
        Args:
            points (int): The points to add.
        """
        self._points += points
        self.set_text(f"Shields Remaining: {self._points}")

        # if the amount of points applied was negative (meaning we lost points)
        if points < 0:
            # set the flash timer to run for 15 frames
            self._flash_timer = 15

    def move_next(self):
        """(OVERRIDE) method used to control flashing animation that gets updated each frame."""

        # maks sure we haven't been set to hidden by the menu (black color)
        if self.get_color() != constants.BLACK:

            # do some funny things with timers. (should have used Modulo, oh well)
            if self._flash_timer > 0:
                self._flash_timer -= 1
                self._wait_flash -= 1
                # when flash wait timer runs out
                if self._wait_flash <= 0: 
                    self._wait_flash = 2
                    if(self._color_toggle == 0):
                        self._color_toggle = 1
                        self.set_color(constants.RED) # toggle the color of the text display
                    else:
                        self._color_toggle = 0
                        self.set_color(constants.WHITE)

            # if it's not supposed to be flashing anymore
            elif self.get_color() != constants.WHITE:
                # make sure the text color is white
                self.set_color(constants.WHITE)
