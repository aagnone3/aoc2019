from __future__ import print_function
from copy import deepcopy

from util import log
from intcode import make_intcode, Op4, get_opcode


CMD_LENGTH = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3
}


def get_outputs(commands):
    codes = list()
    for command in commands:
        if isinstance(command, Op4):
            codes.append(command.output)
    return codes.pop(), codes


def part1(codes):
    addr = 0
    commands = list()

    while True:
        print('--------------------')
        log.info('Opcode: %d', codes[addr])
        is_param_mode, opcode = get_opcode(codes[addr])
        if opcode == 99:
            break
        # elif opcode not in [1, 2, 3, 4]:
        #     raise ValueError("Unexpected opcode %d at position %d." % (opcode, addr))

        hop_size = CMD_LENGTH[opcode] + 1
        instr = codes[addr:addr + hop_size]
        print('Instr {} @ {}'.format(instr, addr))
        if opcode == 3:
            cmd = make_intcode(instr, addr, 5)
        else:
            cmd = make_intcode(instr, addr)
        commands.append(cmd)
        codes, addr = cmd(codes)
        print('Next addr: {}'.format(addr))

    return get_outputs(commands)


def main():
    fn = "../res/d5.txt"
    with open(fn) as fp:
        codes = list(map(int, fp.read().strip().split(',')))

    print(part1(codes))


if __name__ == '__main__':
    main()
