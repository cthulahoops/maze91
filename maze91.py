import random
import time
import sys
import os

from qb import Screen, WHITE, BLUE, YELLOW, RED, RESET, get_key, SHOW_CURSOR

screen = Screen(80, 25)

# Game constants
WALL = '█'
YOU = '☺'
GEM = '*'
ENEMY = '☻'
DOTS = '·'

# Global variables
youx, youy, enex, eney = 0, 0, 0, 0
score, gems = 0, 0
mazeshape = []
skill = 0

def cls():
    screen.clear()

def init():
    global wall, you, gem, enemy, dots, mazeshape, score, gems, enex, eney, youx, youy, skill
    wall, you, gem, enemy, dots = WALL, YOU, GEM, ENEMY, DOTS
    score, gems = 0, 0
    enex, eney, youx, youy = 10, 11, 4, 3

    maze1 = [
        "###############################",
        "#......#<..#.#...##############",
        "######.###.#.#.#............###",
        "#......#...#.#.############.###",
        "####.###.#.#.#.##.......#.....#",
        "#........#...#.#<.#.###.###.###",
        "#.####.#######.##.#.#...#<....#",
        "#.#.............#.#.#.#####.###",
        "#.#.###.###.#.#.#<#.#..<#.....#",
        "#.#.#.....#.#.#.###.#######.###",
        "#.#.###.###.#.#...............#",
        "#.#.........#.###############.#",
        "#...#.#.#.###.#...............#",
        "#####.#.#.#...#.###############",
        "#...#.#.#.#.###.#.............#",
        "#.#<#.#.#.#.#...#<..........#.#",
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
        screen.locate(n + 2, 3)
        for char in row:
            if char == '#':
                screen.color(WHITE)
                screen.write(WALL)
            elif char == '.':
                screen.color(BLUE)
                screen.write(DOTS)
            elif char == '<':
                screen.color(YELLOW)
                screen.write(GEM)
            elif char == ' ':
                screen.write(' ')
    screen.locate(youy, youx)
    screen.color(YELLOW)
    screen.write(YOU)
    screen.locate(eney, enex)
    screen.color(RED)
    screen.write(ENEMY)
    time.sleep(0.05)

def game():
    global youx, youy, enex, eney, score, gems
    while True:
        scoreboard()
        ex, ey, yx, yy = enex, eney, youx, youy
        screen.locate(youy, youx)
        screen.color(YELLOW)
        screen.write(YOU)
        screen.locate(eney, enex)
        screen.color(RED)
        screen.write(ENEMY)
        time.sleep(0.05)

        key = get_key()
        if key == 'UP':
            up()
        elif key == 'DOWN':
            down()
        elif key == 'LEFT':
            left()
        elif key == 'RIGHT':
            right()
        elif key == 'ESC':
            break

        if random.randint(1, skill) == 1:
            baddymove()
        else:
            rand()

        screen.locate(yy, yx)
        screen.write(' ')
        screen.locate(ey, ex)
        d = mazeshape[ey - 2][ex - 3]
        if d == "<":
            screen.color(YELLOW)
            screen.write(GEM)
        elif d == ".":
            screen.color(BLUE)
            screen.write(DOTS)
        else:
            screen.write(d)

def rand():
    global enex, eney, d
    flag = 0
    while flag == 0:
        c = random.randint(1, 4)
        if c == 1 and screen.get(eney, enex - 1) != WALL:
            bleft()
            flag = 1
        elif c == 2 and screen.get(eney, enex + 1) != WALL:
            bright()
            flag = 1
        elif c == 3 and screen.get(eney - 1, enex) != WALL:
            bup()
            flag = 1
        elif c == 4 and screen.get(eney + 1, enex) != WALL:
            bdown()
            flag = 1


def scoreboard():
    screen.locate(1, 1)
    screen.color(WHITE)
    screen.write(f"Score: {score} ")
    screen.locate(1, 20)
    screen.color(YELLOW)
    screen.write(GEM * gems)

def up():
    global youy, gems, score
    p = screen.get(youy + 1, youx)
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
    p = screen.get(youy - 1, youx)
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
    p = screen.get(youy, youx - 1)
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
    p = screen.get(youy, youx + 1)
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
        if c == 1 and downgo and screen.get(eney + 1, enex) != WALL:
            bdown()
            return
        elif c == 2 and upgo and screen.get(eney - 1, enex) != WALL:
            bup()
            return
        elif c == 3 and rightgo and screen.get(eney, enex + 1) != WALL:
            bright()
            return
        elif c == 4 and leftgo and screen.get(eney, enex - 1) != WALL:
            bleft()
            return
    rand()

def bdown():
    global eney
    eney += 1
    if screen.get(eney, enex) == YOU:
        die()

def bup():
    global eney
    eney -= 1
    if screen.get(eney, enex) == YOU:
        die()

def bleft():
    global enex
    enex -= 1
    if screen.get(eney, enex) == YOU:
        die()

def bright():
    global enex
    enex += 1
    if screen.get(eney, enex) == YOU:
        die()

def die():
    time.sleep(0.5)
    screen.clear()
    screen.locate(11, 1)
    screen.color(RED)
    screen.write(ENEMY)
    screen.locate(11, 2)
    screen.color(YELLOW)
    screen.write(YOU)
    screen.locate(1, 1)
    screen.color(WHITE)
    screen.write("He's got you -Shoot him-")
    time.sleep(1)
    for _ in range(gems * 10):
        print('\a', end='')
        sys.stdout.flush()
    screen.write("\nOh no You didn't get all the power gems")
    screen.write("\nYour out of ammo")
    screen.write("\nrun")
    time.sleep(1)
    for n in range(3, 31):
        screen.locate(11, n - 1)
        screen.color(WHITE)
        screen.write(' ')
        screen.color(YELLOW)
        screen.write(YOU)
        sys.stdout.flush()
        time.sleep(0.05)
    screen.locate(11, 30)
    screen.color(RED)
    screen.write('░')
    time.sleep(1)
    screen.clear()
    screen.color(WHITE)
    screen.write(f"He got you\nScore: {score}\nGems: {gems}")
    sys.exit()

def win():
    cls()
    time.sleep(0.5)
    screen.color(WHITE)
    screen.write("You got all the power gems, after him")
    time.sleep(1)
    for n in range(1, 38):
        screen.locate(11, n)
        screen.write(" ")
        screen.color(YELLOW)
        screen.write(YOU)
        screen.color(RED)
        screen.write(ENEMY)
        sys.stdout.flush()
        time.sleep(0.05)
    screen.locate(11, 40)
    screen.write('░')
    cls()
    print("The world is safe, you are a hero")
    print("and I'm Lawrence of Arabia!")
    print("The world is never safe!")
    print("and my granny was more of a hero than you!")
    sys.exit()

if __name__ == "__main__":
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
