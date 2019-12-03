from d3 import part1, part2


def test_part1():
    path1 = ['U1', 'U1', 'R1']
    path2 = ['R2', 'U2', 'L1']
    dist = part1((path1, path2))
    assert dist == 3

    path1 = ['U1']
    path2 = ['U1']
    dist = part1((path1, path2))
    assert dist == 1

    path1 = ['U1', 'U1', 'R1']
    path2 = ['R2', 'U2', 'L2']
    dist = part1((path1, path2))
    assert dist == 2

    path1 = ['U1', 'U1', 'R3']
    path2 = ['R2', 'U3', 'D3']
    dist = part1((path1, path2))
    assert dist == 4


def test_part2():
    path1 = ['U1', 'U1', 'R1']
    path2 = ['R2', 'U2', 'L1']
    dist = part2((path1, path2))
    assert dist == 8

    path1 = ['U1']
    path2 = ['U1']
    dist = part2((path1, path2))
    assert dist == 2

    path1 = ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72']
    path2 = ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83']
    assert part2((path1, path2)) == 610

    path1 = ['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51']
    path2 = ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7']
    assert part2((path1, path2)) == 410


if __name__ == '__main__':
    test_part1()
    test_part2()
