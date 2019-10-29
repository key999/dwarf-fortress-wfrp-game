import curses
import object
from character_creator import Creator


class UI:
    cursor = "<="
    ver = "v.0.6"
    date = "14.06.18, 00:31"
    player = object.Player()
    units = [player]
    key_enter = [curses.KEY_ENTER, 10, 13]
    key_back = [curses.KEY_BACKSPACE, 27]

    def __init__(self, units, height, width):
        self.units = units
        self.height = height
        self.width = width

    def initialize_window(self):
        curses.initscr()
        curses.cbreak()
        window = curses.newwin(self.height, self.width)
        window.keypad(1)
        window.timeout(-1)
        return window

    def start_screen(self):
        window = self.initialize_window()
        window.timeout(-1)

        while True:
            window.clear()
            window.border()

            welcome = "Best RPG 9000"
            window.addstr(self.height // 2,
                          self.width // 2 - (len(welcome) // 2),
                          welcome)
            window.addstr(1, 1, "")

            event = window.getch()

            if event in self.key_enter:
                break
            if event in self.key_back:
                exit()

        curses.endwin()
        self.menu_main()

    def menu_main(self):
        window = self.initialize_window()
        options = ["^^ New game ^^",
                   "^^ Load game ^^",
                   "^^ Exit ^^"]
        cursor_x = self.width // 3 + 3
        cursor_y = self.height // 2 - 5
        cursor_y_up = self.height // 2 - 5
        cursor_y_down = cursor_y_up + (2 * len(options) - 2)  # tbh i have no idea why that -2 was needed

        while True:
            self.set(window)

            zipped = zip(options, [i for i in range(0, 2 * len(options)) if i % 2 == 0])

            # show menu choices onscreen
            self.menu(zipped, window)

            window.addstr(cursor_y, cursor_x, self.cursor)  # menu cursor
            window.addstr(1, 1, "")  # put prompt in left upper corner, just for looks

            # KEY CAPTURE SECTION
            event = window.getch()

            # move cursor down - KEY_DOWN
            if event == curses.KEY_DOWN and cursor_y < cursor_y_down:
                cursor_y += 2

            # move cursor up - KEY_UP
            if event == curses.KEY_UP and cursor_y > cursor_y_up:
                cursor_y -= 2

            # go to next section - ENTER, KEY_RIGHT
            ############################################
            ############# NIE ŁAPIE ENTERA #############
            ############################################
            if event in self.key_enter:
                if cursor_y == cursor_y_up:
                    whereto = "new"
                    break
                elif cursor_y == cursor_y_up + 2:
                    whereto = "load"
                    break
                elif cursor_y == cursor_y_up + 4:
                    exit()

        if whereto == "new":
            self.menu_newgame()
        elif whereto == "load":
            self.menu_load()
        elif whereto == "fightdebug":
            self.menu_load()
        elif whereto == "mapdebug":
            self.menu_load()
        return

    def menu_newgame(self):
        window = self.initialize_window()
        whereto = None
        while True:
            self.set(window)

            window.addstr(self.height // 4,
                          self.width // 4,
                          "Before we start, you need your character created")
            window.addstr(self.height // 4 + 1,
                          self.width // 4,
                          "ENTER to continue, BACKSPACE to return")

            window.addstr(1, 1, "")  # put prompt in left upper corner, just for looks

            # KEY CAPTURE SECTION
            event = window.getch()

            if event in self.key_enter:
                whereto = "create"
                curses.endwin()
                break
            if event in self.key_back:
                whereto = "main"
                curses.endwin()
                break

        if whereto == "main":
            self.menu_main()
        elif whereto == "create":
            self.menu_character_create()

    def menu_character_create(self):
        def create(race):
            window = self.initialize_window()

            while True:
                self.set(window)

                text = "Second, sex - (male, female)"
                window.addstr(self.height // 4 + 1,
                              self.width // 4,
                              text)
                text = "Your choice? - "
                window.addstr(self.height // 4 + 2,
                              self.width // 4,
                              text)

                try:
                    event = window.getstr(self.height // 4 + 2,
                                          self.width // 4 + len(text),
                                          6)

                    if event[0] == ord("m") or event[0] == ord("M"):
                        _player = Creator()
                        _whereto = "finalize"
                        self.units[0] = _player.create(race, "male")
                        break
                    if event[0] == ord("f") or event[0] == ord("F"):
                        _player = Creator()
                        _whereto = "finalize"
                        self.units[0] = _player.create(race, "female")
                        break

                except IndexError:
                    _whereto = "newgame"
                    curses.endwin()
                    break

            if _whereto == "newgame":
                curses.endwin()
                self.menu_newgame()
            elif _whereto == "finalize":
                curses.endwin()
                self.menu_character_create_finalize()

        window = self.initialize_window()
        while True:
            self.set(window)

            text = "First, race - (human, elf, dwarf, halfling)"
            window.addstr(self.height // 4 + 1,
                          self.width // 4,
                          text)
            text = "Your choice? - "
            window.addstr(self.height // 4 + 2,
                          self.width // 4,
                          text)

            try:
                event = window.getstr(self.height // 4 + 2,
                                      self.width // 4 + len(text),
                                      8)

                # human
                if (event[0] == ord("h") or event[0] == ord("H")) and \
                        (event[-1] == ord("n") or event[-1] == ord("N")):
                    whereto = "human"
                    curses.endwin()
                    break

                # elf
                if event[0] == ord("e") or event[0] == ord("E"):
                    whereto = "elf"
                    curses.endwin()
                    break

                # dwarf
                if event[0] == ord("d") or event[0] == ord("D"):
                    whereto = "dwarf"
                    curses.endwin()
                    break

                # halfling
                if (event[0] == ord("h") or event[0] == ord("H")) and \
                        (event[-1] == ord("g") or event[-1] == ord("G")):
                    whereto = "halfling"
                    curses.endwin()
                    break

            except IndexError:
                whereto = "newgame"
                break

        if whereto == "newgame":
            self.menu_newgame()
        elif whereto == "human":
            create(whereto)
        elif whereto == "elf":
            create(whereto)
        elif whereto == "dwarf":
            create(whereto)
        elif whereto == "halfling":
            create(whereto)

    def menu_character_create_finalize(self):
        window = self.initialize_window()

        while True:
            self.set(window)

            text = "{0} {1} {2} created".format(self.units[0].sex.capitalize(),
                                                self.units[0].race.capitalize(),
                                                self.units[0].name)
            window.addstr(3, 4, text)

            self.stats(window)

            window.addstr(24, 4, "If created character is acceptable press ENTER")
            window.addstr(25, 4, "Otherwise press BACKSPACE to return to main menu")
            window.addstr(1, 1, "")

            event = window.getch()
            if event in self.key_back:
                whereto = "main"
                curses.endwin()
                break
            if event in self.key_enter:
                whereto = "start"
                curses.endwin()
                break

        if whereto == "main":
            self.menu_main()
        elif whereto == "start":
            curses.endwin()
            return 1

    def menu_load(self):
        window = self.initialize_window()
        while True:
            self.set(window)

            window.addstr(self.height // 4,
                          self.width // 4,
                          "Currently unavailable")

            window.addstr(1, 1, "")  # put prompt in left upper corner, just for looks

            event = window.getch()

            if event != 0:
                curses.endwin()
                break
        self.menu_main()

    def menu(self, text, window):
        window.clear()
        window.border()  # window border

        window.addstr(1, self.width - len(self.ver) - 1, self.ver)  # app version
        window.addstr(2, self.width - len(self.date) - 1, self.date)  # app date

        for i, j in text:
            window.addstr(self.height // 2 - (5 - j),
                          self.width // 3 - len(i),
                          i)

        window.addstr(1, 1, "")  # put prompt in left upper corner, just for looks

    def set(self, window):
        window.clear()
        window.border()  # window border

        window.addstr(1, self.width - len(self.ver) - 1, self.ver)  # app version
        window.addstr(2, self.width - len(self.date) - 1, self.date)  # app date

    def stats(self, window):
        text = "{0}'s characteristics:".format(self.units[0].name)
        window.addstr(4, 4, text)

        window.addstr(6, 4, "Weapon Skill:             {0}".format(self.units[0].ww))
        window.addstr(7, 4, "Ballistics Skill:         {0}".format(self.units[0].us))
        window.addstr(8, 4, "Strength:                 {0}".format(self.units[0].k))
        window.addstr(9, 4, "Toughness:                {0}".format(self.units[0].odp))
        window.addstr(10, 4, "Agility:                  {0}".format(self.units[0].zr))
        window.addstr(11, 4, "Intelligence:             {0}".format(self.units[0].int))
        window.addstr(12, 4, "Will Power:               {0}".format(self.units[0].sw))
        window.addstr(13, 4, "Fellowship:               {0}".format(self.units[0].ogd))

        window.addstr(15, 4, "Attacks:                  {0}".format(self.units[0].a))
        window.addstr(16, 4, "Wounds (HP):              {0}".format(self.units[0].zyw))
        window.addstr(17, 4, "Strength Bonus:           {0}".format(self.units[0].s))
        window.addstr(18, 4, "Toughness Bonus:          {0}".format(self.units[0].wt))
        window.addstr(19, 4, "Movement:                 {0}".format(self.units[0].sz))
        window.addstr(20, 4, "Magic:                    {0}".format(self.units[0].mag))
        window.addstr(21, 4, "Insanity Points:          {0}".format(self.units[0].po))
        window.addstr(22, 4, "Fate Points (revives):    {0}".format(self.units[0].pp))

        text = "{0}'s equipment:".format(self.units[0].name)
        window.addstr(4, self.width // 2, text)

        window.addstr(6, self.width // 2,
                      "Weapon: {0} (Attack bonus: {1})".format(self.units[0].weapon.name,
                                                               self.units[0].weapon.damage))
        window.addstr(8, self.width // 2,
                      "Armour:")
        window.addstr(9, self.width // 2,
                      "Head: {0}, protection: {1}".format(self.units[0].armor_head.type,
                                                          self.units[0].armor_head.prot))
        window.addstr(10, self.width // 2,
                      "Body: {0}, protection: {1}".format(self.units[0].armor_body.type,
                                                          self.units[0].armor_body.prot))
        window.addstr(11, self.width // 2,
                      "Right arm: {0}, protection: {1}".format(self.units[0].armor_rhand.type,
                                                          self.units[0].armor_rhand.prot))
        window.addstr(12, self.width // 2,
                      "Left arm: {0}, protection: {1}".format(self.units[0].armor_lhand.type,
                                                          self.units[0].armor_lhand.prot))
        window.addstr(13, self.width // 2,
                      "Right leg: {0}, protection: {1}".format(self.units[0].armor_rleg.type,
                                                          self.units[0].armor_rleg.prot))
        window.addstr(14, self.width // 2,
                      "Left leg: {0}, protection: {1}".format(self.units[0].armor_lleg.type,
                                                          self.units[0].armor_lleg.prot))