import board
import fight
import object
import curses
from curses import KEY_UP, KEY_DOWN
from random import randint


class Game:
    player = object.Player()
    entities = [player]
    width = 80
    height = 30
    ui = board.UI(units=entities, width=width, height=height)
    map = {}
    esc_height = 20
    esc_width = 2 * esc_height

    for i in range(height):
        map[i] = []
    for i in range(len(map)):
        for j in range(width):
            x = object.Floor()
            map[i].append(x)

    troll = object.Troll(name="Andrzej")
    troll.pos_x = width - 4
    troll.pos_y = height - 4
    entities.append(troll)

    def start(self):
        self.ui.start_screen()
        self.play()

    def play(self):
        window = self.ui.initialize_window()

        while True:
            self.ui.set(window)
            window.addstr(self.height // 4,
                          self.width // 5,
                          "You will be playing as {0}".format(self.entities[0].name))
            window.addstr(self.height // 4 + 1,
                          self.width // 5,
                          "Designated \"{0}\" on the map".format(self.entities[0].name[0]))
            window.addstr(self.height // 4 + 3,
                          self.width // 5,
                          "Blah blah introduction, stuff, eggs and bacon")
            window.addstr(self.height // 4 + 4,
                          self.width // 5,
                          "ENTER to continue, BACKSPACE to main menu")
            window.addstr(1, 1, "")

            self.entities[0].pos_x = randint(self.width // 10,
                                             self.width - self.width // 10)
            self.entities[0].pos_y = randint(self.height // 10,
                                             self.height - self.height // 10)

            event = window.getch()
            if event in self.ui.key_enter:
                whereto = "start"
                curses.endwin()
                break
            if event in self.ui.key_back:
                whereto = "back"
                curses.endwin()
                break

        if whereto == "back":
            self.start()
        elif whereto == "start":
            self.game()

    def game(self):
        window = self.initialize_window()
        window.timeout(500)

        while True:
            window.clear()
            window.border()

            # CHECK FOR COLLISIONS
            b = self.collide
            if b != None:
                whereto = "fight"
                curses.endwin()
                break

            # DRAW MAP
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    window.addstr(i, j, str(self.map[i][j]))

            # move enemy
            # debug
            try:
                if randint(0, 9) == 0:
                    self.move(1, randint(-1, 1), randint(-1, 1))
            except IndexError:
                pass

            # DRAW ENTITIES
            for i in range(len(self.entities) - 1, -1, -1):
                window.addstr(self.entities[i].pos_y, self.entities[i].pos_x, self.entities[i].name[0])

            window.addstr(0, 0, "")

            event = window.getch()

            if event == 27:  # ESC
                whereto = "pause"
                curses.endwin()
                break
            if event == 9:  # TAB
                whereto = "stats"
                curses.endwin()
                break
            if event == curses.KEY_LEFT:
                self.player_move(-1, 0)
            if event == curses.KEY_RIGHT:
                self.player_move(1, 0)
            if event == curses.KEY_DOWN:
                self.player_move(0, 1)
            if event == curses.KEY_UP:
                self.player_move(0, -1)

        if whereto == "pause":
            self.escape_menu()
        elif whereto == "stats":
            self.stats()
        elif whereto == "fight":
            if fight.Manager(0, b, self.entities).fight() == -1:
                self.game_over()
                return
            self.game()

    def escape_menu(self):
        curses.initscr()
        curses.cbreak()
        window = curses.newwin(self.esc_height, self.esc_width, self.height // 6, 10)
        window.keypad(1)
        window.timeout(-1)

        options = ["Exit game",
                   "Main menu",
                   "Continue"]
        heights = [-2, 0, 2, 4]

        cursor_left = ">"
        cursor_right = "<"
        cursor_x_left = cursor_x_right = None
        cursor_y = self.esc_height // 2 + heights[0]

        while True:
            window.clear()
            window.border()

            zipped = zip(options, heights)

            # MENU CHOICES
            for i, j in zipped:
                window.addstr(self.esc_height // 2 - j,
                              self.esc_width // 2 - len(i) // 2,
                              i)

            # SET CURSOR
            if cursor_y == self.esc_height // 2 - heights[0]:
                cursor_x_left = self.esc_width // 2 - len(options[0]) // 2 - 2
                cursor_x_right = self.esc_width // 2 + len(options[0]) // 2 + 2
            elif cursor_y == self.esc_height // 2 - heights[1]:
                cursor_x_left = self.esc_width // 2 - len(options[1]) // 2 - 2
                cursor_x_right = self.esc_width // 2 + len(options[1]) // 2 + 2
            elif cursor_y == self.esc_height // 2 - heights[2]:
                cursor_x_left = self.esc_width // 2 - len(options[2]) // 2 - 2
                cursor_x_right = self.esc_width // 2 + len(options[2]) // 2 + 1

            window.addstr(cursor_y, cursor_x_left, cursor_left)
            window.addstr(cursor_y, cursor_x_right, cursor_right)
            window.addstr(1, 1, "")

            event = window.getch()

            if event == KEY_DOWN and cursor_y < self.esc_height // 2 + heights[-1]:
                cursor_y += 2
            if event == KEY_UP and cursor_y > self.esc_height // 2 + heights[0]:
                cursor_y -= 2
            if event in self.ui.key_enter:
                if cursor_y == self.esc_height // 2 + heights[0]:  # close menu
                    whereto = "close"
                    break
                elif cursor_y == self.esc_height // 2 + heights[1]:  # main menu
                    whereto = "main"
                    break
                elif cursor_y == self.esc_height // 2 + heights[2]:  # exit game
                    whereto = "exit"
                    break
            if event in self.ui.key_back:
                whereto = "close"
                break

        curses.endwin()
        if whereto == "close":
            self.game()
        elif whereto == "main":
            self.start()
        elif whereto == "exit":
            exit()

    def player_move(self, x, y):
        if x == 1 and self.entities[0].pos_x < self.width - 2 \
                or x == -1 and self.entities[0].pos_x > 1:
            self.entities[0].pos_x += x
        if y == 1 and self.entities[0].pos_y < self.height - 2 \
                or y == -1 and self.entities[0].pos_y > 1:
            self.entities[0].pos_y += y

    def move(self, unit, x, y):
        if x == 1 and self.entities[unit].pos_x < self.width - 2 \
                or x == -1 and self.entities[unit].pos_x > 1:
            self.entities[unit].pos_x += x
        elif y == 1 and self.entities[unit].pos_y < self.height - 2 \
                or y == -1 and self.entities[unit].pos_y > 1:
            self.entities[unit].pos_y += y

    def initialize_window(self):
        curses.initscr()
        curses.cbreak()
        window = curses.newwin(self.height, self.width)
        window.keypad(1)
        window.timeout(-1)
        return window

    def stats(self):
        window = self.initialize_window()

        text = "{0}'s characteristics:".format(self.entities[0].name)

        while True:
            window.clear()
            window.border()

            window.addstr(4, 4, text)

            window.addstr(6, 4, "Weapon Skill:             {0}".format(self.entities[0].ww))
            window.addstr(7, 4, "Ballistics Skill:         {0}".format(self.entities[0].us))
            window.addstr(8, 4, "Strength:                 {0}".format(self.entities[0].k))
            window.addstr(9, 4, "Toughness:                {0}".format(self.entities[0].odp))
            window.addstr(10, 4, "Agility:                  {0}".format(self.entities[0].zr))
            window.addstr(11, 4, "Intelligence:             {0}".format(self.entities[0].int))
            window.addstr(12, 4, "Will Power:               {0}".format(self.entities[0].sw))
            window.addstr(13, 4, "Fellowship:               {0}".format(self.entities[0].ogd))

            window.addstr(15, 4, "Attacks:                  {0}".format(self.entities[0].a))
            window.addstr(16, 4, "Wounds (HP):              {0}".format(self.entities[0].zyw))
            window.addstr(17, 4, "Strength Bonus:           {0}".format(self.entities[0].s))
            window.addstr(18, 4, "Toughness Bonus:          {0}".format(self.entities[0].wt))
            window.addstr(19, 4, "Movement:                 {0}".format(self.entities[0].sz))
            window.addstr(20, 4, "Magic:                    {0}".format(self.entities[0].mag))
            window.addstr(21, 4, "Insanity Points:          {0}".format(self.entities[0].po))
            window.addstr(22, 4, "Fate Points (revives):    {0}".format(self.entities[0].pp))

            text = "{0}'s equipment:".format(self.entities[0].name)
            window.addstr(4, self.width // 2, text)

            window.addstr(6, self.width // 2,
                          "Weapon: {0} (Attack bonus: {1})".format(self.entities[0].weapon.name,
                                                                   self.entities[0].weapon.damage))
            window.addstr(8, self.width // 2,
                          "Armour:")
            window.addstr(9, self.width // 2,
                          "Head: {0}, protection: {1}".format(self.entities[0].armor_head.type,
                                                              self.entities[0].armor_head.prot))
            window.addstr(10, self.width // 2,
                          "Body: {0}, protection: {1}".format(self.entities[0].armor_body.type,
                                                              self.entities[0].armor_body.prot))
            window.addstr(11, self.width // 2,
                          "Right arm: {0}, protection: {1}".format(self.entities[0].armor_rhand.type,
                                                                   self.entities[0].armor_rhand.prot))
            window.addstr(12, self.width // 2,
                          "Left arm: {0}, protection: {1}".format(self.entities[0].armor_lhand.type,
                                                                  self.entities[0].armor_lhand.prot))
            window.addstr(13, self.width // 2,
                          "Right leg: {0}, protection: {1}".format(self.entities[0].armor_rleg.type,
                                                                   self.entities[0].armor_rleg.prot))
            window.addstr(14, self.width // 2,
                          "Left leg: {0}, protection: {1}".format(self.entities[0].armor_lleg.type,
                                                                  self.entities[0].armor_lleg.prot))
            window.addstr(16, self.width // 2, "Current experience: {0}".format(self.entities[0].exp_current))
            window.addstr(17, self.width // 2, "Total experience: {0}".format(self.entities[0].exp_cumulative))

            window.addstr(1, 1, "")

            event = window.getch()

            if event != 0:
                curses.endwin()
                break

        self.game()

    @property
    def collide(self):
        x = self.entities[0].pos_x
        y = self.entities[0].pos_y
        for i in range(1, len(self.entities)):
            if x == self.entities[i].pos_x and y == self.entities[i].pos_y:
                return i
        return None

    def game_over(self):
        curses.initscr()
        curses.cbreak()
        window = curses.newwin(self.height // 2, self.width // 2, self.height // 4, self.width // 4)
        window.keypad(1)
        window.timeout(-1)

        while True:
            window.clear()
            window.border()

            text = "You died"
            window.addstr(self.height // 4 - 1, self.width // 4 - len(text) // 2, text)
            text = "Game over"
            window.addstr(self.height // 4 + 1, self.width // 4 - len(text) // 2, text)

            if window.getch():
                return