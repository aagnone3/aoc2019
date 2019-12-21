from util import log


def get_opcode(code):
    if code in [1, 2, 3, 4, 5, 6, 7, 8, 99]:
        return False, code
    return True, int(str(code)[-2:])


class Intcode(object):

    OPCODES = [1, 2, 3]

    def __init__(self, command, enable_param_modes=False):
        self.enable_param_modes = enable_param_modes
        self.__parse_op(command[0])

    def __parse_op(self, op):
        if self.enable_param_modes:
            code = str(op)
            self.opcode = int(code[-2:])

            self.param_modes = [0] * len(self)
            modes = list(map(int, code[:-2]))
            modes.reverse()
            for i in range(len(modes)):
                self.param_modes[i] = modes[i]
        else:
            self.opcode = op

    def __call__(self, codes):
        raise ValueError("__call__ invoked for base class")


class Op1(Intcode):

    def __init__(self, command, addr, **kwargs):
        super(Op1, self).__init__(command, **kwargs)
        self.param1, self.param2, self.param_dst = command[1:]
        self.addr = addr

    def __call__(self, codes):
        if self.enable_param_modes:
            a = self.param1 if self.param_modes[0] == 1 else codes[self.param1]
            b = self.param2 if self.param_modes[1] == 1 else codes[self.param2]
            dst = self.param_dst
        else:
            a = codes[self.param1]
            b = codes[self.param2]
            dst = self.param_dst

        codes[dst] = a + b
        print(self.addr, len(self))
        return codes, self.addr + len(self) + 1

    def __len__(self):
        return 3

    def __str__(self):
        return "codes[%d] = codes[%d] + codes[%d]" % (self.param_dst, self.param1, self.param2)


class Op2(Intcode):

    def __init__(self, command, addr, **kwargs):
        super(Op2, self).__init__(command, **kwargs)
        self.param1, self.param2, self.param_dst = command[1:]
        self.addr = addr

    def __call__(self, codes):
        if self.enable_param_modes:
            a = self.param1 if self.param_modes[0] == 1 else codes[self.param1]
            b = self.param2 if self.param_modes[1] == 1 else codes[self.param2]
            dst = self.param_dst
        else:
            a = codes[self.param1]
            b = codes[self.param2]
            dst = self.param_dst

        codes[dst] = a * b
        return codes, self.addr + len(self) + 1

    def __len__(self):
        return 3

    def __str__(self):
        return "codes[%d] = codes[%d] * codes[%d]" % (self.param_dst, self.param1, self.param2)


class Op3(Intcode):

    def __init__(self, command, addr, value, **kwargs):
        super(Op3, self).__init__(command, **kwargs)
        self.param_dst = command[1]
        self.value = value
        self.addr = addr

    def __call__(self, codes):
        codes[self.param_dst] = self.value
        return codes, self.addr + len(self) + 1

    def __len__(self):
        return 1

    def __str__(self):
        return "hi"


class Op4(Intcode):

    def __init__(self, command, addr, **kwargs):
        super(Op4, self).__init__(command, **kwargs)
        self.param_dst = command[1]
        self.output = None
        self.addr = addr

    def __call__(self, codes):
        self.output = codes[self.param_dst]
        return codes, self.addr + len(self) + 1

    def __len__(self):
        return 1

    def __str__(self):
        return "hi"


class Op5(Intcode):

    def __init__(self, command, addr, **kwargs):
        super(Op5, self).__init__(command, **kwargs)
        self.test = (command[1] != 0)
        self.addr = command[2] if self.test else addr + len(self) + 1

    def __call__(self, codes):
        return codes, self.addr

    def __len__(self):
        return 2

    def __str__(self):
        return "hi"


class Op6(Intcode):

    def __init__(self, command, addr, **kwargs):
        super(Op6, self).__init__(command, **kwargs)
        self.test = (command[1] == 0)
        self.addr = command[2] if self.test else addr + len(self) + 1

    def __call__(self, codes):
        return codes, self.addr

    def __len__(self):
        return 2

    def __str__(self):
        return "hi"


class Op7(Intcode):

    def __init__(self, command, addr, **kwargs):
        super(Op7, self).__init__(command, **kwargs)
        self.param1, self.param2, self.dst = command[1:]
        self.addr = addr

    def __call__(self, codes):
        if self.param1 < self.param2:
            codes[self.dst] = 1
        else:
            codes[self.dst] = 0
        return codes, self.addr + len(self) + 1

    def __len__(self):
        return 3

    def __str__(self):
        return "hi"


class Op8(Intcode):

    def __init__(self, command, addr, **kwargs):
        super(Op8, self).__init__(command, **kwargs)
        self.param1, self.param2, self.dst = command[1:]
        self.addr = addr

    def __call__(self, codes):
        if self.param1 == self.param2:
            codes[self.dst] = 1
        else:
            codes[self.dst] = 0
        return codes, self.addr + len(self) + 1

    def __len__(self):
        return 3

    def __str__(self):
        return "hi"



def make_intcode(command, *args, **kwargs):
    is_param_mode, opcode = get_opcode(command[0])
    # log.info('Opcode: %d, Param mode? %d', opcode, is_param_mode)

    if opcode == 1:
        return Op1(command, *args, enable_param_modes=is_param_mode)
    elif opcode == 2:
        return Op2(command, *args, enable_param_modes=is_param_mode)
    elif opcode == 3:
        return Op3(command, *args, enable_param_modes=is_param_mode)
    elif opcode == 4:
        return Op4(command, *args, enable_param_modes=is_param_mode)
    elif opcode == 5:
        return Op5(command, *args, enable_param_modes=is_param_mode)
    elif opcode == 6:
        return Op6(command, *args, enable_param_modes=is_param_mode)
    elif opcode == 7:
        return Op7(command, *args, enable_param_modes=is_param_mode)
    elif opcode == 8:
        return Op8(command, *args, enable_param_modes=is_param_mode)
    else:
        raise ValueError('Bad opcode: %d' % opcode)
