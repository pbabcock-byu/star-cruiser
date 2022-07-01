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

    def execute(self, cast, script):
        """Executes the draw actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        # GET ACTORS TO DRAW - - - -
        # get display elements
        score = cast.get_first_actor("scores")
        shield = cast.get_first_actor("shields")
        messages = cast.get_actors("messages")
        # get ship parts
        ship = cast.get_first_actor("ships")
        parts = ship.get_parts()
        # get lasers
        lasers = cast.get_actors("lasers")
        # get asteroids
        asteroids = cast.get_actors("asteroids")
        # get explosions
        explosions = cast.get_actors("explosions")

        # DRAW ACTORS - - - - - - -
        self._video_service.clear_buffer()
        # draw hud elements
        self._video_service.draw_actor(score)
        self._video_service.draw_actor(shield)
        self._video_service.draw_actors(messages, True)
        # draw player ship
        self._video_service.draw_actors(parts)
        # draw lasers
        self._video_service.draw_actors(lasers)
        # draw asteroids
        self._video_service.draw_actors(asteroids)
        # draw explosions
        self._video_service.draw_actors(explosions)

        self._video_service.flush_buffer()
