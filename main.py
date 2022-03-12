#!/usr/bin/env python3
import os
from sys import stderr
os.system('setfont Lat15-TerminusBold14')
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor import INPUT_2

from way import shortest_way

from time import sleep
from sys import stderr

lm = LargeMotor(OUTPUT_B)     # левый мотор   # 
rm = LargeMotor(OUTPUT_C)     # правый мотор  #
c1 = ColorSensor(INPUT_1)     # color sensor  #  !!!!!!!!!!!!!!!!!!
c2 = ColorSensor(INPUT_2)
robot = MoveTank(OUTPUT_B, OUTPUT_C)    # для движения "танком" #
sound = Sound()
kp = 0.2
w = 80
target = []


def line(sp0):
    global kp
    err = c1.reflected_light_intensity - c2.reflected_light_intensity
    spb = sp0 + err*kp
    spc = sp0 + err*kp
    robot.on(spb, spc)
    sleep(0.002)


def line2(sp0):
    err = 40 - c2.reflected_light_intensity
    spb = sp0 + err*0.4
    spc = sp0
    robot.on(spb, spc)
    sleep(0.001)

def move_to_line(sp0):
    while c1.reflected_light_intensity > 10:
        line2(20)
    robot.on_for_rotations(sp0, sp0, 0.24)
    robot.off()

    
def start_decode():
    global target
    robot.on_for_rotations(20, 20, 0.35)
    robot.on(20, 20)
    while int(c1.reflected_light_intensity) > 15:
        sleep(0.001)
    lm.position = 0
    robot.on(30, 30)
    while int(c1.reflected_light_intensity) < 60:
        sleep(0.001)
    bend = int(lm.position)
    print(bend*3.14*56/360, file=stderr)
    data=[]
    while int(lm.position) < bend*10:
        data.append(int(c1.reflected_light_intensity))
    print(data, file=stderr)
    robot.on_for_rotations(20, 20, 0.8)
    robot.off()

    a = len(data)
    b = a / 9
    r = 35
    sps = []
    for i in range(9):
        n=data[int(b/2+b*i)]
        if n<r:
            sps.append(1)
        else:
            sps.append(0)
    print(sps, file=stderr)
    sps.reverse()
    print(sps, file=stderr)
    data = sps[:-2]
    print(data, file=stderr)

    cd = "".join([str(i) for i in data])
    coord = int(cd, 2)
    print(coord, file=stderr)
    
    target = (coord // 10, coord % 10)
    print(target, file=stderr)


def rotate(a, b):
    c = a - b
    kf = c // 90
    robot.on_for_degrees(20, -20, -180*kf)


def point():
    global startt
    global start2
    global test
    for i in test:
        lx = startt[0] - i[0]
        ly = startt[1] - i[1]
        if lx > 0:
            la = 180
        elif lx < 0:
            la = 0
        elif ly < 0:
            la = 90
        elif ly > 0:
            la = -90
        rotate(startt[2], la)
        move_to_line(20)
        startt = [i[0], i[1], la]

def finishh():
    global startt
    if startt[1] > 3:
        rotate(startt[2], -90)
        for i in range(3 - startt[1]):
            move_to_line(30)
        rotate(-90, 180)
        for i in range(startt[0]-1):
            move_to_line(20)
    elif startt[1] < 3:
        rotate(startt[2], 90)
        for i in range(3 - startt[1]):
            move_to_line(30)
        rotate(90, 180)
        for i in range(startt[0]-1):
            move_to_line(20)
    else:
        rotate(startt[2], 180)
        for i in range(startt[0]-1):
            move_to_line(30)
    robot.on_for_rotations(30, 30, 3.6)


start2 = 0
start_decode()



alphabet = {'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ж': 7}
f = open('data.txt', 'r', encoding='utf-8')
e = eval(f.read())
f.close()
edges = []
for coord in e:
    a = alphabet[coord[0][0]], int(coord[0][1])
    b = alphabet[coord[1][0]], int(coord[1][1])
    edges.append([a, b, int(coord[2])])

startt = [1, 3, 0]
way = shortest_way(edges, (1, 3), target)
test = way[1:]
# test = [(2, 3), (3, 3), (4, 3), (4, 2), (5, 2), (6, 2), (7, 2)]

point()
start2 = startt
finishh()