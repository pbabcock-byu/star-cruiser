import constants
import random
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.explosion import Explosion
from game.casting.spark import Spark
# need this module to play sounds
from playsound import playsound


class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.

    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self, keyboard_service, handle_menu_system, audio_service):
        """Constructs a new HandleCollisionsAction."""

        self._keyboard_service = keyboard_service
        self._handle_menu_system = handle_menu_system
        self._audio_service = audio_service

        self._is_game_over = False
        self._game_over_timer = 0
        self._who_won = ""

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:

            self._handle_laser_enemy_collision(cast, ["asteroids"])
            self._handle_player_enemy_collision(cast, ["asteroids"])
            self._handle_player_upgrade_collision(cast)

            self._handle_game_over(cast)
        else:
            if self._game_over_timer < 75:
                self._game_over_timer += 1
            else:
                # run the following code once
                if self._game_over_timer < 110:
                    self._game_over_timer = 110
                    self._handle_menu_system.set_menu_state("highscore")
                    # remove game over message
                    cast.remove_actor(
                        "messages", cast.get_first_actor("messages"))

                # #reset game over variable
                # self._is_game_over = False
                # # reset snake bodies
                # ship = cast.get_first_actor("ships")
                # ship.reset_ship()

    def _handle_laser_enemy_collision(self, cast, groups):
        """Destroys enemies when laser hits them

        Args:
            cast (Cast): The cast of Actors in the game.
        """
        lasers = cast.get_actors("lasers")
        hit = False
        destroyed = False
        # for every laser
        for laser in lasers:
            # loop through every group in the groups list
            for group in groups:
                if hit:
                    break
                # loop through every enemy in this group
                for enemy in cast.get_actors(group):
                    if hit:
                        break
                    # loop through every enemy in this group
                    for enemypart in enemy._parts:
                        # get laser positions
                        laser_position = laser.get_position()
                        laser_last_position = Point(laser.get_position().get_x(
                        ), laser.get_position().get_y()+constants.CELL_SIZE)

                        if laser_position.equals(enemypart.get_position()) or laser_last_position.equals(enemypart.get_position()):
                            # create an explosion at the lasers position
                            explosion = Explosion(cast)
                            explosion.set_text(".")
                            explosion.set_color(constants.WHITE)
                            explosion.set_velocity(Point(0, 1))
                            explosion.set_position(laser_last_position)
                            # add explosion to "explosions" cast group
                            cast.add_actor("explosions", explosion)

                            # apply damage from laser to enemy health
                            destroyed = enemy.remove_health(laser.get_damage())
                            if destroyed:
                                # play enemy destroy sound
                                self._audio_service.play_sound(enemy.get_exp_sound())                        
                            else:
                                # play enemy hit sound
                                self._audio_service.play_sound(enemy.get_hit_sound())
                            # delete the laser
                            cast.remove_actor("lasers", laser)
                            # break all loops
                            hit = True
                            break

    def _handle_player_enemy_collision(self, cast, groups):
        """Sets the game over flag if a snake head collides with a segment from another snake.

        Args:
            cast (Cast): The cast of Actors in the game.
        """
        ship = cast.get_first_actor("ships")

        # make sure we are not on our hurt timer
        if ship.get_is_hurt() == False:
            # then, check for collisions
            parts = ship.get_parts()
            # loop through every part
            hit = False
            for part in parts:
                if hit:
                    break
                for group in groups:
                    if hit:
                        break
                    # loop through every enemy in this group
                    for enemy in cast.get_actors(group):
                        if hit:
                            break
                        for enemypart in enemy._parts:
                            if part.get_position().equals(enemypart.get_position()):
                                # set hit to true so we can break the loop and only apply one hit at a time
                                hit = True
                                # if any player part collides with any enemy part
                                # get reference to shields instance
                                shields = cast.get_first_actor("shields")

                                # ( CODE FOR APPLYING DAMAGE TO SHIELDS HERE )
                                shields.add_points(- enemy.get_damage())

                                # create sparks that bounce off player ship
                                self._create_sparks(
                                    cast, 20, part.get_position(), 5, 13, 270, 40)
                                # if player is moving sideways
                                if ship.get_velocity().get_x() > 0:
                                    self._create_sparks(
                                        cast, 20, part.get_position(), 10, 23, 350, 40)
                                if ship.get_velocity().get_x() < 0:
                                    self._create_sparks(
                                        cast, 20, part.get_position(), 10, 23, 190, 40)

                                # remove all the enemies health
                                enemy.remove_health(1000)

                                # if we have less than 0 shields now
                                if shields.get_points() < 0:
                                    # explode player, game over
                                    self._is_game_over = True
                                    ship.set_is_dead(True)
                                else:
                                    # set ship is hurt to true
                                    ship.set_is_hurt(True)

                                    # play ship hit sound
                                    self._audio_service.play_sound("ship-hit")

                                    if shields.get_points() <= 4:
                                        # play low shields warning sound
                                        self._audio_service.play_sound("low-shields")

                                # break the current loop
                                break

    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.

        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:

            # tell the menu system it's game over
            self._handle_menu_system.set_game_over(True)

            # stop game music
            self._audio_service.set_music("none")
            # play game over sound
            self._audio_service.play_sound("game-over")
            # play ship explode 
            self._audio_service.play_sound("ship-exp")


            # get center screen position
            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y * 0.5)
            position = Point(x, y)
            # create a game over message at that position
            message = Actor()
            message.set_text(
                f"Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)

            # hide current display elements
            display_elements = cast.get_actors("scores")
            for display in display_elements:
                display.set_color(constants.BLACK)
            display_elements = cast.get_actors("shields")
            for display in display_elements:
                display.set_color(constants.BLACK)

            # get ship
            ship = cast.get_first_actor("ships")
            parts = ship.get_parts()
            # loop through every part
            for part in parts:
                # make sparks and explosion there
                self._create_explosion(cast, part.get_position())
                self._create_sparks(
                    cast, 3, part.get_position(), 5, 13, 0, 360)

            # delete the ship parts
            ship.remove_parts()

            # delete all enemies
            cast.remove_actors("asteroids")

    def _handle_player_upgrade_collision(self, cast):
        ship = cast.get_first_actor("ships")
        parts = ship.get_parts()
        upgrades = cast.get_actors("upgrades")
        for upgrade in upgrades:
            for part in parts:
                if part.get_position().equals(upgrade.get_position()):
                    shields = cast.get_first_actor("shields")
                    shields.add_points(10)
                    cast.remove_actor("upgrades", upgrade)
                    # play upgrade sound
                    self._audio_service.play_sound("upgrade")

    def _create_sparks(self, cast, amount, position, speed_min, speed_max, dir, dir_range):
        """"Create a certain number of sparks at a certain location between min/max speed and min/max direction"""
        for i in range(0, amount):
            # create some sparks at our location
            spark = Spark(cast)
            spark.set_text(".")
            spark.set_color(constants.WHITE)
            spark.set_speed(speed_min + random.random()
                            * (speed_max-speed_min))
            spark.set_direction(dir + (random.random()-0.5)*dir_range)
            spark.set_position(position)
            # add explosion to "explosions" cast group
            cast.add_actor("sparks", spark)

    def _create_explosion(self, cast, position):
        """"Create an explosion at location"""
        # create an explosion at the parts position
        explosion = Explosion(cast)
        explosion.set_text(".")
        explosion.set_color(constants.WHITE)
        explosion.set_velocity(Point(0, 1))
        explosion.set_position(position)
        explosion.set_animate_speed(0.1 + random.random()*0.8)
        # add explosion to "explosions" cast group
        cast.add_actor("explosions", explosion)
