import math

from ppi.pySingleton import Singleton  # Privte Package


class GameSettings(Singleton):
    TICKS_PER_SEC = 90

    WALKING_SPEED = 5
    RUNNING_SPEED = 10
    FLYING_SPEED = 15

    GRAVITY = 20.0
    MAX_JUMP_HEIGHT = 1.0

    JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
    TERMINAL_VELOCITY = 50

    PLAYER_HEIGHT = 2

    SECTOR_SIZE = 16

