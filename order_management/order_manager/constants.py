from enum import Enum

class ORDER_SIDES(Enum):
    BUY = 1
    SELL = -1

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)

class ORDER_STATUS(Enum):
    OPEN = 1
    PARTIALLY_FILLED = 2
    SUCCESSFULL = 3
    UNSUCCESSFULL = 4
    CANCELLED = 5

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)
