from __future__ import print_function
from copy import deepcopy

from util import log


fn = "../res/d2.txt"


class Intcode(object):

    def __init__(self, command):
        self.opcode, self.idx1, self.idx2, self.idx_dst = command
        if self.opcode not in [1, 2]:
            raise ValueError('Bad opcode')

    def forward(self, codes):
        if self.opcode == 1:
            codes[self.idx_dst] = codes[self.idx1] + codes[self.idx2]
        elif self.opcode == 2:
            codes[self.idx_dst] = codes[self.idx1] * codes[self.idx2]
        else:
            raise ValueError('wat')
        return codes

    def __str__(self):
        op = '+' if self.opcode == 1 else '*'
        return "codes[%d] = codes[%d] %s codes[%d]" % (self.idx_dst, self.idx1, op, self.idx2)

    def backward(self, codes, previous_commands):
        idx_change = None
        idx_static = None
        for i in range(len(previous_commands) - 1):
            command = previous_commands[-(i + 1)]
            if self.idx1 == command.idx_dst:
                idx_change = self.idx1
                idx_static = self.idx2
            elif self.idx2 == command.idx_dst:
                idx_change = self.idx2
                idx_static = self.idx1

        if idx_change is None:
            print(self, "No change necessary")
        else:
            op = '-' if self.opcode == 1 else '/'
            # print(str(self), "->", "codes[%d] = codes[%d] %s codes[%d]" % (idx_change, self.idx_dst, op, idx_static))
            if self.opcode == 1:
                # inverse of codes[self.idx_dst] = codes[self.idx1] + codes[self.idx2]
                codes[idx_change] = codes[self.idx_dst] - codes[idx_static]
            elif self.opcode == 2:
                # inverse of codes[self.idx_dst] = codes[self.idx1] * codes[self.idx2]
                codes[idx_change] = codes[self.idx_dst] / codes[idx_static]
        return codes


def part2(codes):
    indices = [i for i, x in enumerate(codes) if x == 99]
    commands = list()
    codes, commands = forward(codes)
    codes[0] = 19690720
    codes_bak = deepcopy(codes)

    for idx in indices:
        codes = deepcopy(codes_bak)
        # print('Trying %d' % idx)
        for i in range(len(commands) - 1):
            codes = commands[-(i + 1)].backward(codes, commands[:-(i + 1)])
        # print('Solved: ', codes[1], codes[2])

    return codes


def part2a(codes, target=19690720):
    for i in range(100):
        for j in range(100):
            new_codes = forward(deepcopy(codes), i, j)
            print(i, j, new_codes[0][0])
            if new_codes[0][0] == target:
                return i, j
    raise ValueError("Didn't find solution")


def forward(codes, noun=None, verb=None):
    index = 0
    commands = list()
    if noun is not None:
        codes[1] = noun
    if verb is not None:
        codes[2] = verb

    done = False
    while True:
        opcode = codes[index]
        if opcode == 99:
            break
        elif opcode not in [1, 2]:
            raise ValueError("Unexpected opcode %d at position %d." % (opcode, index))

        cmd = Intcode(codes[index:index + 4])
        commands.append(cmd)
        codes = cmd.forward(codes)
        index += 4

    return codes, commands


def test_forward():
    pairs = [
        [[2, 0, 0, 0, 99], [1, 0, 0, 0, 99]],
        [[2, 3, 0, 6, 99], [2, 3, 0, 3, 99]],
        [[2, 4, 4, 5, 99, 9801], [2, 4, 4, 5, 99, 0]],
        [[30, 1, 1, 4, 2, 5, 6, 0, 99], [1, 1, 1, 4, 99, 5, 6, 0, 99]],
    ]
    for codes_out, codes_in in pairs:
        out, _ = forward(codes_in)
        assert codes_out == out, out


if __name__ == '__main__':
    test_forward()
    with open(fn) as fp:
        codes = list(map(int, fp.read().strip().split(',')))

    # codes, commands = forward(codes, 12, 2)
    # print(codes[0])

    noun, verb = part2a(codes)
    print(100 * noun + verb)
