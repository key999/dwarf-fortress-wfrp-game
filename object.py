from random import randint


class Character:
    def __init__(self, name="blank"):
        self.type = ""
        self.board = ""
        self.pos_x = 0
        self.pos_y = 0
        self.race = ""

        self.name = name
        self.ww = 0
        self.us = 0
        self.k = 0
        self.odp = 0
        self.zr = 0
        self.int = 0
        self.sw = 0
        self.ogd = 0
        self.a = 0
        self.zyw = 0
        self.sz = 0
        self.mag = 0
        self.po = 0
        self.pp = 0

        self.s = self.k // 10
        self.wt = self.odp // 10

        self.sex = ""

        self.armor_head = Armor("None")
        self.armor_body = Armor("None")
        self.armor_lhand = Armor("None")
        self.armor_lleg = Armor("None")
        self.armor_rhand = Armor("None")
        self.armor_rleg = Armor("None")

        self.weapon = Weapon("Improvised", "Fists")

    def __str__(self):
        return self.name


class Player(Character):
    exp_cumulative = exp_current = 0

    def __init__(self):
        super().__init__()
        self.type = "player"

    def exp_add(self, amount):
        self.exp_cumulative += amount
        self.exp_current += amount

    def exp_spend(self, amount, stat):
        self.exp_current -= amount
        self.ww += amount // 50 if stat == "ww" else None
        self.us += amount // 50 if stat == "us" else None
        self.k += amount // 50 if stat == "k" else None
        self.odp += amount // 50 if stat == "odp" else None
        self.zr += amount // 50 if stat == "zr" else None
        self.int += amount // 50 if stat == "int" else None
        self.sw += amount // 50 if stat == "sw" else None
        self.ogd += amount // 50 if stat == "ogd" else None
        self.a += amount // 50 if stat == "a" else None
        self.zyw += amount // 50 if stat == "zyw" else None
        self.mag += amount // 50 if stat == "mag" else None


class Troll(Character):
    def __init__(self, name):
        super().__init__()
        self.type = "troll"
        self.name = name
        self.ww = 35
        self.s = 3
        self.zyw = 12
        self.a = 1
        self.wt = 4
        self.weapon = Weapon("Twohanded", "Big stick")
        self.armor_head = Armor("None")
        self.armor_body = Armor("None")
        self.armor_rhand = Armor("None")
        self.armor_lhand = Armor("None")
        self.armor_rleg = Armor("None")
        self.armor_lleg = Armor("None")


class Weapon:
    weapon_types = {"Onehanded": [0, True],
                    "Twohanded": [1, False],
                    "Staff": [1, True],
                    "Dagger": [-2, True],
                    "Improvised": [-4, False]}

    def __init__(self, type, name):
        self.type = type
        self.name = name

        self.parry = self.weapon_types[type][1]
        self.damage = self.weapon_types[type][0]


class Armor:
    armor_types = {"None": 0,
                   "Cloth": 1,
                   "Chain": 2,
                   "Plate": 3}

    def __init__(self, type):
        self.type = type
        self.prot = self.armor_types[type]


class Tile:
    def __init__(self, sign="", passable=True):
        self.sign = sign
        self.passable = passable

    def __str__(self):
        return (self.sign)


class Floor(Tile):
    def __init__(self):
        super().__init__()
        self.passable = True
        s = [",", ".", " "]
        self.sign = s[randint(0, len(s) - 1)]
