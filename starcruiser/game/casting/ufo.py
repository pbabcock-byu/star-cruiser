
import constants
import random
from game.casting.actor import Actor
from game.shared.point import Point
from game.casting.explosion import Explosion
from game.casting.spark import Spark
from game.casting.laser import Laser

class Ufo(Actor):
    """
    Ufo are objects that fly back and forth in space and shoot lasers at the player ship

    Attributes:
        health (int): how many shots it takes to destroy this asteroid
        damage (int): how much damage the asteroid does to the player
        points (int): how many points the asteroid is worth if it's destroyed

        hit_sound ("string"): reference to sound file to play when this asteroid gets shot by a laser
        exp_sound ("string"): reference to sound file to play when this asteroid gets blown up

        parts (list): list of individual parts of a large structured asteroid
    """

    def __init__(self, cast, audio_service):
        super().__init__()
        self._cast = cast
        # enemy attributes
        self._health = 3
        self._damage = 2
        self._points = 8
        # for audio
        self._hit_sound = "ast-hit"
        self._exp_sound = "ufo-exp"
        # prepare ufo body structure
        self.set_text('H')
        self.set_color(constants.YELLOW)
        # create empty parts list
        self._parts = [self]
        # control ufo shooting
        self._shoot_wait = 0
        # allow ufo to play a flying loop sound
        self._audio_service = audio_service

    def get_parts(self):
        return self._parts

    def get_hit_sound(self):
        return self._hit_sound

    def get_exp_sound(self):
        return self._exp_sound       

    def get_health(self):
        return self._health

    def get_damage(self):
        return self._damage

    def set_up_ufo(self):
        # prepare ufo body at correct position
        self._prepare_structured_ufo_body()

    def remove_health(self, amount):
        """ Removes a certain amount of health when hit by a laser or by the player ship
        Args:
            amount (int): the amount of damage that is occuring
        """
        # apply the damage
        self._health -= amount

        # check to see if ufo is out of health
        if self._health <= 0:

            # if the amount is 1000 then we hit the player ship, so don't apply score
            if (amount != 1000):
                # otherwise apply this asteroids points worth to score
                scoreboard = self._cast.get_first_actor("scores")
                scoreboard.add_points(self._points)

            # Do special effects ( explosion and sparks )
            for part in self._parts:
                # create an explosion at each parts position
                explosion = Explosion(self._cast)
                explosion.set_text(".")
                explosion.set_color(constants.WHITE)
                explosion.set_velocity(
                    Point(random.randint(-1, 1), random.randint(0, 2)))
                explosion.set_position(part.get_position())
                explosion.set_animate_speed(0.3 + random.random()*0.7)
                # add explosion to "explosions" cast group
                self._cast.add_actor("explosions", explosion)

                for i in range(0, 3):
                    # create three sparks at each parts location
                    spark = Spark(self._cast)
                    spark.set_text(".")
                    spark.set_color(constants.WHITE)
                    spark.set_speed(random.choice([5, 8, 9, 10, ]))
                    spark.set_direction(random.random()*360)
                    spark.set_position(part.get_position())
                    # add explosion to "explosions" cast group
                    self._cast.add_actor("sparks", spark)

            # remove ourselves
            self._cast.remove_actor("ufos", self)

            # return whether we blew up so handle_collisions can play appropriate sound
            return True
        else:
            return False


    def _prepare_structured_ufo_body(self):
        """
        Creates the structure of actors to form a ufo ship using a layout.
        Stores each Actor reference in self._parts list.
        """
        # set origin position for layout
        origin = self.get_position()
        # get layout information to draw ufo
        ufo_layout = constants.UFO_LAYOUT
        ufo_colors = constants.UFO_COLORS
        # generate structure from layout and store in parts list
        self._parts = self._generate_structure(origin, self._velocity, ufo_layout, ufo_colors)
        # add self to front of parts list as the center piece of the structure
        self._parts.append(self)#insert(0, self)


    def move_next(self):
        """ (OVERRIDE) Moves the actor to its next position according to its velocity. 
        Will wrap the x position from one side of the screen to the other when it reaches the given maximum x.
        Args:
            max_x (int): The maximum x value.
        """

        # check if ufo is off screen
        if self._position.get_y() >= constants.MAX_Y:
            # delete it
            self._cast.remove_actor("ufos", self)
        else:

            # make sure flying ufo sound loop is playing
            self._audio_service.set_loop_sound("ufo-fly")

            # randomly reverse x movement to move side to side
            if random.random() > 0.93:
                self._velocity._x = -self._velocity._x

            # randomly move downward towards the player
            if random.random() > 0.8:
                self._velocity._y = constants.CELL_SIZE
            else:
                self._velocity._y = 0

            # apply movement to ufo (all parts)
            for part in self._parts:
                # wrap x
                x = (part._position.get_x() + self._velocity.get_x()) % constants.MAX_X
                y = (part._position.get_y() + self._velocity.get_y())
                # apply movement
                part._position = Point(x, y)

            # handle shooting
            if self._shoot_wait > 0:
                # increment the shoot timer
                self._shoot_wait -= 1
            else:
                # if the timer is zero
                ship = self._cast.get_first_actor("ships")
                # check to see if the ship is below our x position (within 3cells away)
                if abs(ship.get_position().get_x() - self._position._x) < 3 * constants.CELL_SIZE:
                    if self._shoot_wait == 0:
                        # apply attributes to a new instance of laser
                        laser = Laser(self._cast)
                        laser.set_position(Point(self._position._x,self._position._y+constants.CELL_SIZE))
                        laser.set_velocity(Point(0,constants.CELL_SIZE))
                        laser.set_text("|")
                        laser.set_color(constants.RED)
                        laser.set_damage(3)
                        # add laser to the "lasers" cast
                        self._cast.add_actor("lasers", laser)
                        # wait before shooting again
                        self._shoot_wait = 2
                        # play ufo laser sound
                        self._audio_service.play_sound("ufo-laser")



                

