from enum import IntEnum


class Roles(IntEnum):
    GUEST = 0
    FOLLOWER = 1
    REGULAR = 2
    SUBSCRIBER = 3
    MOD = 4
    OWNER = 5
