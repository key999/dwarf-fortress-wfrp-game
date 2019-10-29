import dice
import curses


class Manager:
    height = 30
    width = 80

    def __init__(self, a, b, units):
        self.a = a
        self.b = b
        self.units = units

    def fight(self):
        window = self.initialize_window()

        options = ["Melee attack",
                   "Ranged attack",
                   "Magic attack",
                   "Escape fight"]
        cursor_x = len(max(options, key=len)) + 5
        cursor_y = 15
        cursor_y_up = 15
        cursor_y_down = 15 + 2 * len(options) - 2
        cursor = "<"

        while True:
            window.clear()
            window.border()

            # LAYOUT AND DECORATIONS
            window.addstr(10, 1, (self.width - 2) * "_")
            window.addstr(13, 1, (self.width - 2) * "_")
            for i in range(14, self.height - 1):
                window.addstr(i, cursor_x + 2, "|")
            self.draw_player(window)
            self.draw_enemy(window, self.units[self.b].type)
            self.stats(window)

            # WELCOME / ANNOUNCE
            text = "{0} fights with {1} (a {2}). What is your " \
                   "move?".format(self.units[self.a].name, self.units[self.b].name,
                                  self.units[self.b].type)
            window.addstr(12, 3, text)

            # OPTIONS / MENU
            zipped = zip(options, [i for i in range(0, 2 * len(options), 2)])
            for i, j in zipped:
                window.addstr(15 + j, 3, i)

            # CURSOR
            window.addstr(cursor_y, cursor_x, cursor)

            # ACTIONS
            text = ""
            window.addstr(16, 15, text)

            window.addstr(1, 1, "")

            event = window.getch()

            if event == curses.KEY_DOWN and cursor_y < cursor_y_down:
                cursor_y += 2
            if event == curses.KEY_UP and cursor_y > cursor_y_up:
                cursor_y -= 2
            if event == ord("q"):
                whereto = "escape"
                break
            if event in [curses.KEY_ENTER, 10, 13]:
                if cursor_y == cursor_y_up:  # MELEE
                    whereto = "melee"
                    curses.endwin()
                    break
                elif cursor_y == cursor_y_up + 2:  # RANGED
                    whereto = "ranged"
                    curses.endwin()
                    break
                elif cursor_y == cursor_y_up + 4:  # MAGIC
                    whereto = "magic"
                    curses.endwin()
                    break
                elif cursor_y == cursor_y_up + 6:  # ESCAPE
                    whereto = "escape"
                    curses.endwin()
                    break
                else:
                    whereto = "escape"
                    curses.endwin()
                    break

        if whereto == "melee":
            self.melee(self.units[self.a], self.units[self.b])
            if self.units[self.b].zyw <= 0:
                self.end(self.units[self.a], self.b, self.units[self.b])
                return
            self.enemy_turn()
            if self.units[self.a].zyw <= 0:
                self.end(self.units[self.b], self.a, self.units[self.a])
                return -1
        elif whereto == "ranged":
            self.enemy_turn()
            if self.units[self.a].zyw <= 0:
                self.end(self.units[self.b], self.a, self.units[self.a])
                return -1
        elif whereto == "magic":
            pass
        elif whereto == "escape":
            if self.escape() == 0:
                self.enemy_turn()
                if self.units[self.a].zyw <= 0:
                    self.end(self.units[self.b], self.a, self.units[self.a])
                    return -1

    def initialize_window(self):
        curses.initscr()
        curses.cbreak()
        window = curses.newwin(self.height, self.width)
        window.keypad(1)
        window.timeout(-1)
        return window

    def draw_player(self, window):
        with open("arts/player", "r") as f:
            for i in f:
                for j in range(2, 10):
                    window.addstr(j, 2, f.readline())

    def draw_enemy(self, window, type):
        file = "arts/" + type
        with open(file, "r") as f:
            for i in f:
                for j in range(2, 10):
                    window.addstr(j, 35, f.readline())

    def melee(self, a, b):
        window = self.small_window()

        while True:
            window.clear()

            window.addstr(1, 1, "You try to hit {0} with your {1}".format(self.units[self.b].name,
                                                                          self.units[self.a].weapon.name))
            self.hit(a, b, window)

            if window.getch():
                return

    def escape(self):
        window = self.small_window()

        while True:
            window.clear()

            if dice.toss(100) <= self.units[self.a].ww + self.units[self.a].zr:
                success = 1
                window.addstr(1, 1, "You try to escape and are successful")
            else:
                success = 0
                window.addstr(1, 1, "You try to escape but are unsuccessful")
                window.addstr(2, 1, "{0} gets a chance to attack you".format(self.units[self.b]))

            if window.getch():
                break

        if success:
            try:
                self.units[self.a].pos_x += 1
                return 1
            except curses.ERR:
                self.units[self.a].pos_x -= 1
        return 0

    def small_window(self):
        curses.initscr()
        curses.cbreak()
        pad_y = 14
        pad_x = 21
        window = curses.newwin(self.height - pad_y - 1, self.width - pad_x - 1, pad_y, pad_x)
        window.keypad(1)
        window.timeout(-1)
        return window

    def hit(self, a, b, window):
        attack_roll = dice.toss(100)
        if attack_roll <= a.ww:
            if b.weapon.parry and dice.toss(100) <= b.ww:
                window.addstr(3, 1, "{0} parries the attack".format(b.name))
                return

            damage = a.s + a.weapon.damage + dice.toss(10)
            if damage < 0:
                damage = 0
            armor = self.attack_location(attack_roll, b)
            reduction = b.wt + armor
            if damage - reduction > 0:
                b.zyw -= (damage - reduction)

                window.addstr(3, 1, "The attack connects and {0} suffers {1} damage". format(b, damage - reduction))
                return
            else:
                window.addstr(3, 1, "The attack connects but delivers no damage")
                return
        window.addstr(3, 1, "The attack misses...")

    def enemy_turn(self):
        window = self.small_window()

        while True:
            window.clear()

            window.addstr(1, 1, "{0} tries to hit you with his {1}".format(self.units[self.b].name, self.units[self.b].weapon.name))

            self.hit(self.units[self.b], self.units[self.a], window)

            if window.getch():
                break

    @staticmethod
    def attack_location(x, char):
        if 1 <= x <= 15:
            return char.armor_head.prot
        elif 16 <= x <= 35:
            return char.armor_rhand.prot
        elif 36 <= x <= 55:
            return char.armor_lhand.prot
        elif 56 <= x <= 80:
            return char.armor_body.prot
        elif 81 <= x <= 90:
            return char.armor_rleg.prot
        elif 91 <= x <= 100:
            return char.armor_lleg.prot

    def stats(self, window):
        text = "Your HP: {0}".format(self.units[self.a].zyw)
        window.addstr(1, self.width - len(text) - 1, text)

        text = "{1}'s HP: {0}".format(self.units[self.b].zyw, self.units[self.b].name)
        window.addstr(2, self.width - len(text) - 1, text)

    def end(self, a, b, b_object):
        curses.initscr()
        curses.cbreak()
        width = self.width // 2
        height = self.height // 2
        window = curses.newwin(height , width, height // 2, width // 2)
        window.keypad(1)
        window.timeout(-1)

        while True:
            window.clear()
            window.border()

            text = "{0} wins the fight".format(a.name)
            window.addstr(height // 2 - 1, width // 2 - len(text) // 2, text)
            text = "{0} dies".format(b_object.name)
            window.addstr(height // 2 + 1, width // 2 - len(text) // 2, text)

            if a.type == "player":
                a.exp_add(5)

            window.addstr(1, 1, "")

            self.units.pop(b)

            if window.getch():
                return