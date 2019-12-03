from __future__ import print_function
from copy import deepcopy

from util import log


class Intcode(object):

    OPCODES = {
        1: '+',
        2: '-'
    }

    def __init__(self, command):
        self.opcode, self.idx1, self.idx2, self.idx_dst = command
        if self.opcode not in self.OPCODES:
            raise ValueError('Bad opcode')

    def forward(self, codes):
        if self.opcode == 1:
            codes[self.idx_dst] = codes[self.idx1] + codes[self.idx2]
        elif self.opcode == 2:
            codes[self.idx_dst] = codes[self.idx1] * codes[self.idx2]
        return codes

    def __str__(self):
        return "codes[%d] = codes[%d] %s codes[%d]" % (self.idx_dst, self.idx1, self.OPCODES[self.opcode], self.idx2)


def part2(codes, target=19690720):
    for i in range(100):
        for j in range(100):
            new_codes = forward(deepcopy(codes), i, j)
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
    # test_forward()
    fn = "../res/d2.txt"
    with open(fn) as fp:
        codes = list(map(int, fp.read().strip().split(',')))

    # codes, commands = forward(codes, 12, 2)
    # print(codes[0])

    noun, verb = part2(codes)
    print(noun, verb)
    print(100 * noun + verb)
    # 86, 9 => 8609
