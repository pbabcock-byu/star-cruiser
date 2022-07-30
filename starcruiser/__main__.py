import constants
from game.casting.cast import Cast
from game.scripting.script import Script
from game.scripting.draw_actors_action import DrawActorsAction
from game.directing.director import Director
from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService
from game.services.audio_service import AudioService
from game.shared.color import Color
from game.shared.point import Point
from game.scripting.handle_menu_system import handleMenuSystem


def main():

    # create the cast
    cast = Cast()

    # create services
    keyboard_service = KeyboardService()
    audio_service = AudioService()
    video_service = VideoService(audio_service)

    # create actions
    draw_actors_instance = DrawActorsAction(video_service)
    handle_menu_system = handleMenuSystem(
        keyboard_service, draw_actors_instance, video_service, audio_service)

    # create scripts and start running menu system
    script = Script()
    script.add_action("update", handle_menu_system)
    script.add_action("output", draw_actors_instance)

    # create director to execute scripts
    director = Director(video_service)
    director.start_game(cast, script)


if __name__ == "__main__":
    main()
