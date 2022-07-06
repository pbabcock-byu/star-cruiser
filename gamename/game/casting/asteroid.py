
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

        # for building out larger asteroid structures
        self._parts = [self]

    def get_parts(self):
        return self._parts

    def get_name(self):
        """Gets the Asteriod's size
        Returns:
            string: The type.
        """
        return self._name

    def get_health(self):
        return self._health

    def remove_health(self, amount):
        self._health -= amount

        # check to see if asteroid is out of health
        if self._health <= 0:
            # if yes
            # apply points to score
            scoreboard = self._cast.get_first_actor("scores")
            scoreboard.add_points(self._points)

            # create special effects ( explosion and sparks )
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

            # if we are a giant asteroid, generate some huge asteroids when we are broken:
            if self.get_name() == "GIANT":
                for i in range(0, 2):
                    this = self._create_asteroid_when_destroyed(4)
                    self._cast.add_actor("asteroids", this)

            # if we are a huge asteroid, generate some large asteroids when we are broken:
            if self.get_name() == "HUGE":
                for i in range(0, 3):
                    this = self._create_asteroid_when_destroyed(2)
                    self._cast.add_actor("asteroids", this)

            # remove ourselves
            self._cast.remove_actor("asteroids", self)

    def set_up_type(self, type):
        """Updates Asteriod's size.
        Args:
            type (string): The Asteriod's size.
        """
        asteroid_type_info = constants.ASTEROID_TYPES_LIST[type]

        self._name = asteroid_type_info["name"]
        self._text = asteroid_type_info["text"]
        self._health = asteroid_type_info["health"]
        self._damage = asteroid_type_info["damage"]
        self._points = asteroid_type_info["points"]

        # update speed, movement, and structure based on name
        # move speed
        if self._name == "SML":
            self._move_wait = random.choice([2, 3, 4])

        if self._name == "MED":
            self._move_wait = random.choice([3, 4])

        if self._name == "LRG":
            self._move_wait = 4
        # movement
        if self._name == "SML-xmove":
            # cause us to move horizontally
            self._velocity = Point(random.choice(
                [-constants.CELL_SIZE, constants.CELL_SIZE]), constants.CELL_SIZE)
        # structure
        if self._name in ["HUGE", "GIANT"]:
            # this astroid is a structure of multiple actors
            self._move_wait = 5
            self._prepare_structured_asteroid_body()

    def _prepare_structured_asteroid_body(self):
        """
        Creates the structure of actors to form a huge asteroid
        self._parts
        """
        # set origin position
        origin = self.get_position()
        # set up layout information
        if self._name == "HUGE":
            asteroid_layout = constants.HUGE_ASTEROID_LAYOUT
        if self._name == "GIANT":
            asteroid_layout = constants.GIANT_ASTEROID_LAYOUT
        # set up layout color info
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
        asteroid = Asteroid(self._cast)
        asteroid.set_color(self._color)
        asteroid.set_position(position)
        asteroid.set_velocity(velocity)
        asteroid.set_up_type(asteroidtype)
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
