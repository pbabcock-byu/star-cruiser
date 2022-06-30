

# REPLACED BY HANDLE ENEMY CREATION !


# import random

# from game.shared.point import Point
# from game.shared.color import Color
# from game.casting.asteriod import Asteriod


# class AsteriodCreator:
#     """
#     This call will create all the new Asteriods

#     Attributes:
#         cell_size (int): For scaling gravity to grid.
#         cols (int): Stores the column location for the new Asteriod (this is a random number)
#         font_size (int): used to assign the Asteriod a font size
#         create_rate(int): For controlling the % chance of a  new Asteriod being created
#     """

#     def __init__(self):
#         """Constructs Gravity using the specified cell size.

#         Args:
#             cell_size (int): The size of a cell in the display grid.
#             cols (int): The  number of columns in our actor grid
#             font_size (int): Font size to assign to the Asteriod
#             create_rate(int): % of how likely it is to create a new Asteriod
#         """
#         self._create_rate = 25

#     def update_asteriodcreator(self, cast):
#         if random.randint(0, 100) > (100 - self._create_rate):
#             asteriod = self.make_asteriod()
#             cast.add_actor("asteriods", asteriod)

#     def make_asteriod(self):
#         """Creates a new meteor at the top of the screen

#         Returns:
#             reference to the new meteoroid
#         """
#         x = random.randint(1, self._cols - 1)
#         y = 1
#         position = Point(x, y)
#         position = position.scale(self._cell_size)

#         r = random.randint(0, 255)
#         g = random.randint(0, 255)
#         b = random.randint(0, 255)
#         color = Color(r, g, b)

#         asteriod = Asteriod()
#         type = random.choice([["SML", "`"], ["MED", "*"], ["LRG", "@"]])
#         asteriod.set_type(type[0])
#         asteriod.set_text(type[1])
#         asteriod.set_font_size(self._font_size)
#         asteriod.set_color(color)
#         asteriod.set_position(position)

#         # returns it so Director can add it to the cast "asteriods" group
#         return asteriod
