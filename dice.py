def toss(y):
    try:
        from secrets import randbelow
        return(randbelow(y) + 1)
    except ImportError:
        from random import randint
        return(randint(1, y))

