from __future__ import print_function
import numpy as np
from copy import deepcopy
from collections import defaultdict

from util import log

DEBUG = False


def load_input(fn):
    with open(fn, 'r') as fp:
        path1 = fp.readline().strip().split(',')
        path2 = fp.readline().strip().split(',')
    return path1, path2


class Move(object):

    def __init__(self, move):
        '''eg: U123'''
        self.move = move
        self.direction = move[0]
        self.distance = int(move[1:])

    def __str__(self):
        return self.move


class Wire(object):

    def __init__(self, pos_x=0, pos_y=0):
        self.pos_x = 0
        self.pos_y = 0
        self.n_steps = 0
        self.pos_history = defaultdict(list)

    def __move(self, dx, dy):
        '''d should be 1 or -1'''
        self.pos_x += dx
        self.pos_y += dy
        self.n_steps += 1
        self.pos_history[str(self)].append(self.n_steps)

    def move(self, move):
        '''eg: U123'''
        if move.direction == 'L':
            for i in range(move.distance):
                self.__move(-1, 0)
        elif move.direction == 'R':
            for i in range(move.distance):
                self.__move(1, 0)
        elif move.direction == 'U':
            for i in range(move.distance):
                self.__move(0, 1)
        else:
            # move.direction == 'D'
            for i in range(move.distance):
                self.__move(0, -1)

    def intersect(self, other):
        point = set(self.pos_history.keys()) & set(other.pos_history.keys())
        return point

    def first_arrival_at(self, point):
        return self.pos_history[point][0]

    def __str__(self):
        return '%d,%d' % (self.pos_x, self.pos_y)


def part1(paths):
    wires = [Wire(), Wire()]
    path1 = map(Move, paths[0])
    path2 = map(Move, paths[1])
    for move1, move2 in zip(path1, path2):
        if DEBUG:
            print('---------------------')
            print('A moves {}'.format(move1))
            print('B moves {}'.format(move2))

        wires[0].move(move1)
        wires[1].move(move2)

    intersections = set(wires[0].pos_history.keys()) & set(wires[1].pos_history.keys())
    if len(intersections) == 0:
        raise ValueError('Did not find any intersections')

    distances = []
    for point in wires[0].intersect(wires[1]):
        pos = list(map(int, point.split(',')))
        distances.append(int(np.linalg.norm(pos, ord=1)))

    return np.min(distances)


def part2(paths):
    wires = [Wire(), Wire()]
    path1 = map(Move, paths[0])
    path2 = map(Move, paths[1])
    for move1, move2 in zip(path1, path2):
        wires[0].move(move1)
        wires[1].move(move2)

    distances = []
    for point in wires[0].intersect(wires[1]):
        distances.append(wires[0].first_arrival_at(point) + wires[1].first_arrival_at(point))

    return np.min(distances)


if __name__ == '__main__':
    print(part1(load_input('../res/d3.txt')))
    print(part2(load_input('../res/d3.txt')))
