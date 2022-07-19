from game.scripting.action import Action


class DrawActorsAction(Action):
    """
    An output action that draws all the actors.

    The responsibility of DrawActorsAction is to draw all the actors.

    Attributes:
        _video_service (VideoService): An instance of VideoService.
    """

    def __init__(self, video_service):
        """Constructs a new DrawActorsAction using the specified VideoService.

        Args:
            video_service (VideoService): An instance of VideoService.
        """
        self._video_service = video_service
        self._game_started = False

    def set_game_started(self, started):
        self._game_started = started

    def execute(self, cast, script):
        """Executes the draw actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        # GATHER ACTORS TO DRAW - - -

        # menu items
        menus = cast.get_actors("menus")
        highscores = cast.get_actors("highscores")

        # if game is started get gameplay actors
        if self._game_started:

            # display elements
            score = cast.get_first_actor("scores")
            shield = cast.get_first_actor("shields")
            messages = cast.get_actors("messages")
            stage_messages = cast.get_actors("stage messages")
            # ship parts
            ship = cast.get_first_actor("ships")
            parts = ship.get_parts()
            # lasers
            lasers = cast.get_actors("lasers")
            # asteroids
            asteroid_parts = []
            asteroids = cast.get_actors("asteroids")
            # append all asteroid parts into one list
            for asteroid in asteroids:
                for part in asteroid.get_parts():
                    asteroid_parts.append(part)
            # asteroids
            ufo_parts = []
            ufos = cast.get_actors("ufos")
            # append all ufo parts into one list
            for ufo in ufos:
                for part in ufo.get_parts():
                    ufo_parts.append(part)
            # explosions
            explosions = cast.get_actors("explosions")
            # sparks
            sparks = cast.get_actors("sparks")
            # upgrades
            upgrades = cast.get_actors("upgrades")

        # DRAW ACTORS - - - - - - -
        self._video_service.clear_buffer()

        # draw menus
        self._video_service.draw_actors(menus, True)
        self._video_service.draw_actors(highscores)

        if self._game_started:
            # draw hud elements
            self._video_service.draw_actor(score)
            self._video_service.draw_actor(shield)
            self._video_service.draw_actors(messages, True)
            self._video_service.draw_actors(stage_messages, True)
            # draw player ship
            self._video_service.draw_actors(parts)
            # draw lasers
            self._video_service.draw_actors(lasers)
            # draw asteroids
            self._video_service.draw_actors(asteroid_parts)
            # draw ufos
            self._video_service.draw_actors(ufo_parts)
            # draw explosions
            self._video_service.draw_actors(explosions)
            # draw explosions
            self._video_service.draw_actors(sparks)
            # draw upgrades
            self._video_service.draw_actors(upgrades)

        self._video_service.flush_buffer()
