import math
from util import log

DEBUG = False


def fuel_from_mass(mass):
    return int(math.floor(mass / 3.) - 2)


def fuel_from_fuel(fuel_mass, print_vals=False):
    if print_vals:
        print 'The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.'
    fuel_needed = 0
    done = False
    while not done:
        fuel_mass = fuel_from_mass(fuel_mass)
        if fuel_mass > 0:
            fuel_needed += fuel_mass
            if print_vals:
                print fuel_mass
        else:
            done = True
    return fuel_needed


def part1(fn):
    if DEBUG:
        # quick test based on given inputs
        masses = {
            12: 2,
            14: 2,
            1969: 654,
            100756: 33583
        }
        for mass, expected in masses.iteritems():
            assert expected == fuel_from_mass(mass)

    # load the masses from disk and compute the fuel requirements
    with open(fn, 'r') as fp:
        masses = [int(line.strip()) for line in fp.readlines()]

    fuel_needed = reduce(lambda a, b: a + b, map(fuel_from_mass, masses))
    log.info('Total fuel needed: %d', fuel_needed)
    return fuel_needed


def part2(fn):
    if DEBUG:
        # quick test based on given inputs
        assert 50346 == fuel_from_fuel(100756, print_vals=True)

    # load the masses from disk and compute the fuel requirements
    fuel_needed = 0
    with open(fn, 'r') as fp:
        for line in fp.readlines():
            mass = int(line.strip())
            fuel = fuel_from_mass(mass)
            fuel_needed += fuel + fuel_from_fuel(fuel)

    log.info('Total fuel needed: %d', fuel_needed)
    return fuel_needed


def main(fn):
    assert 3361299 == part1(fn)
    assert 5039071 == part2(fn)


if __name__ == '__main__':
    main('../res/d1.txt')
