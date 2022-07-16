import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Ship(Actor):
    """
    A spaceship

    The responsibility of Ship is to move itself.

    Attributes:
        parts (list): keeps track of ships structure of parts
        is_hurt (bool): true for given amount of time after ship hits an enemy
        is_hurt_timer (int): used by is_hurt
        flash_color (Color): used to toggle a flashing color when is_hurt is True

        is_dead (bool): set when player dies and parts are no longer displayed
        
    """

    def __init__(self):
        super().__init__() 
        self._parts = []
        # prepare ship structure and save actors to parts list
        self._prepare_ship()
        # default values
        self._is_hurt = False
        self._is_hurt_timer = 0
        self._flash_color = constants.AQUA
        self._is_dead = False
        # gun stuff
        self._gun_type = "single" # ex: single, rapid, shotgun
        self._upgrade_shots = 0
        

    def get_is_hurt(self):
        return self._is_hurt

    def get_is_dead(self):
        return self._is_dead

    def set_gun_type(self,type):
        self._gun_type = type

    def get_gun_type(self):
        return self._gun_type

    def set_upgrade_shots(self, shots):
        self._upgrade_shots = shots

    def get_upgrade_shots(self):
        return self._upgrade_shots

    def set_is_dead(self, is_dead):
        self._is_dead = is_dead
        self._is_hurt = False

    def set_is_hurt(self, is_hurt):
        self._is_hurt = is_hurt
        # set the flash timer if ship got hurt
        if is_hurt == True:
            self._is_hurt_timer = 10

    def get_parts(self):
        return self._parts

    def remove_parts(self):
        self._parts.clear()

    def reset_ship(self):
        # resets the ship to display again
        self._is_hurt = False
        self._is_dead = False
        self._prepare_ship()

    def move_next(self):
        """(OVERRIDE) Applies player movement by updating the position of the ship and it's parts """

        # make sure the body exists
        if len(self._parts) > 0:

            # move all parts
            for part in self._parts:
                # set velocity of all ship parts
                part.set_velocity(self._velocity)
                # apply base move_next() method of Actor class
                part.move_next()
            
            # HANDLE ANIMATIONS - - - - - - - 
            # animate thrust (seventh part)
            if self._parts[7].get_text() == '*':
                # toggle symbols and colors
                self._parts[7].set_text("'")
                self._parts[7].set_color(constants.ORANGE)
            else:
                self._parts[7].set_text('*')
                self._parts[7].set_color(constants.RED)

            # is hurt timer is on
            if self._is_hurt_timer > 0:
                # increment it
                self._is_hurt_timer -= 1
                # every two frames
                if self._is_hurt_timer % 2 == 0:
                    # toggle the flash color
                    if self._flash_color == constants.AQUA:
                        self._flash_color = constants.PINK
                    else:
                        self._flash_color = constants.AQUA
                    # apply the flash color to the ship parts (besides thrust)
                    for part in self._parts[:-1]:
                        part.set_color(self._flash_color)
            else:
                # if the ship timer is equal to zero
                if self.get_is_hurt() == True:
                    # reset is_hurt
                    self._is_hurt = False
                    # reset ship color
                    for idx, part in enumerate(self._parts):
                        part.set_color(constants.SHIP_COLORS[constants.SHIP_LAYOUT[idx][3]])
            # - - - - - - - - - - - - - - -


    def control_ship(self, velocity):
        # set our velocity
        self.set_velocity(velocity)

    def _prepare_ship(self):
        """
        Creates the ship by making a list of ship parts relative to the x,y starting position.
        Saves the list of actors in self._parts.
        """
        # set origin position
        x = int(constants.MAX_X * 0.5)
        y = int(constants.MAX_Y - constants.CELL_SIZE * 8)
        # generate parts list based on layout
        self._parts = self._generate_structure(Point(x, y), Point(0, 0), constants.SHIP_LAYOUT, constants.SHIP_COLORS)
