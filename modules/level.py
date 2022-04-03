def GetLevel(price):
    increment = 5
    rounded = int(price - (price % increment))

    return rounded