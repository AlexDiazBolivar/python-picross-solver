

class Unsolvable(Exception):
    pass

def elements_normalize(elements):
    return [e for e in elements if e > 0]

def element_to_list(element):
    return [True] * element

def elements_exact_row(elements):
    result = []
    for e in elements:
        if not e:
            continue
        if len(result):
            result.append(False)
        result.extend(element_to_list(e))

    return result

def pad(padlen):
    return [False] * padlen

def elements_combinations(elements, size):
    elements = elements_normalize(elements)
    if len(elements) == 0:
        return [[False] * size]

    min_size = sum(elements) + len(elements) - 1

    if min_size > size:
        raise Unsolvable()

    if min_size == size:
        return [elements_exact_row(elements)]


    results = []
    for padlen in xrange(size - min_size + 1):
        first = elements[0]
        firstl = element_to_list(first)
        remaining = elements[1:]

        rpad = size - padlen - first - 1
        for result in elements_combinations(remaining, rpad):
            if rpad >= 0:
                results.append(pad(padlen) + firstl + [False] + result)
            else:
                results.append(pad(padlen) + firstl + result)

    return results 

def row_check_conflict(row1, row2):
    assert len(row1) == len(row2)
    for i, v1 in enumerate(row1):
        v2 = row2[i]
        if v1 is None or v2 is None:
            continue
        if v1 != v2:
            return False
    return True

def find_commonalities(results):
    common = results[0]
    for result in results[1:]:
        for i, v in enumerate(result):
            if common[i] != v:
                common[i] = None
    return common

import copy

class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = []

        for i in xrange(height):
            self.rows.append([None] * width)

        self.col_elements = [[]] * width
        self.row_elements = [[]] * height

    def row(self, i):
        return self.rows[i][:]

    def col(self, j):
        result = []
        for i in xrange(self.height):
            result.append(self.rows[i][j])
        return result

    def set_row(self, i, row):
        self.rows[i] = row[:]
        print self.render()
        print '---'

    def set_col(self, j, col):
        for i, v in enumerate(col):
            self.set_cell(i, j, v)
        print self.render()
        print '---'

    def set_cell(self, i, j, value):
        self.rows[i][j] = value

    def solve(self):
        while True:
            oldrows = copy.deepcopy(self.rows)
            self.solve1()
            if self.rows == oldrows:
                return

    def solve1(self):
        for i in xrange(self.height):
            row = self.row(i)
            if None not in row:
                continue
            possibilities = [
                possibility for possibility
                in elements_combinations(self.row_elements[i], self.width)
                if row_check_conflict(row, possibility)
            ]
            if len(possibilities) == 0:
                raise Unsolvable()
            elif len(possibilities) == 1:
                self.set_row(i, possibilities[0])
            else:
                commonalities = find_commonalities(possibilities)
                if commonalities != row:
                    self.set_row(i, commonalities)

        for j in xrange(self.width):
            col = self.col(j)
            if None not in col:
                continue
            possibilities = [
                possibility for possibility
                in elements_combinations(self.col_elements[j], self.height)
                if row_check_conflict(col, possibility)
            ]

            if len(possibilities) == 0:
                raise Unsolvable()
            elif len(possibilities) == 1:
                self.set_col(j, possibilities[0])
            else:
                commonalities = find_commonalities(possibilities)
                if commonalities != col:
                    self.set_col(j, commonalities)


    def render(self):
        result = ''
        for row in self.rows:
            for v in row:
                if v is True:
                    result += 2*u'\u2593'
                elif v is False:
                    result += 2*u'\u2591'
                elif v is None:
                    result += '  '
            result += '\n'
        return result.rstrip('\n')
