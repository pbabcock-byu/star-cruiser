import pyray
import constants


class AudioService:
    """Plays sounds and music
    """

    def __init__(self):
        """Constructs a new AudioService
        Args:

        """
        # this is to initialize the audio device
        pyray.init_audio_device()

        self._sounds = {}
        # ship
        self._sounds['laser'] = pyray.load_sound(constants.SHIP_FIRE_SOUND)
        self._sounds['ship-hit'] = pyray.load_sound(constants.SHIP_HIT_SOUND)
        self._sounds['ship-exp'] = pyray.load_sound(constants.SHIP_EXPLOSION_SOUND)
        # asteroids
        self._sounds['ast-hit'] = pyray.load_sound(constants.ASTEROIDS_HIT_SOUND)
        self._sounds['ast-hit-sml'] = pyray.load_sound(constants.ASTEROIDS_HIT_SML_SOUND)
        self._sounds['ast-hit-lrg'] = pyray.load_sound(constants.ASTEROIDS_HIT_LRG_SOUND)
        self._sounds['ast-hit-giant'] = pyray.load_sound(constants.ASTEROIDS_HIT_GIANT_SOUND)
        self._sounds['ast-hit-exp'] = pyray.load_sound(constants.ASTEROIDS_HIT_GIANT_EXP_SOUND)
        # menu
        self._sounds['menu-select'] = pyray.load_sound(constants.MENU_SELECT_SOUND)
        self._sounds['menu-start'] = pyray.load_sound(constants.MENU_START_SOUND)
        self._sounds['enter-initial'] = pyray.load_sound(constants.ENTER_INITIAL_SOUND)
        self._sounds['new-highscore'] = pyray.load_sound(constants.NEW_HIGHSCORE_SOUND)
        # game
        self._sounds['game-over'] = pyray.load_sound(constants.GAMEOVER_SOUND)
        self._sounds['new-stage'] = pyray.load_sound(constants.NEW_STAGE_SOUND)
        self._sounds['upgrade'] = pyray.load_sound(constants.UPGRADE_SOUND)
        self._sounds['low-shields'] = pyray.load_sound(constants.LOW_SHIELDS_WARNING_SOUND)
        # music
        self._sounds['menu-music'] = pyray.load_sound(constants.MUSIC_MENU_SOUND)
        self._sounds['game-music'] = pyray.load_sound(constants.MUSIC_GAMEPLAY_SOUND)

    def play_sound(self, sound):
        """ plays sound using string and looking it up in _sounds dictionary"""
        pyray.play_sound(self._sounds[sound])
        print(sound)
