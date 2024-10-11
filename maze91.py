import random
import time
import sys
import os

# ANSI escape sequences
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# Color codes
WHITE = "\033[97m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Game characters
WALL = '#'
YOU = '☺'
GEM = '<'
ENEMY = '☻'
DOTS = '·'

# Global variables
youx, youy, enex, eney = 0, 0, 0, 0
score, gems = 0, 0
mazeshape = []
skill = 0

def locate(row, col):
    print(f"\033[{row};{col}H", end='')

def cls():
    print(CLEAR_SCREEN + CURSOR_HOME, end='')

def rand():
    global enex, eney, d
    flag = 0
    while flag == 0:
        c = random.randint(1, 4)
        if c == 1 and get_screen(eney, enex - 1) != WALL:
            bleft()
            flag = 1
        elif c == 2 and get_screen(eney, enex + 1) != WALL:
            bright()
            flag = 1
        elif c == 3 and get_screen(eney - 1, enex) != WALL:
            bup()
            flag = 1
        elif c == 4 and get_screen(eney + 1, enex) != WALL:
            bdown()
            flag = 1

def init():
    global wall, you, gem, enemy, dots, mazeshape, score, gems, enex, eney, youx, youy, skill
    wall, you, gem, enemy, dots = WALL, YOU, GEM, ENEMY, DOTS
    score, gems = 0, 0
    enex, eney, youx, youy = 10, 11, 4, 3

    maze1 = [
        "###############################",
        "#......#<..#.....##############",
        "######.###.#.#.#............###",
        "#....#...#.#.#.############.###",
        "####.###.#.#.#.##........#...##",
        "#....#...#...#.<.#.####.###.###",
        "#.####.#######.##.#.#...#<...##",
        "#.#............##.#.#.####.####",
        "#.#.###.###.#.#.#<#.#...<#....#",
        "#.#.#.......#.#.#.###.#######.#",
        "#.<.###.###.#.#...............#",
        "#.#.........#.###############.#",
        "#...#.#.#.#.#.................#",
        "#####.#.#.#.#.#################",
        "#.....#.#.#.#.#...............#",
        "#.#<#.#.#.#.#.#<............#.#",
        "#.###.#.#.#.#.###############.#",
        "#.....#<#<#<#.................#",
        "###############################"
    ]

    maze2 = [
        "###############################",
        "#..................... .......#",
        "#.##.####.####.####.######.##.#",
        "#.##...................  ..##.#",
        "#.....##.#.################<..#",
        "#.#.##..#.........<##...###.#.#",
        "#.#.<...#.###########.#.#<#.#.#",
        "#.#.#...#..........<###.#.#.#.#",
        "#.#.#...#.############....#.#.#",
        "#...#............#####........#",
        "#.#.#...#.############....#.#.#",
        "#.#.#...#<.............##.#.#.#",
        "#.#.#...################.<#.#.#",
        "#.#.##<##................##.#.#",
        "#....###..################<...#",
        "#.##.......................##.#",
        "#.##.####.####.#####..####.##.#",
        "#.............................#",
        "###############################"
    ]

    mazenum = int(input("Maze 1-2: "))
    cls()
    if mazenum == 1:
        mazeshape = maze1
    elif mazenum == 2:
        mazeshape = maze2
    else:
        print("Invalid maze number. Exiting.")
        sys.exit()

    skill = int(input("Skill level 1-20: "))
    cls()
    if skill < 1 or skill > 20:
        print("Invalid skill level. Exiting.")
        sys.exit()
    skill = 21 - skill

def drawn():
    for n, row in enumerate(mazeshape):
        locate(n + 2, 3)
        for char in row:
            if char == '#':
                print(WHITE + WALL + RESET, end='')
            elif char == '.':
                print(BLUE + DOTS + RESET, end='')
            elif char == '<':
                print(YELLOW + GEM + RESET, end='')
            elif char == ' ':
                print(' ', end='')
    locate(youy, youx)
    print(YELLOW + YOU + RESET, end='')
    locate(eney, enex)
    print(RED + ENEMY + RESET, end='')
    sys.stdout.flush()
    time.sleep(0.05)

def get_screen(y, x):
    return mazeshape[y-2][x-3]

def set_screen(y, x, char):
    row = list(mazeshape[y - 2])
    row[x - 3] = char
    mazeshape[y - 2] = ''.join(row)

def game():
    global youx, youy, enex, eney, score, gems
    while True:
        scoreboard()
        ex, ey, yx, yy = enex, eney, youx, youy
        locate(eney, enex)
        print(RED + ENEMY + RESET, end='')
        locate(youy, youx)
        print(YELLOW + YOU + RESET, end='')
        sys.stdout.flush()
        time.sleep(0.05)

        if sys.stdin.read(1) == '\x1b':
            if sys.stdin.read(1) == '[':
                key = sys.stdin.read(1)
                if key == 'B':
                    up()
                elif key == 'A':
                    down()
                elif key == 'D':
                    left()
                elif key == 'C':
                    right()

        if random.randint(1, skill) == 1:
            baddymove()
        else:
            rand()

        locate(yy, yx)
        print(' ', end='')
        locate(ey, ex)
        d = get_screen(ey, ex)
        if d == GEM:
            print(YELLOW + d + RESET, end='')
        elif d == DOTS:
            print(BLUE + d + RESET, end='')
        else:
            print(d, end='')
        sys.stdout.flush()

