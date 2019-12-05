

def has_adjacent_digits(num, two_sided=False):
    s = str(num)
    if two_sided:
        for i in range(2, 4):
            if s[i] != s[i - 1] and s[i] == s[i + 1] and s[i] != s[i + 2]:
                return True
            if s[i] == s[i - 1] and s[i] != s[i + 1] and s[i] != s[i - 2]:
                return True
        if s[0] == s[1] and s[1] != s[2]:
            return True
        if s[-1] == s[-2] and s[-2] != s[-3]:
            return True
    else:
        for i in range(1, 5):
            if s[i] == s[i - 1] or s[i] == s[i + 1]:
                return True
    return False


def test_has_adjacent():
    cases = [
        [223456, True],
        [322456, True],
        [523356, True],
        [523155, True],
        [553157, True],
        [522158, True],
        [523446, True],
        [523455, True],
        [523456, False],
    ]
    for num, exp in cases:
        print '%d -> %d' % (num, exp)
        assert has_adjacent_digits(num) == exp

    print '---'
    cases = [
        [223456, True],
        [112233, True],
        [411238, True],
        [421138, True],
        [429118, True],
        [429411, True],
        [523356, True],
        [123444, False],
        [444444, False],
        # [443444, False],
        [111122, True],
        [111123, False],
    ]
    for num, exp in cases:
        print '%d -> %d' % (num, exp)
        assert has_adjacent_digits(num, two_sided=True) == exp


def potential_numbers(low, high, two_sided=False):
    cnt = 0
    good = True
    for i in range(low, high):
        s = str(i)
        good = True
        for j in range(1, 6):
            if int(s[j]) < int(s[j - 1]):
                good = False
                break
        if good and has_adjacent_digits(i, two_sided=two_sided):
            cnt += 1
    return cnt


if __name__ == '__main__':
    test_has_adjacent()
    print potential_numbers(347312, 805915)
    print potential_numbers(347312, 805915, two_sided=True)
