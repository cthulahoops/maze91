DECLARE SUB rand ()
DECLARE SUB init ()
DECLARE SUB game ()
DECLARE SUB scoreboard ()
DECLARE SUB down ()
DECLARE SUB up ()
DECLARE SUB left ()
DECLARE SUB right ()
DECLARE SUB win ()
DECLARE SUB die ()
DECLARE SUB baddymove ()
DECLARE SUB bdown ()
DECLARE SUB bup ()
DECLARE SUB bleft ()
DECLARE SUB bright ()
DECLARE SUB drawn ()
COMMON SHARED youx, youy, enex, eney, yx, yy, ex, ey, mazeshape() AS STRING * 33 , score, gems
COMMON SHARED wall, you, gem, enemy, dots, d, flag, skill
RANDOMIZE TIMER
SCREEN 7
15 INPUT "Skill level 1-20"; skill: CLS
IF skill < 1 OR skill > 20 THEN GOTO 15
LET skill = 21 - skill
16 INPUT "Maze 1-2"; mazenum: CLS
IF mazenum < 1 AND mazenum > 2 THEN GOTO 16
IF mazenum = 1 THEN RESTORE 11
IF mazenum = 2 THEN RESTORE 12
init
drawn
game
11 DATA "###############################"
DATA "#.....#<..#.#...###############"
DATA "######.###.#.#.#............###"
DATA "#....#...#.#.#.############.###"
DATA "####.###.#.#.#.##........#...##"
DATA "#....#...#...#.<.#.####.###.###"
DATA "#.####.#######.##.#.#...#<...##"
DATA "#.#............##.#.#.####.####"
DATA "#.#.###.###.#.#.#<#.#...<#...##"
DATA "#.#.#......#.#.#.###.########.#"
DATA "#.<.###.###.#.#...............#"
DATA "#.#........#.################.#"
DATA "#...#.#.#.###.#...............#"
DATA "####.#.#.#...#.################"
DATA "#....#.#.#.#.###.#............#"
DATA "#.#<#.#.#.#.#..#<...........#.#"
DATA "#.###.#.#.#.#.###############.#"
DATA "#.....#<#<#<#.................#"
DATA "###############################"
12 DATA "###############################"
DATA "#..................... .......#"
DATA "#.##.####.####.####.######.##.#"
DATA "#.##...................  ..##.#"
DATA "#.....##.#.################<..#"
DATA "#.#.##..#.........<##...###.#.#"
DATA "#.#.<...#.###########.#.#<#.#.#"
DATA "#.#.#...#..........<###.#.#.#.#"
DATA "#.#.#...#.############....#.#.#"
DATA "#...#............#####........#"
DATA "#.#.#...#.############....#.#.#"
DATA "#.#.#...#<.............##.#.#.#"
DATA "#.#.#...################.<#.#.#"
DATA "#.#.##<##................##.#.#"
DATA "#....###..################<...#"
DATA "#.##.......................##.#"
DATA "#.##.####.####.#####..####.##.#"
DATA "#.............................#"
DATA "###############################"

SUB baddymove
LET vert = youy - eney
LET hor = youx - enex
LET upgo = 1
LET downgo = 1
LET leftgo = 1
LET rightgo = 1
IF vert >= 0 THEN upgo = 0
IF vert <= 0 THEN downgo = 0
IF hor >= 0 THEN leftgo = 0
IF hor <= 0 THEN rightgo = 0
d = 0
FOR n = 1 TO 10
flag = 0
LET c = 1 + INT(RND * 4)
SELECT CASE c
CASE 1
    IF downgo = 0 THEN GOTO 1
    d = SCREEN(eney + 1, enex)
    IF d = 219 THEN GOTO 1
    bdown
    flag = 1
    GOTO 5
1 CASE 2
    IF upgo = 0 THEN GOTO 2
    d = SCREEN(eney - 1, enex)
    IF d = 219 THEN GOTO 2
    bup
    flag = 1
    GOTO 5
2 CASE 3
    IF rightgo = 0 THEN GOTO 3
    d = SCREEN(eney, enex + 1)
    IF d = 219 THEN GOTO 3
    bright
    flag = 1
    GOTO 5
3 CASE 4
    IF leftgo = 0 THEN GOTO 5
    d = SCREEN(eney, enex - 1)
    IF d = 219 THEN GOTO 5
    bleft
    flag = 1
    GOTO 5
5 END SELECT
IF flag = 1 THEN EXIT FOR
NEXT n
IF flag = 0 THEN LET d = 0: rand
END SUB

SUB bdown
LET eney = eney + 1
IF d = enemy THEN die
END SUB

SUB bleft
LET enex = enex - 1
IF d = enemy THEN die
END SUB

SUB bright
LET enex = enex + 1
IF d = enemy THEN die
END SUB

SUB bup
LET eney = eney - 1
IF d = enemy THEN die
END SUB

SUB die
FOR n = 1 TO 500: NEXT n
COLOR 15
CLS
LOCATE 11, 1
COLOR 4
PRINT CHR$(enemy)
COLOR 14
LOCATE 11, 2
PRINT CHR$(enemy)
LOCATE 1, 1
COLOR 15
PRINT "He's got you -Shoot him-"
SLEEP
FOR n = 1 TO gems * 10
BEEP
NEXT n
PRINT "Oh no You didn't get all the power gems"
PRINT "Your out of ammo"
PRINT "run"
SLEEP
FOR n = 3 TO 30
LOCATE 11, n - 1
COLOR 4
PRINT CHR$(176);
COLOR 14
PRINT CHR$(enemy)
BEEP
FOR m = 1 TO 50
NEXT m
NEXT n
LOCATE 11, 30
COLOR 4
PRINT CHR$(176)
SLEEP
CLS
COLOR 15
PRINT "He got you"
PRINT "score "; score
PRINT "Gems "; gems
END
END SUB