def scoreboard():
    locate(1, 1)
    print(f"Score: {score} ", end='')
    locate(1, 20)
    print(YELLOW + GEM * gems + RESET, end='')
    sys.stdout.flush()

def up():
    global youy, gems, score
    p = get_screen(youy + 1, youx)
    if p != WALL:
        if p == GEM:
            gems += 1
            score += 100
            if gems == 10:
                win()
        elif p == DOTS:
            score += 5
        elif p == ENEMY:
            die()
        youy += 1

def down():
    global youy, gems, score
    p = get_screen(youy - 1, youx)
    if p != WALL:
        if p == GEM:
            gems += 1
            score += 100
            if gems == 10:
                win()
        elif p == DOTS:
            score += 5
        elif p == ENEMY:
            die()
        youy -= 1

def left():
    global youx, gems, score
    p = get_screen(youy, youx - 1)
    if p != WALL:
        if p == GEM:
            gems += 1
            score += 100
            if gems == 10:
                win()
        elif p == DOTS:
            score += 5
        elif p == ENEMY:
            die()
        youx -= 1

def right():
    global youx, gems, score
    p = get_screen(youy, youx + 1)
    if p != WALL:
        if p == GEM:
            gems += 1
            score += 100
            if gems == 10:
                win()
        elif p == DOTS:
            score += 5
        elif p == ENEMY:
            die()
        youx += 1

def baddymove():
    global enex, eney
    vert = youy - eney
    hor = youx - enex
    upgo = 1 if vert < 0 else 0
    downgo = 1 if vert > 0 else 0
    leftgo = 1 if hor < 0 else 0
    rightgo = 1 if hor > 0 else 0

    for _ in range(10):
        c = random.randint(1, 4)
        if c == 1 and downgo and get_screen(eney + 1, enex) != WALL:
            bdown()
            return
        elif c == 2 and upgo and get_screen(eney - 1, enex) != WALL:
            bup()
            return
        elif c == 3 and rightgo and get_screen(eney, enex + 1) != WALL:
            bright()
            return
        elif c == 4 and leftgo and get_screen(eney, enex - 1) != WALL:
            bleft()
            return
    rand()

def bdown():
    global eney
    eney += 1
    if get_screen(eney, enex) == ENEMY:
        die()

def bup():
    global eney
    eney -= 1
    if get_screen(eney, enex) == ENEMY:
        die()

def bleft():
    global enex
    enex -= 1
    if get_screen(eney, enex) == ENEMY:
        die()

def bright():
    global enex
    enex += 1
    if get_screen(eney, enex) == ENEMY:
        die()

def die():
    time.sleep(0.5)
    cls()
    locate(11, 1)
    print(RED + ENEMY + RESET, end='')
    locate(11, 2)
    print(YELLOW + ENEMY + RESET, end='')
    locate(1, 1)
    print(WHITE + "He's got you -Shoot him-" + RESET)
    time.sleep(1)
    for _ in range(gems * 10):
        print('\a', end='')
        sys.stdout.flush()
    print("Oh no You didn't get all the power gems")
    print("Your out of ammo")
    print("run")
    time.sleep(1)
    for n in range(3, 31):
        locate(11, n - 1)
        print(RED + '░' + RESET, end='')
        print(YELLOW + ENEMY + RESET, end='')
        print('\a', end='')
        sys.stdout.flush()
        time.sleep(0.05)
    locate(11, 30)
    print(RED + '░' + RESET, end='')
    time.sleep(1)
    cls()
    print(WHITE + f"He got you\nScore: {score}\nGems: {gems}" + RESET)
    sys.exit()

def win():
    cls()
    time.sleep(0.5)
    print(WHITE + "You have all the power gems, after him" + RESET)
    time.sleep(1)
    for n in range(1, 38):
        locate(11, n)
        print(YELLOW + ' ' + ENEMY + RESET, end='')
        print(RED + '░' + ENEMY + RESET, end='')
        print('\a', end='')
        sys.stdout.flush()
        time.sleep(0.05)
    locate(11, 40)
    print('░', end='')
    cls()
    print(WHITE + "The world is safe, you are a hero")
    print("and I'm Lawrence of Arabia!")
    print("The world is never safe!")
    print("and my granny was more of a hero than you!" + RESET)
    sys.exit()

if __name__ == "__main__":
    print(HIDE_CURSOR, end='')
    import termios
    import tty
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        random.seed(time.time())
        init()
        tty.setcbreak(sys.stdin.fileno())
        drawn()
        game()
    finally:
        print(SHOW_CURSOR, end='')
        sys.stdout.flush()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
