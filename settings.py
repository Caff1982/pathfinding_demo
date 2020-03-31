

def vec2int(v):
    """
    Helper function which takes a pygame vector
    object and returns a tuple with integers for
    x and y
    """
    return (int(v.x), int(v.y))


TILESIZE = 25
ROWS = 20
COLUMNS = 30
HEIGHT = ROWS * TILESIZE
WIDTH = COLUMNS * TILESIZE
FPS = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (160, 160, 160)
MEDGRAY = (75, 75, 75)
DARKGRAY = (70, 70, 70)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)