SUB down
LET p = SCREEN(youy - 1, youx)
IF p = wall THEN EXIT SUB
IF p = gem THEN gems = gems + 1: score = score + 100: IF gems = 10 THEN win
IF p = dots THEN LET score = score + 5
IF p = enemy THEN die
LET youy = youy - 1
END SUB

SUB drawn
FOR n = 1 TO 19
FOR m = 1 TO 33
p$ = MID$(mazeshape(n), m, 1)
LOCATE n + 1, m + 2
SELECT CASE (p$)
CASE "#"
    COLOR 15
    PRINT CHR$(wall);
CASE "."
    COLOR 9
    PRINT CHR$(dots);
CASE "<"
    COLOR 14
    PRINT CHR$(gem);
CASE " "
    COLOR 0
    PRINT " ";
END SELECT
NEXT m
NEXT n
LOCATE yy, yx
PRINT CHR$(you)
LOCATE eney, enex
PRINT CHR$(enemy)
FOR n = 1 TO 50
NEXT n
END SUB

SUB game
DO
scoreboard
ex = enex: ey = eney: yx = youx: yy = youy
LOCATE youy, youx
COLOR 14
print CHR$(enemy);
LOCATE eney, enex
COLOR 4
PRINT CHR$(enemy);
FOR n = 1 TO 50
NEXT n
LET i$ = INKEY$
IF i$ = CHR$(0) + "H" THEN up
IF i$ = CHR$(0) + "P" THEN down
IF i$ = CHR$(0) + "K" THEN left
IF i$ = CHR$(0) + "M" THEN right
c = 1 + INT(RND * skill)
IF c = 1 THEN baddymove ELSE rand
COLOR 15
LOCATE yy, yx
PRINT " ";
LOCATE ey, ex
IF d = gem THEN COLOR 14
if d = dots then color 9
PRINT CHR$(d);
LOOP UNTIL i$ = CHR$(27)
END SUB

SUB init
wall = 219
you = 2
gem = 42
enemy = 1
dots = 249
DIM mazeshape(1 TO 19) AS STRING * 33
FOR n = 1 TO 19
READ mazeshape$(n)
IF LEN(mazeshape$(n)) < 33 THEN PRINT LEN(mazeshape(n))
NEXT n
score = 0
gems = 0
enex = 10
eney = 11
youx = 4
youy = 3
END SUB

SUB left
LET p = SCREEN(youy, youx - 1)
IF p = wall THEN EXIT SUB
IF p = gem THEN gems = gems + 1: score = score + 100: IF gems = 10 THEN win
IF p = dots THEN LET score = score + 5
IF p = enemy THEN die
LET youx = youx - 1
END SUB

SUB rand
LET flag = 0
10 LET c = 1 + INT(RND * 4)
SELECT CASE c
CASE 1
    LET d = SCREEN(eney, enex - 1)
    IF d <> wall THEN bleft
    LET flag = 1
CASE 2
    LET d = SCREEN(eney, enex + 1)
    IF d <> wall THEN bright
    LET flag = 1
CASE 3
    LET d = SCREEN(eney - 1, enex)
    IF d <> wall THEN bup
    LET flag = 1
CASE 4
    LET d = SCREEN(eney + 1, enex)
    IF d <> wall THEN bdown
    LET flag = 1
END SELECT
IF flag = 0 THEN GOTO 10
END SUB

SUB right
LET p = SCREEN(youy, youx + 1)
IF p = wall THEN EXIT SUB
IF p = gem THEN gems = gems + 1: score = score + 100: IF gems = 10 THEN win
IF p = dots THEN LET score = score + 5
IF p = enemy THEN die
LET youx = youx + 1
END SUB

SUB scoreboard
LOCATE 1, 1
PRINT "score: "; score; " ";
LOCATE 1, 20
FOR n = 1 TO gems
print CHR$(gem);
NEXT n
END SUB

SUB up
LET p = SCREEN(youy + 1, youx)
IF p = wall THEN EXIT SUB
IF p = gem THEN gems = gems + 1: score = score + 100: IF gems = 10 THEN win
IF p = dots THEN LET score = score + 5
IF p = enemy THEN die
LET youy = youy + 1
END SUB

SUB win
CLS : COLOR 15
FOR n = 1 TO 500: NEXT n
PRINT "You have all the power gems, after him"
SLEEP
FOR n = 1 TO 37
LOCATE 11, n
COLOR 14
PRINT " "; CHR$(enemy);
COLOR 4
PRINT CHR$(176) + CHR$(enemy);
BEEP
FOR m = 1 TO 50
NEXT m
NEXT n
LOCATE 11, 40
PRINT CHR$(176)
' SOUND 10000, 18
CLS
COLOR 15
PRINT "The world is safe, you are a hero"
PRINT "and I'm Lawrence of Arabia!"
PRINT "The world is never safe!"
PRINT "and my granddad was more of a hero than you!"
END SUB
