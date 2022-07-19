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

    The responsibility of HandleCollisionsAction is to handle the situation when the ship collides
    with enemies, or the laser collides with enemies, or ship collides with upgrades, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
        _game_over_timer (int): waits n frames after player dies to display highscore table
    """

    def __init__(self, handle_menu_system, audio_service):
        """Constructs a new HandleCollisionsAction.
        Args:
            handle_menu_system (Action): reference to menu system so we can tell is when game over happens
            audio_service (AudioService): An instance of AudioService.
        """
        # services
        self._handle_menu_system = handle_menu_system
        self._audio_service = audio_service
        # game over variables
        self._is_game_over = False
        self._game_over_timer = 0

    def execute(self, cast, script):
        """Executes the handle collisions action.
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        # as long as the game isn't over
        if not self._is_game_over:

            # run the collision checks for enemies, lasers, and upgrades
            self._handle_laser_enemy_collision(cast, ["asteroids","ufos"])
            self._handle_player_enemy_collision(cast, ["asteroids","ufos"])
            self._handle_player_lasers_collision(cast)
            self._handle_player_upgrade_collision(cast)

            # run this last in case we get game over in the player-enemy collision check above
            self._handle_game_over(cast)

        else:
            # it's game over
            if self._game_over_timer < 75:
                # wait a while to display "game over" on the screen
                self._game_over_timer += 1
            else:

                # run the following code once
                if self._game_over_timer != 100:
                    self._game_over_timer = 100 # (arbitrary number greater than wait time)
                    # set the menu system state to display the highscore table
                    self._handle_menu_system.set_menu_state("highscore")
                    # remove game over message
                    cast.remove_actor("messages", cast.get_first_actor("messages"))


    def _handle_laser_enemy_collision(self, cast, groups):
        """removes health from enemies when laser hits them
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # get list of all lasers on the screen right now
        lasers = cast.get_actors("lasers")
        # keep track of whether there's a hit so we can break the nested for loops
        hit = False

        # for every laser
        for laser in lasers:
            # loop through every group in the enemies groups list
            for group in groups:
                if hit: break

                # loop through every enemy in this group
                for enemy in cast.get_actors(group):
                    if hit: break

                    # loop through every part of this enemy
                    for enemypart in enemy._parts:

                        # get corrected enemy position
                        enemy_position = Point(enemypart.get_position().get_x() - enemypart.get_velocity().get_x(), enemypart.get_position().get_y())

                        # get laser position
                        laser_position = laser.get_position()
                        # also get it's last position just in case they jumped over eachother
                        laser_last_position = Point(laser.get_position().get_x(), laser.get_position().get_y()+constants.CELL_SIZE)

                        # assume false
                        collision = False

                        if laser_position.equals(enemypart.get_position()) or laser_last_position.equals(enemypart.get_position()):
                            collision = True

                        if laser_position.equals(enemy_position) or laser_last_position.equals(enemy_position):
                            collision = True

                        # if enemy parts position is equal to lasers
                        if collision:

                            # create an explosion at the lasers position
                            self._create_explosion(cast, laser_last_position)
                            # apply damage from laser to enemy health
                            destroyed = enemy.remove_health(laser.get_damage())

                            # if enemy was destroyed
                            if destroyed:
                                # play the enemies destroy sound
                                self._audio_service.play_sound(enemy.get_exp_sound())                        
                            else:
                                # play enemies hit sound
                                self._audio_service.play_sound(enemy.get_hit_sound())

                            # delete the laser
                            cast.remove_actor("lasers", laser)

                            # break all loops
                            hit = True
                            break

    def _handle_player_enemy_collision(self, cast, groups):
        """Checks if the ship has collided with an enemy and applies damage to shields.
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # get reference to ship
        ship = cast.get_first_actor("ships")

        # don't check if ships hurt timer is on
        if ship.get_is_hurt() == False:

            # get list of ship parts
            parts = ship.get_parts()
            # break for loops if there's a collision
            hit = False

            # loop through every part
            for part in parts:
                if hit: break

                # loop through every enemy group
                for group in groups:
                    if hit: break

                    # loop through every enemy in this group
                    for enemy in cast.get_actors(group):
                        if hit: break

                        # loop through every part in this enemies part list
                        for enemypart in enemy._parts:

                            # if this ship part is colliding with this enemy part
                            if part.get_position().equals(enemypart.get_position()):
                                # set hit to true so we can break the loop and only apply one hit at a time
                                hit = True

                                # get reference to shields instance
                                shields = cast.get_first_actor("shields")
                                shields.add_points( - enemy.get_damage())

                                # create sparks that bounce off player ship
                                self._create_sparks(cast, 20, part.get_position(), 5, 13, 270, 40)
                            
                                # if player is moving sideways send sparks sideways too
                                if ship.get_velocity().get_x() > 0: # right
                                    self._create_sparks(cast, 20, part.get_position(), 10, 23, 350, 40)
                                if ship.get_velocity().get_x() < 0: # left
                                    self._create_sparks(cast, 20, part.get_position(), 10, 23, 190, 40)

                                # remove all the enemies health
                                enemy.remove_health(1000) # (must be 1000, see asteroid class for details)

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
                                    # if we are low on shields
                                    if shields.get_points() <= 4:
                                        # play low shields warning sound
                                        self._audio_service.play_sound("low-shields")

                                # break the loop
                                break

    def _handle_player_lasers_collision(self, cast):
        """Checks if the ship has collided with an enemy laser and applies damage to shields.
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # get reference to ship
        ship = cast.get_first_actor("ships")

        # don't check if ships hurt timer is on
        if ship.get_is_hurt() == False:

            # get list of ship parts
            parts = ship.get_parts()
            # break for loops if there's a collision
            hit = False

            # loop through every part
            for part in parts:
                if hit: break

                # loop through every enemy in this group
                for laser in cast.get_actors("lasers"):
                    if hit: break

                    # if this ship part is colliding with this enemy part
                    if part.get_position().equals(laser.get_position()):
                        # set hit to true so we can break the loop and only apply one hit at a time
                        hit = True

                        # get reference to shields instance
                        shields = cast.get_first_actor("shields")
                        shields.add_points( - laser.get_damage())

                        # create sparks that bounce off player ship
                        self._create_sparks(cast, 20, part.get_position(), 5, 13, 270, 40)
                    
                        # if player is moving sideways send sparks sideways too
                        if ship.get_velocity().get_x() > 0: # right
                            self._create_sparks(cast, 20, part.get_position(), 10, 23, 350, 40)
                        if ship.get_velocity().get_x() < 0: # left
                            self._create_sparks(cast, 20, part.get_position(), 10, 23, 190, 40)

                        # remove all the enemies health
                        cast.remove_actor("lasers", laser)

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
                            # if we are low on shields
                            if shields.get_points() <= 4:
                                # play low shields warning sound
                                self._audio_service.play_sound("low-shields")

                        # break the loop
                        break


    def _handle_game_over(self, cast):
        """Shows the 'game over' message and explodes the ship.
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

            # HIDE other display elements by turning their color black
            display_elements = cast.get_actors("scores")
            for display in display_elements:
                display.set_color(constants.BLACK)
            display_elements = cast.get_actors("shields")
            for display in display_elements:
                display.set_color(constants.BLACK)

            # DISPLAY game over message at screen center
            message = Actor()
            message.set_text(f"Game Over!")
            # get center screen position
            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y * 0.5)
            position = Point(x, y)
            message.set_position(position)
            # display it
            cast.add_actor("messages", message)

            # get ship reference
            ship = cast.get_first_actor("ships")
            # get ships list of parts
            parts = ship.get_parts()
            # loop through every part
            for part in parts:
                # make sparks and explosion there
                self._create_explosion(cast, part.get_position())
                self._create_sparks(cast, 3, part.get_position(), 5, 13, 0, 360)

            # delete the ship parts
            ship.remove_parts()
            # delete all enemies
            cast.remove_actors("asteroids")
            cast.remove_actors("lasers")
            cast.remove_actors("ufos")

    def _handle_player_upgrade_collision(self, cast):
        """ When the player collides with an upgrade item, apply it's upgrade.
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # get ship reference
        ship = cast.get_first_actor("ships")
        # get list of all ship parts
        parts = ship.get_parts()
        # get list of all upgrades
        upgrades = cast.get_actors("upgrades")

        # for every upgrade
        for upgrade in upgrades:
            # for every part in ship
            for part in parts:
                # see if part position x matches upgrade position x
                if part.get_position().get_x() == upgrade.get_position().get_x():
                    # if we are within a certain y distance consider it a collision
                    if abs(part.get_position().get_y() - upgrade.get_position().get_y()) < 15:
                        # get reference to shields
                        shields = cast.get_first_actor("shields")

                        # add points (apply upgrade)
                        if upgrade.get_type() == "shield":
                            shields.add_points(10)

                        if upgrade.get_type() == "gun-rapid":
                            ship.set_gun_type("rapid")

                        if upgrade.get_type() == "gun-shotgun":
                            ship.set_gun_type("shotgun")

                        # remove that upgrade from screen
                        cast.remove_actor("upgrades", upgrade)
                        # play upgrade sound
                        self._audio_service.play_sound("upgrade")
                        # break loop so we don't count it twice
                        break

    def _create_sparks(self, cast, amount, position, speed_min, speed_max, dir, dir_range):
        """"Create a certain number of sparks at a certain location between min/max speed and min/max direction
        Args:
            cast (Cast): The cast of Actors in the game.
            amount (int): number of sparks to create
            position (Point): position to create the sparks
            speed_min (float): minimum speed a spark might move
            speed_max (float): maximum speed a spark might randomly move
            dir (int): direction spark will move in degrees 0-360
            dir_range (int):  randomizes the direction angle by this amount
        """
        # create this amount of sparks
        for i in range(0, amount):
            # create instance
            spark = Spark(cast)
            spark.set_text(".")
            spark.set_color(constants.WHITE)
            spark.set_speed(speed_min + random.random() * (speed_max-speed_min))
            spark.set_direction(dir + (random.random()-0.5)*dir_range)
            spark.set_position(position)
            # add spark to "sparks" cast group
            cast.add_actor("sparks", spark)

    def _create_explosion(self, cast, position):
        """"Create an explosion at location
        Args:
            cast (Cast): The cast of Actors in the game.
            position (Point): position to create the explosion       
        """
        # create an explosion at the parts position
        explosion = Explosion(cast)
        explosion.set_text(".")
        explosion.set_color(constants.WHITE)
        explosion.set_velocity(Point(0, 1))
        explosion.set_position(position)
        explosion.set_animate_speed(0.1 + random.random()*0.8)
        # add explosion to "explosions" cast group
        cast.add_actor("explosions", explosion)
