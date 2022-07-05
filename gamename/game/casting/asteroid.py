
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
    Also the bigger an the less points the player will get for shooting it

    Attributes:
        _type (String): "LRG" or "MED" or "SML" or "HUGE"
    """

    def __init__(self, cast, type):
        super().__init__()
        self._cast = cast
        # default attributes
        self._type = type
        self._move_wait = 4
        self._move_timer = 0
        self._parts = [self]
        self._health = constants.ASTEROID_HEALTH_LIST[self._type]

    def get_parts(self):
        return self._parts

    def get_type(self):
        """Gets the Asteriod's size
        Returns:
            string: The type.
        """
        return self._type

    def get_health(self):
        return self._health

    def remove_health(self, amount):
        self._health -= amount
        # check to see if we are out of health
        if self._health <= 0:
            for part in self._parts:
                # create an explosion at the parts position
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
                    # create some sparks at our location
                    spark = Spark(self._cast)
                    spark.set_text(".")
                    spark.set_color(constants.WHITE)
                    spark.set_speed(random.choice([5, 8, 9, 10, ]))
                    spark.set_direction(random.random()*360)
                    spark.set_position(part.get_position())
                    # add explosion to "explosions" cast group
                    self._cast.add_actor("sparks", spark)

            # if we are a giant asteroid, generate some huge ones when we are broken:
            if self.get_type() == "GIANT":
                for i in range(0, 2):
                    this = self._create_asteroid_when_destroyed(4)
                    self._cast.add_actor("asteroids", this)

            # if we are a giant asteroid, generate some huge ones when we are broken:
            if self.get_type() == "HUGE":
                for i in range(0, 3):
                    this = self._create_asteroid_when_destroyed(2)
                    self._cast.add_actor("asteroids", this)

            # remove ourselves
            self._cast.remove_actor("asteroids", self)

    def set_up_parts(self):
        """Updates Asteriod's size.
        Args:
            type (string): The Asteriod's size.
        """
        # update attributes based on type
        # health
        self._health = constants.ASTEROID_HEALTH_LIST[self._type]
        # move speed
        if self._type == "SML":
            self._move_wait = random.choice([2, 3, 4])

        if self._type == "MED":
            self._move_wait = random.choice([3, 4])

        if self._type == "LRG":
            self._move_wait = 4

        if self._type in ["HUGE", "GIANT"]:
            # this astroid is structure of multiple actors
            self._move_wait = 5
            self._prepare_structured_asteroid_body()

    def _prepare_structured_asteroid_body(self):
        """
        Creates the structure of actors to form a huge asteroid
        self._parts
        """
        # set origin position
        origin = self.get_position()

        # set layout information
        if self._type == "HUGE":
            asteroid_layout = [["@", 0, 0, 0], ["@", 1, 0, 0], ["@", -1, 0, 0], ["@", 0, 1, 0], ["@", 0, -1, 0],
                               ["@", -1, -1, 0], ["@", 1, -1, 0],
                               ["@", -1, 1, 0], ["@", 1, 1, 0],
                               ["@", -2, 0, 0], ["@", 0, -2, 0], ["@", 2, 0, 0], ["@", 0, 2, 0]]
        if self._type == "GIANT":
            asteroid_layout = [["@", 0, 0, 0], ["@", 1, 0, 0], ["@", -1, 0, 0], ["@", 0, 1, 0], ["@", 0, -1, 0],
                               ["@", -1, -1, 0], ["@", 1, -1, 0],
                               ["@", -1, 1, 0], ["@", 1, 1, 0],
                               ["@", -2, 0, 0], ["@", 0, -2, 0],
                               ["@", 2, 0, 0], ["@", 0, 2, 0],

                               ["@", -2, -2, 0], ["@", 2, -2, 0],
                               ["@", -2, 2, 0], ["@", 2, 2, 0],

                               ["@", -2, -1, 0], ["@", -2, 1, 0],
                               ["@", 2, 1, 0], ["@", 2, -1, 0],
                               ["@", -1, 2, 0], ["@", 1, 2, 0],
                               ["@", 1, -2, 0], ["@", -1, -2, 0],

                               ["@", -3, -1, 0], ["@", -3, 1, 0],
                               ["@", 3, 1, 0], ["@", 3, -1, 0],
                               ["@", -1, 3, 0], ["@", 1, 3, 0],
                               ["@", 1, -3, 0], ["@", -1, -3, 0],
                               ["@", 0, 3, 0], ["@", 0, -3, 0],
                               ["@", -3, 0, 0], ["@", 3, 0, 0]
                               ]

        asteroid_colors = [constants.BROWN]

        # generate parts list from layout
        self._parts = self._generate_structure(
            origin, self._velocity, asteroid_layout, asteroid_colors)
        # add self to parts list
        self._parts.append(self)

    def _create_asteroid_when_destroyed(self, asteroidtype):
        """
        Creates the structure of actors to form a huge asteroid
        self._parts
        """
        x = self._position.get_x() + random.randint(-1, 1) * constants.CELL_SIZE
        y = self._position.get_y() + random.randint(-1, 0) * constants.CELL_SIZE
        position = Point(x, y)

        velocity = Point(random.randint(-1, 1) *
                         constants.CELL_SIZE, 1 * constants.CELL_SIZE)
        type = constants.ASTEROID_TYPES[asteroidtype]
        asteroid = Asteroid(self._cast, type[0])
        asteroid.set_text(type[1])
        asteroid.set_color(constants.BROWN)
        asteroid.set_position(position)
        asteroid.set_velocity(velocity)
        asteroid.set_up_parts()
        # returns it so we can add it to the cast "asteriods" group
        return asteroid

    def move_next(self):
        """ (OVERRIDE) Moves the actor to its next position according to its velocity. Will wrap the position 
        from one side of the screen to the other when it reaches the given maximum (X ONLY FOR LASER).

        Args:
            max_x (int): The maximum x value.
        """
        if self._move_timer == 0:
            # reset move timer
            self._move_timer = self._move_wait

            # if asteroid is off screen
            if self._position.get_y() >= constants.MAX_Y + constants.CELL_SIZE * 5:
                # delete it
                self._cast.remove_actor("asteroids", self)
            else:
                # apply movement to all parts
                for part in self._parts:
                    x = (part._position.get_x() +
                         self._velocity.get_x()) % constants.MAX_X
                    y = (part._position.get_y() + self._velocity.get_y())
                    # move part
                    part._position = Point(x, y)

        else:
            # waiting a few frames before moving again
            self._move_timer -= 1
