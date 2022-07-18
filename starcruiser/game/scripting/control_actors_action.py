import constants
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.actor import Actor
from game.casting.laser import Laser
# need this module to play sounds
from playsound import playsound


class ControlActorsAction(Action):
    """
    An input action that controls the ship and fires lasers.

    The responsibility of ControlActorsAction is to get the direction and move the ship back and forth and fire lasers.

    Attributes:
        _keyboard_service (KeyboardService): An instance of KeyboardService.
    """

    def __init__(self, keyboard_service, audio_service):
        """Constructs a new ControlActorsAction using the specified KeyboardService.

        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            audio_servie (AudioService): An instance of AudioService.
        """
        self._keyboard_service = keyboard_service
        self._audio_service = audio_service
        # key press only vs key hold and laser timer
        self._key_fire = False
        self._key_fire_timer = 0
        
        # stores player movement direction
        self._player_direction = Point(0, 0)

    def _handle_player_movement(self, cast):
        """Executes the control actors action to control player movement
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # reset movement velocity
        self._player_direction = Point(0, 0)

        # left key
        if self._keyboard_service.is_key_down('left'):
            self._player_direction = Point(-constants.CELL_SIZE, 0)

        # right key
        if self._keyboard_service.is_key_down('right'):
            self._player_direction = Point(constants.CELL_SIZE, 0)

        # apply velocity to player
        ship = cast.get_first_actor("ships")
        ship.control_ship(self._player_direction)

    def _handle_player_fire_weapon(self, cast):
        """Executes the control actors action to handle player firing weapon
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # get reference to ship
        ship = cast.get_first_actor("ships")

        # make sure ship is not dead or in hurt mode
        if ship.get_is_dead() == False and ship.get_is_hurt() == False:
            # if player presses the space bar
            if self._keyboard_service.is_key_down('space') and self._key_fire == False:

                # play laser sound
                self._audio_service.play_sound("laser")

                # set key fire so only one bullet is fired at a time
                self._key_fire = True

                # set timer to control how rapidly player can fire
                if ship.get_gun_type() == "single":
                    self._key_fire_timer = 6

                # if we are any other gun type, limit the number of shots
                if ship.get_gun_type() != "single":
                    # get the wait time for this gun type from constants
                    self._key_fire_timer = constants.GUN_UPGRADE_ATTRIBUTES[ship.get_gun_type()][1]
                    # check if we've reached max shots
                    if ship.get_upgrade_shots() < constants.GUN_UPGRADE_ATTRIBUTES[ship.get_gun_type()][0]:
                        ship.set_upgrade_shots(ship.get_upgrade_shots() + 1)
                    else:
                        # reset to zero
                        ship.set_upgrade_shots(0)
                        ship.set_gun_type("single")



                # get the position of the front of the ship (part zero)
                ship_parts = ship.get_parts()
                ship_position = ship_parts[0].get_position()

                # get a location point one cell above the front of the ship
                position = Point(ship_position.get_x(),
                                 ship_position.get_y() - 1 * constants.CELL_SIZE)

                # set attributes of laser (default green)
                color = constants.GREEN
                text = "^"
                # set rapid fire laser color to red
                if ship.get_gun_type() == "rapid":
                    color = constants.RED
                    text = "|"

                if ship.get_gun_type() == "shotgun":
                    color = constants.PURPLE
                    text = "!"

                # velocity to move upward
                velocity = Point(0, -constants.CELL_SIZE)
                
                def make_laser():
                    # apply attributes to a new instance of laser
                    laser = Laser(cast)
                    laser.set_position(position)
                    laser.set_velocity(velocity)
                    laser.set_text(text)
                    laser.set_color(color)
                    return laser

                laser = make_laser()
                # add laser to the "lasers" cast
                cast.add_actor("lasers", laser)

                # if we are the shotgun type make two additional lasers
                if ship.get_gun_type() == "shotgun":
                    # increase the original lasers damage
                    laser.set_damage(2)
                    # get a location point one cell to the left
                    position = Point(ship_position.get_x() - 1 * constants.CELL_SIZE,
                                    ship_position.get_y()) 
                    #make another laser
                    laser = make_laser()
                    laser.set_damage(2)
                    # add laser to the "lasers" cast
                    cast.add_actor("lasers", laser)

                     # get a location point one cell to the right
                    position = Point(ship_position.get_x() + 1 * constants.CELL_SIZE,
                                    ship_position.get_y())   
                    #make another laser
                    laser = make_laser()   
                    laser.set_damage(2)
                    # add laser to the "lasers" cast
                    cast.add_actor("lasers", laser)                        

        # handle rapid fire wait timer and key hold
        if self._key_fire == True:

            # if self._keyboard_service.is_key_up('space'):  #(uncomment to make it so you have to press each time)
            if self._key_fire_timer <= 0:
                # if timer is up reset key fire so we can shoot again
                self._key_fire = False

            # increment timer if greater than zero
            if self._key_fire_timer > 0:
                self._key_fire_timer -= 1

    def execute(self, cast, script):
        """Executes the control actors action.
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        # handle player movement
        self._handle_player_movement(cast)
        # handle player fire weapon
        self._handle_player_fire_weapon(cast)
