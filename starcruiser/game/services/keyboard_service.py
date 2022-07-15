import pyray
from game.shared.point import Point


class KeyboardService:
    """Detects player input. 

    The responsibility of a KeyboardService is to indicate whether or not a key is up or down.

    Attributes:
        _keys (Dict[string, int]): The letter to key mapping.
    """

    def __init__(self):
        """Constructs a new KeyboardService."""
        self._keys = {}

        # for player movement
        self._keys['left'] = pyray.KEY_LEFT
        self._keys['right'] = pyray.KEY_RIGHT

        # for player fire weapon
        self._keys['space'] = pyray.KEY_SPACE

        # for menu selections
        self._keys['up'] = pyray.KEY_UP
        self._keys['down'] = pyray.KEY_DOWN
        
        # for menu selections, pause game
        self._keys['enter'] = pyray.KEY_ENTER

        # for entering initials into highscore board
        self._keys['back'] = pyray.KEY_BACKSPACE

        # letter keys for entering initials into highscore board
        self._keys['a'] = pyray.KEY_A
        self._keys['b'] = pyray.KEY_B
        self._keys['c'] = pyray.KEY_C
        self._keys['d'] = pyray.KEY_D
        self._keys['e'] = pyray.KEY_E
        self._keys['f'] = pyray.KEY_F
        self._keys['g'] = pyray.KEY_G
        self._keys['h'] = pyray.KEY_H
        self._keys['i'] = pyray.KEY_I
        self._keys['j'] = pyray.KEY_J
        self._keys['k'] = pyray.KEY_K
        self._keys['l'] = pyray.KEY_L
        self._keys['m'] = pyray.KEY_M
        self._keys['n'] = pyray.KEY_N
        self._keys['o'] = pyray.KEY_O
        self._keys['p'] = pyray.KEY_P
        self._keys['q'] = pyray.KEY_Q
        self._keys['r'] = pyray.KEY_R
        self._keys['s'] = pyray.KEY_S
        self._keys['t'] = pyray.KEY_T
        self._keys['u'] = pyray.KEY_U
        self._keys['v'] = pyray.KEY_V
        self._keys['w'] = pyray.KEY_W
        self._keys['x'] = pyray.KEY_X
        self._keys['y'] = pyray.KEY_Y
        self._keys['z'] = pyray.KEY_Z

        # for easily checking every letter key
        self._letters_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    def is_key_up(self, key):
        """Checks if the given key is currently up.

        Args:
            key (string): The given key (up, down, left, right, space)
        """
        pyray_key = self._keys[key.lower()]
        return pyray.is_key_up(pyray_key)

    def is_key_down(self, key):
        """Checks if the given key is currently down.

        Args:
            key (string): The given key (up, down, left, right, space)
        """
        pyray_key = self._keys[key.lower()]
        return pyray.is_key_down(pyray_key)

    def is_any_letter_key_down(self):
        """Checks if any letter keys are currently down.
        """
        # for every letter in letters list
        for letter in self._letters_list:
            # check it's associated pyray key
            pyray_key = self._keys[letter]
            if pyray.is_key_down(pyray_key):
                # return the letter
                return letter
        # else return False
        return False
