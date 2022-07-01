import constants
import random
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.explosion import Explosion


class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.

    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self, keyboard_service):
        """Constructs a new HandleCollisionsAction."""

        self._keyboard_service = keyboard_service

        self._is_game_over = False
        self._who_won = ""

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:

            # self._handle_snakes_collision(cast)
            self._handle_laser_enemy_collision(cast, ["asteroids"])
            self._handle_player_enemy_collision(cast, ["asteroids"])

            self._handle_game_over(cast)
        else:
            if self._keyboard_service.is_key_down('enter'):
                # reset game over variable
                self._is_game_over = False
                # remove game over message
                cast.remove_actor("messages", cast.get_first_actor("messages"))

                # reset snake bodies
                ship = cast.get_first_actor("ships")
                ship.reset_ship()

    def _handle_laser_enemy_collision(self, cast, groups):
        """Destroys enemies when laser hits them

        Args:
            cast (Cast): The cast of Actors in the game.
        """
        lasers = cast.get_actors("lasers")
        # for every laser
        for laser in lasers:
            # loop through every group in the groups list
            for group in groups:
                # loop through every enemy in this group
                for enemy in cast.get_actors(group):
                    # for every segment in this other snake
                    laser_position = laser.get_position()
                    laser_last_position = Point(laser.get_position().get_x(
                    ), laser.get_position().get_y()+constants.CELL_SIZE)
                    if laser_position.equals(enemy.get_position()) or laser_last_position.equals(enemy.get_position()):
                        # create an explosion at the lasers position
                        explosion = Explosion(cast)
                        explosion.set_text(".")
                        explosion.set_color(constants.WHITE)
                        explosion.set_velocity(Point(0, 1))
                        explosion.set_position(laser.get_position())
                        # add explosion to "explosions" cast group
                        cast.add_actor("explosions", explosion)

                        # delete the laser and enemy
                        cast.remove_actor("lasers", laser)
                        cast.remove_actor(group, enemy)
                        break

    def _handle_player_enemy_collision(self, cast, groups):
        """Sets the game over flag if a snake head collides with a segment from another snake.

        Args:
            cast (Cast): The cast of Actors in the game.
        """
        ship = cast.get_first_actor("ships")

        parts = ship.get_parts()
        # loop through every part
        for part in parts:
            for group in groups:
                # loop through every enemy in this group
                for enemy in cast.get_actors(group):
                    if part.get_position().equals(enemy.get_position()):
                        # if head collides with any, game over
                        self._is_game_over = True

    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.

        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text(
                f"Game Over!\n {self._who_won.capitalize()} player won the game.\n\n Press 'Y' to play again! ")
            message.set_position(position)
            cast.add_actor("messages", message)

            ship = cast.get_first_actor("ships")
            parts = ship.get_parts()
            # loop through every part
            for part in parts:
                # create an explosion at the parts position
                explosion = Explosion(cast)
                explosion.set_text(".")
                explosion.set_color(constants.WHITE)
                explosion.set_velocity(Point(0, 1))
                explosion.set_position(part.get_position())
                explosion.set_animate_speed(0.1 + random.random()*0.8)
                # add explosion to "explosions" cast group
                cast.add_actor("explosions", explosion)

            # delete the ship parts
            ship.remove_parts()
            # delete all enemies
            cast.remove_actors("asteroids")
