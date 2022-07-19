
import constants
import random
from game.casting.actor import Actor
from game.shared.point import Point
from game.casting.explosion import Explosion
from game.casting.spark import Spark


class Asteroid(Actor):
    """
    Asteriod are objects that will be flying in space
    different size asteriod will do diffent amounts of damage if they hit the space ship
    Also the bigger an the more points the player will get for shooting it

    Attributes:
        name (string): "SML", "MED", "LRG", "SML-xmove", "GIANT", "HUGE", used to look up asteroid attributes in the ASTEROID_TYPES_LIST (constants)
        text (string): used to display the asteroid, ex: medium asteroid = "*" large asteroid = "@"
        health (int): how many shots it takes to destroy this asteroid
        damage (int): how much damage the asteroid does to the player
        points (int): how many points the asteroid is worth if it's destroyed

        move_wait (int): waits this many frames between moving (used to make asteroids move slower)
        move_timer (int): ^ used by move wait

        hit_sound ("string"): reference to sound file to play when this asteroid gets shot by a laser
        exp_sound ("string"): reference to sound file to play when this asteroid gets blown up

        parts (list): list of individual parts of a large structured asteroid

    """

    def __init__(self, cast):
        super().__init__()
        self._cast = cast

        # these are set in the set_up_type() method
        self._name = "SML"
        self._text = "."
        self._health = 1
        self._damage = 1
        self._points = 1

        # for movement
        self._move_wait = 4
        self._move_timer = 0

        # for audio
        self._hit_sound = "ast-hit"
        self._exp_sound = "ast-hit-sml"

        # for building out larger asteroid structures
        self._parts = [self]

    def get_parts(self):
        return self._parts

    def get_name(self):
        return self._name

    def get_hit_sound(self):
        return self._hit_sound

    def get_exp_sound(self):
        return self._exp_sound       

    def get_health(self):
        return self._health

    def get_damage(self):
        return self._damage

    def remove_health(self, amount):
        """ Removes a certain amount of health when hit by a laser or by the player ship
        Args:
            amount (int): the amount of damage that is occuring
        """
        # apply the damage
        self._health -= amount

        # check to see if asteroid is out of health
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

            # if this is a giant asteroid, generate some HUGE asteroids when we are broken:
            if self.get_name() == "GIANT":
                for i in range(0, 2):
                    this = self._create_asteroid_when_destroyed(4)
                    self._cast.add_actor("asteroids", this)

            # if this is a huge asteroid, generate some LARGE asteroids when we are broken:
            if self.get_name() == "HUGE":
                for i in range(0, 3):
                    this = self._create_asteroid_when_destroyed(2)
                    self._cast.add_actor("asteroids", this)

            # remove ourselves
            self._cast.remove_actor("asteroids", self)

            # return whether we blew up so handle_collisions can play appropriate sound
            return True
        else:
            return False

    def set_up_type(self, type):
        """Updates Asteriod's attributes based on it's type
        Args:
            type (string): The Asteriod's size.
        """
        # get object with appropriate info from list in constants
        asteroid_type_info = constants.ASTEROID_TYPES_LIST[type]
        # update our member variables with that objects values
        self._name = asteroid_type_info["name"]
        self._text = asteroid_type_info["text"]
        self._health = asteroid_type_info["health"]
        self._damage = asteroid_type_info["damage"]
        self._points = asteroid_type_info["points"]
        self._move_wait = asteroid_type_info["movewait"]() # called as function to get random value
        self.set_color(asteroid_type_info["color"])
        self._hit_sound = asteroid_type_info["hit-sound"]
        self._exp_sound = asteroid_type_info["destroy-snd"]

        # apply special horizontal movement to "SML-xmove" asteroids
        if self._name == "SML-xmove":
            self._velocity = Point(random.choice([-constants.CELL_SIZE, constants.CELL_SIZE]), constants.CELL_SIZE)

        # generate structures of parts for "HUGE" and "GIANT" asteroids
        if self._name in ["HUGE", "GIANT"]:
            # this astroid is a structure of multiple actors
            self._prepare_structured_asteroid_body()

    def _prepare_structured_asteroid_body(self):
        """
        Creates the structure of actors to form a huge asteroid using a layout.
        Stores each Actor reference in self._parts list.
        """
        # set origin position for layout
        origin = self.get_position()
        # get layout information based on type/name
        if self._name == "HUGE":
            asteroid_layout = constants.HUGE_ASTEROID_LAYOUT
        if self._name == "GIANT":
            asteroid_layout = constants.GIANT_ASTEROID_LAYOUT
        # get layout color info
        asteroid_colors = [self.get_color()]

        # generate structure from layout and store in parts list
        self._parts = self._generate_structure(origin, self._velocity, asteroid_layout, asteroid_colors)
        # add self to parts list as the center piece of the structure
        self._parts.append(self)

    def _create_asteroid_when_destroyed(self, asteroidtype):
        """
        Creates a smaller asteroid at this asteroids position (slightly randomized) when it gets blown up.
        """
        # find a slightly randomized position
        x = self._position.get_x() + random.randint(-1, 1) * constants.CELL_SIZE
        y = self._position.get_y() + random.randint(-1, 0) * constants.CELL_SIZE
        position = Point(x, y)
        # make it move randomly horizontally
        velocity = Point(random.randint(-1, 1) *constants.CELL_SIZE, 1 * constants.CELL_SIZE)
        asteroid = Asteroid(self._cast)
        asteroid.set_color(self._color)
        asteroid.set_position(position)
        asteroid.set_velocity(velocity)
        # call it's set up type so it's attributes get applied
        asteroid.set_up_type(asteroidtype)
        # returns it so the calling method can add it to the cast "asteriods" group
        return asteroid

    def move_next(self):
        """ (OVERRIDE) Moves the actor to its next position according to its velocity. 
        Will wrap the x position from one side of the screen to the other when it reaches the given maximum x.
        Args:
            max_x (int): The maximum x value.
        """
        # if the move wait timer is up
        if self._move_timer == 0:
            # reset move timer
            self._move_timer = self._move_wait

            # check if asteroid is off screen
            if self._position.get_y() >= constants.MAX_Y - constants.CELL_SIZE * 2:
                # delete it
                self._cast.remove_actor("asteroids", self)
            else:
                # otherwise apply movement to asteroid (all parts)
                for part in self._parts:
                    # wrap x
                    x = (part._position.get_x() + self._velocity.get_x()) % constants.MAX_X
                    y = (part._position.get_y() + self._velocity.get_y())
                    # apply movement
                    part._position = Point(x, y)
        else:
            # waiting a few frames before moving again
            self._move_timer -= 1
