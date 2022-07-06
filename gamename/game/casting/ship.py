import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Ship(Actor):
    """
    A spaceship

    The responsibility of Ship is to move itself.

    Attributes:

    """

    def __init__(self):
        super().__init__()
        self._parts = []
        self._prepare_ship()
        self._is_hurt = False
        self._is_hurt_timer = 0
        self._is_dead = False
        self._flash_color = constants.AQUA

    def get_is_hurt(self):
        return self._is_hurt

    def get_is_dead(self):
        return self._is_dead

    def set_is_dead(self, is_dead):
        self._is_dead = is_dead
        self._is_hurt = False

    def set_is_hurt(self, is_hurt):
        self._is_hurt = is_hurt
        if is_hurt == True:
            self._is_hurt_timer = 10

    def get_parts(self):
        return self._parts

    def remove_parts(self):
        self._parts.clear()

    def reset_ship(self):
        self._is_hurt = False
        self._is_dead = False
        self._prepare_ship()

    def move_next(self):
        # if the body exists
        if len(self._parts) > 0:
            # move all parts
            for part in self._parts:
                part.move_next()
            # animate thrust
            if self._parts[7].get_text() == '*':
                self._parts[7].set_text("'")
                self._parts[7].set_color(constants.ORANGE)
            else:
                self._parts[7].set_text('*')
                self._parts[7].set_color(constants.RED)

        # is hurt timer
        if self._is_hurt_timer > 0:
            self._is_hurt_timer -= 1

            if self._is_hurt_timer % 2 == 0:
                if self._flash_color == constants.AQUA:
                    self._flash_color = constants.PINK
                else:
                    self._flash_color = constants.AQUA
                # set ship flashing color
                for part in self._parts[:-1]:
                    part.set_color(self._flash_color)
        else:
            if self.get_is_hurt() == True:
                self._is_hurt = False
                # reset ship color
                for idx, part in enumerate(self._parts):
                    part.set_color(
                        constants.SHIP_COLORS[constants.SHIP_LAYOUT[idx][3]])

    def control_ship(self, velocity):
        # set our velocity
        self.set_velocity(velocity)
        # set velocity of all ship parts
        for part in self._parts:
            part.set_velocity(velocity)

    def _prepare_ship(self):
        """
        Creates the ship by making a list of ship parts relative to the x,y starting position
        self._parts
        """
        # set origin position
        x = int(constants.MAX_X * 0.5)
        y = int(constants.MAX_Y - constants.CELL_SIZE * 8)

        # generate parts list based on layout
        self._parts = self._generate_structure(
            Point(x, y), Point(0, 0), constants.SHIP_LAYOUT, constants.SHIP_COLORS)
