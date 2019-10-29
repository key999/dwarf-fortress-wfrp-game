import object
import dice
from os import system
from sys import platform


def clear_screen():
    system("cls") if "win" in platform.lower() else system("clear")


def file_len(file):
    with open(file, "r") as f:
        for i, l in enumerate(f):
            pass
    return (i + 1)


class Creator:
    human_names_male = {1: "Adelbert", 2: "Albrecht", 3: "Berthold", 4: "Dieter", 5: "Eckhardt", 6: "Felix",
                        7: "Gottfried", 8: "Gustav", 9: "Heinz", 10: "Johann", 11: "Konrad", 12: "Leopold",
                        13: "Magnus", 14: "Otto", 15: "Pieter", 16: "Rudiger", 17: "Siegfried", 18: "Ulrich",
                        19: "Waldemar", 20: "Wolfgang"}
    human_names_female = {1: "Alexa", 2: "Alfrida", 3: "Beatrix", 4: "Bianka", 5: "Carlott", 6: "Elfrida", 7: "Elise",
                          8: "Gabrielle", 9: "Gretchen", 10: "Hanna", 11: "Ilsa", 12: "Klara", 13: "Jarla",
                          14: "Ludmilla", 15: "Mathilde", 16: "Regina", 17: "Solveig", 18: "Theodora", 19: "Ulrike",
                          20: "Wertha"}
    human_health = {1: 10, 2: 10, 3: 10, 4: 11, 5: 11, 6: 11, 7: 12, 8: 12, 9: 12, 10: 13}
    human_revive = {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 3}

    dwarf_names_male = {1: "Bardin", 2: "Brokk", 3: "Dimzad", 4: "Durak", 5: "Garil", 6: "Gottri", 7: "Grundi",
                        8: "Hargin", 9: "Imrak", 10: "Kargun", 11: "Jotunn", 12: "Magnar", 13: "Mordrin", 14: "Nargond",
                        15: "Orzad", 16: "Ragnar", 17: "Snorri", 18: "Storri", 19: "Thingrim", 20: "Urgrim"}
    dwarf_names_female = {1: "Anika", 2: "Asta", 3: "Astrid", 4: "Berta", 5: "Birgit", 6: "Dagmar", 7: "Elsa",
                          8: "Erika", 9: "Franziska", 10: "Greta", 11: "Hunni", 12: "Ingrid", 13: "Janna", 14: "Karin",
                          15: "Petra", 16: "Sigrid", 17: "Sigrun", 18: "Silma", 19: "Thylda", 20: "Ulla"}
    dwarf_health = {1: 11, 2: 11, 3: 11, 4: 12, 5: 12, 6: 12, 7: 13, 8: 13, 9: 13, 10: 14}
    dwarf_revive = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3, 10: 3}

    elf_names_male = {1: "Aluthol", 2: "Amendil", 3: "Angran", 4: "Cavindel", 5: "Dolwen", 6: "Eldillor", 7: "Falandar",
                      8: "Farnoth", 9: "Gildiril", 10: "Harrond", 11: "Imhol", 12: "Larandar", 13: "Laurenor",
                      14: "Mellion", 15: "Mormacar", 16: "Ravandil", 17: "Torendil", 18: "Urdithane", 19: "Valahuir",
                      20: "Yavandir"}
    elf_names_female = {1: "Alane", 2: "Altronia", 3: "Davandrel", 4: "Eldril", 5: "Eponia", 6: "Fanriel", 7: "Filamir",
                        8: "Gallina", 9: "Halion", 10: "Iludil", 11: "Ionor", 12: "Lindara", 13: "Lorandara",
                        14: "Maruviel", 15: "Pelgrana", 16: "Siluvaine", 17: "Tallana", 18: "Ulliana", 19: "Vivandrel",
                        20: "Yuviel"}
    elf_health = {1: 9, 2: 9, 3: 9, 4: 10, 5: 10, 6: 10, 7: 11, 8: 11, 9: 11, 10: 12}
    elf_revive = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2}

    halfling_names_male = {1: "Adam", 2: "Albert", 3: "Alfred", 4: "Axel", 5: "Carl", 6: "Edgar", 7: "Hugo", 8: "Jakob",
                           9: "Ludo", 10: "Max", 11: "Niklaus", 12: "Oskar", 13: "Paul", 14: "Ralf", 15: "Rudi",
                           16: "Theo", 17: "Thomas", 18: "Udo", 19: "Viktor", 20: "Walter"}
    halfling_names_female = {1: "Agnes", 2: "Alice", 3: "Elena", 4: "Eva", 5: "Frida", 6: "Greta", 7: "Hanna",
                             8: "Heidi", 9: "Hilda", 10: "Janna", 11: "Karin", 12: "Leni", 13: "Marie", 14: "Petra",
                             15: "Silma", 16: "Sophia", 17: "Susi", 18: "Theda", 19: "Ulla", 20: "Wanda"}
    halfling_health = {1: 8, 2: 8, 3: 8, 4: 9, 5: 9, 6: 9, 7: 11, 8: 11, 9: 11, 10: 12}
    halfling_revive = {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3, 10: 3}

    def create(self, race, sex):
        character = object.Player()
        character.race = race
        character.sex = sex
        # self.import_names()

        # STAT GEN
        # HUMAN
        if character.race == "human":
            if character.sex == "male":
                character.name = self.human_names_male[dice.toss(len(self.human_names_male))]
            elif character.sex == "female":
                character.name = self.human_names_female[dice.toss(len(self.human_names_female))]
            character.ww = 20 + dice.toss(10) + dice.toss(10)
            character.us = 20 + dice.toss(10) + dice.toss(10)
            character.k = 20 + dice.toss(10) + dice.toss(10)
            character.odp = 20 + dice.toss(10) + dice.toss(10)
            character.zr = 20 + dice.toss(10) + dice.toss(10)
            character.ogd = 20 + dice.toss(10) + dice.toss(10)
            character.zyw = self.human_health[dice.toss(10)]
            character.sz = 4
            character.pp = self.human_revive[dice.toss(10)]

        # DWARF
        if character.race == "dwarf":
            if character.sex == "male":
                character.name = self.dwarf_names_male[dice.toss(len(self.dwarf_names_male))]
            elif character.sex == "female":
                character.name = self.dwarf_names_female[dice.toss(len(self.dwarf_names_female))]
            character.ww = 30 + dice.toss(10) + dice.toss(10)
            character.us = 20 + dice.toss(10) + dice.toss(10)
            character.k = 20 + dice.toss(10) + dice.toss(10)
            character.odp = 30 + dice.toss(10) + dice.toss(10)
            character.zr = 10 + dice.toss(10) + dice.toss(10)
            character.ogd = 10 + dice.toss(10) + dice.toss(10)
            character.zyw = self.dwarf_health[dice.toss(10)]
            character.sz = 3
            character.pp = self.dwarf_revive[dice.toss(10)]

        # ELF
        if character.race == "elf":
            if character.sex == "male":
                character.name = self.elf_names_male[dice.toss(len(self.elf_names_male))]
            elif character.sex == "female":
                character.name = self.elf_names_female[dice.toss(len(self.elf_names_female))]
            character.ww = 20 + dice.toss(10) + dice.toss(10)
            character.us = 30 + dice.toss(10) + dice.toss(10)
            character.k = 20 + dice.toss(10) + dice.toss(10)
            character.odp = 20 + dice.toss(10) + dice.toss(10)
            character.zr = 30 + dice.toss(10) + dice.toss(10)
            character.ogd = 20 + dice.toss(10) + dice.toss(10)
            character.zyw = self.elf_health[dice.toss(10)]
            character.sz = 5
            character.pp = self.elf_revive[dice.toss(10)]

        # HALFLING
        if character.race == "halfling":
            if character.sex == "male":
                character.name = self.halfling_names_male[dice.toss(len(self.halfling_names_male))]
            elif character.sex == "female":
                character.name = self.halfling_names_female[dice.toss(len(self.halfling_names_female))]
            character.ww = 10 + dice.toss(10) + dice.toss(10)
            character.us = 30 + dice.toss(10) + dice.toss(10)
            character.k = 10 + dice.toss(10) + dice.toss(10)
            character.odp = 10 + dice.toss(10) + dice.toss(10)
            character.zr = 30 + dice.toss(10) + dice.toss(10)
            character.ogd = 30 + dice.toss(10) + dice.toss(10)
            character.zyw = self.halfling_health[dice.toss(10)]
            character.sz = 4
            character.pp = self.halfling_revive[dice.toss(10)]

        # COMMON STATS
        character.mag = 0
        character.po = 0
        character.int = 20 + dice.toss(10) + dice.toss(10)
        character.sw = 20 + dice.toss(10) + dice.toss(10)
        character.a = 1
        character.s = character.k // 10
        character.wt = character.odp // 10

        character.weapon = object.Weapon("Onehanded", "Shortsword")
        character.armor_head = object.Armor("Plate")
        character.armor_body = object.Armor("Chain")
        character.armor_rhand = object.Armor("Cloth")
        character.armor_lhand = object.Armor("Cloth")
        character.armor_rleg = object.Armor("Cloth")
        character.armor_lleg = object.Armor("Cloth")


        character.name = character.name[:len(character.name)]
        return character

    def import_names(self):
        hm = "names/human_male.cfg"
        hf = "names/human_female.cfg"
        dm = "names/dwarf_male.cfg"
        df = "names/dwarf_female.cfg"
        em = "names/elf_male.cfg"
        ef = "names/elf_female.cfg"
        lm = "names/halfling_male.cfg"
        lf = "names/halfling_female.cfg"

        # HUMAN
        try:
            with open(hm, "r") as f:
                for i in range(file_len(hm)):
                    x = f.readline()
                    if x != "\n":
                        self.human_names_male[i] = x
        except FileNotFoundError:
            print("brak pliku", hm)
        try:
            with open(hf, "r") as f:
                for i in range(file_len(hf)):
                    x = f.readline()
                    if x != "\n":
                        self.human_names_female[i] = x
        except FileNotFoundError:
            print("brak pliku", hf)

        # DWARF
        try:
            with open(dm, "r") as f:
                for i in range(file_len(dm)):
                    x = f.readline()
                    if x != "\n":
                        self.dwarf_names_male[i] = x
        except FileNotFoundError:
            print("brak pliku", dm)
        try:
            with open(df, "r") as f:
                for i in range(file_len(df)):
                    x = f.readline()
                    if x != "\n":
                        self.dwarf_names_female[i] = x
        except FileNotFoundError:
            print("brak pliku", df)

        # ELF
        try:
            with open(em, "r") as f:
                for i in range(file_len(em)):
                    x = f.readline()
                    if x != "\n":
                        self.elf_names_male[i] = x
        except FileNotFoundError:
            print("brak pliku", em)
        try:
            with open(ef, "r") as f:
                for i in range(file_len(ef)):
                    x = f.readline()
                    if x != "\n":
                        self.elf_names_female[i] = x
        except FileNotFoundError:
            print("brak pliku", ef)

        # HALFLING
        try:
            with open(lm, "r") as f:
                for i in range(file_len(lm)):
                    x = f.readline()
                    if x != "\n":
                        self.halfling_names_male[i] = x
        except FileNotFoundError:
            print("brak pliku", lm)
        try:
            with open(lf, "r") as f:
                for i in range(file_len(lf)):
                    x = f.readline()
                    if x != "\n":
                        self.halfling_names_female[i] = x
        except FileNotFoundError:
            print("brak pliku", lf)

        print()
