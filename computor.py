#!/usr/bin/python

import sys;
import re;


def check_poly(_poly):
    return re.match(
        "^\s*-?(?:(?:\d*(?:\.\d+)?[xX](?:\^\d+)?)|(?:\d+(?:\.\d+)?))(?:\s*(?:[+\-]|\*\s*-?)(?:\s*(?:(?:\d*(?:\.\d+)?[xX])(?:\^\d+)?|(?:\d+)(?:\.\d+)?))\s*)*\s*=\s*-?(?:(?:\d*(?:\.\d+)?[xX](?:\^\d+)?)|(?:\d+(?:\.\d+)?))(?:\s*(?:[+\-]|\*\s*-?)(?:\s*(?:(?:\d*(?:\.\d+)?[xX])(?:\^\d+)?|(?:\d+)(?:\.\d+)?))\s*)*\s*$",
        _poly)


def multipy(_terms):
    i = 1
    pattern = "(?:[*]-?|[+\-])(?:(\d*(?:\.\d+)?)[xX](?:\^(\d{1}))?|(\d+(?:\.\d+)?))"
    while i < len(_terms):
        sign = 1;
        base = False
        if _terms[i][0] == '*':
            if re.match('-', _terms[i]) and re.match('-', _terms[i - 1]):
                sign = 1
            elif re.match('-', _terms[i]) or re.match('-', _terms[i - 1]):
                sign = -1;
            _t1 = re.match(pattern, _terms[i - 1])
            _t2 = re.match(pattern, _terms[i])
            _t1fix = 1;
            _t2fix = 1;
            exp = ''
            if _t1.group(1) != None and _t2.group(1) != None:
                if _t1.group(2) != None and _t2.group(2) != None:
                    exp = "^" + str(float(_t1.group(2)) + float(_t2.group(2)))
                elif _t1.group(2) != None:
                    exp = "^" + str(float(_t1.group(2)) + 1)
                elif _t2.group(2) != None:
                    exp = "^" + str(float(_t2.group(2)) + 1)
                else:
                    exp = "^2"
            elif _t1.group(1) != None and _t1.group(2) > '1':
                exp = "^" + _t1.group(2)
            elif _t2.group(1) != None and _t2.group(2) > '1':
                exp = "^" + _t2.group(2)

            if (_t1.group(1) != None and _t1.group(2) != '0') or (_t2.group(1) != None and _t2.group(2) != '0'):
                base = True
            if _t1.group(1):
                _t1fix = float(_t1.group(1))
            elif _t1.group(3):
                _t1fix = float(_t1.group(3))
            if _t2.group(1):
                _t2fix = float(_t2.group(1))
            elif _t2.group(3):
                _t2fix = float(_t2.group(3))
            res = _t1fix * _t2fix
            if base:
                res = str(res) + 'x'
            res = str(res) + exp
            if sign == -1:
                res = '-' + res
            else:
                res = '+' + res
            _terms[i - 1] = res
            _terms.remove(_terms[i])
        else:
            i = i + 1


def map_terms(_list):
    _map = {0: 0.0, 1: 0.0, 2: 0.0}
    try:
        for t in _list:
            m = re.match("([+-])(?:(\d*(?:\.\d+)?)[xX](?:\^(\d{1}))?|(\d+(?:\.\d+)?))", t)
            if m.group(4) != None:
                if m.group(1) == '-':
                    _map[0] = _map[0] - float(m.group(4))
                else:
                    _map[0] = _map[0] + float(m.group(4))
            else:
                if m.group(3) and _map.has_key(int(m.group(3))) == False:
                    _map[int(m.group(3))] = 0.0
                if m.group(1) == '-':
                    if m.group(3):
                        if m.group(2):
                            _map[int(m.group(3))] = _map[int(m.group(3))] - float(m.group(2))
                        else:
                            _map[int(m.group(3))] = _map[int(m.group(3))] - 1
                    else:
                        if m.group(2):
                            _map[1] = _map[1] - float(m.group(2))
                        else:
                            _map[1] = _map[1] - 1
                else:
                    if m.group(3):
                        if m.group(2):
                            _map[int(m.group(3))] = _map[int(m.group(3))] + float(m.group(2))
                        else:
                            _map[int(m.group(3))] = _map[int(m.group(3))] + 1
                    else:
                        if m.group(2):
                            _map[1] = _map[1] + float(m.group(2))
                        else:
                            _map[1] = _map[1] + 1
    except KeyError:
        print "Exceeds the 2nd degree found degree {0}".format(m.group(3))
        sys.exit(0);
    return _map


def print_side(_m):
    print_zero = True
    for exp, val in _m.items():
        if val != 0:
            if val > 0:
                if print_zero:
                    sys.stdout.write(str(val))
                else:
                    sys.stdout.write("+ " + str(val))
            else:
                sys.stdout.write("- " + str(val * -1))
            if exp > 1:
                sys.stdout.write("X^" + str(exp) + ' ')
            elif exp == 1:
                sys.stdout.write("X ")
            else:
                sys.stdout.write(' ')
            print_zero = False
    if print_zero:
        sys.stdout.write('0 ')


def print_step(_ml, _mr):
    print_side(_ml)
    sys.stdout.write("= ")
    print_side(_mr)
    print ""


def print_degree(_m):
    _max = 0
    for key, val in _m.items():
        if key > _max and val != 0:
            _max = key
    print "Polynomial degree: " + str(_max)
    if _max > 2:
        print "The polynomial degree is strictly greater than 2, I can't solve."
        sys.exit(0);


def pow_ten(num):
    res = 1.0
    if num >= 0:
        for i in range(0, num):
            res = res * 10.0
    else:
        num = num * -1
        for i in range(0, num):
            res = res * 0.1
    return res


def sqrt(num):
    t_num = num
    res = 0.0
    m = 12
    j = 1.0
    if num < 0:
        raise ValueError('square root not defined for negative numbers')
    for i in range(m, 0, -1):
        if t_num - ((2 * res) + (j * pow_ten(i))) * (j * pow_ten(i)) >= 0:
            while t_num - ((2 * res) + (j * pow_ten(i))) * (j * pow_ten(i)) >= 0:
                j = j + 1
                if j >= 10:
                    break
            j = j - 1
            t_num = t_num - ((2 * res) + (j * pow_ten(i))) * (j * pow_ten(i))
            res = res + (j * pow_ten(i))
            j = 1.0

    for i in range(0, -m, -1):
        if t_num - ((2 * res) + (j * pow_ten(i))) * (j * pow_ten(i)) >= 0:
            while t_num - ((2 * res) + (j * pow_ten(i))) * (j * pow_ten(i)) >= 0:
                j = j + 1
            j = j - 1
            t_num = t_num - ((2 * res) + (j * pow_ten(i))) * (j * pow_ten(i))
            res = res + (j * pow_ten(i))
            j = 1.0
    return res


def solve_quad(_m):
    _div = 2 * _m[2]
    _sqr = (_m[1] * _m[1]) - (4 * _m[0] * _m[2])
    if _div == 0:
        print "Unsolvable zero division"
        sys.exit(0)
    if _sqr < 0:
        print "Unsolvable sqrt of negative number"
        sys.exit(0)
    _t = -1 * _m[1]
    _sqr = sqrt(_sqr)
    pos = (_t + _sqr) / _div
    neg = (_t - _sqr) / _div
    print "X = " + str(pos)
    if pos != neg:
        print "Or X = " + str(neg)


def solve_lineior(_m):
    _num = -1 * _m[0]
    if _m[1] != 0:
        _num = _num / _m[1]
    print "X = " + str(_num)


def solve_equasion(_m, lc, rc):
    if _m[2] != 0:
        solve_quad(_m)
    elif _m[1] != 0:
        solve_lineior(_m)
    else:
        if _m[0] == 0:
            print str(lc) + " = " + str(rc)
        else:
            print str(lc) + " != " + str(rc)


def simplify(_poly):
    pattern = "\s*(?:[+\-]?|\*\s*-?)?\s*(?:(?:\d*(?:\.\d+)?[xX])(?:\^\d+)?|\d+(?:\.\d+)?)\s*";
    _split = _poly.split('=')
    _left = re.findall(pattern, _split[0])
    _right = re.findall(pattern, _split[1])
    if not re.match("^[+\-*]", _left[0]):
        _left[0] = "+" + _left[0]
    if not re.match("^[+\-*]", _right[0]):
        _right[0] = "+" + _right[0]
    multipy(_left)
    multipy(_right)
    _ml = map_terms(_left)
    _mr = map_terms(_right)
    sys.stdout.write('Simplified: ')
    print_step(_ml, _mr)
    lc = _ml[0]
    rc = _mr[0]
    for exp in _ml.keys():
        if _mr.has_key(exp) and _mr[exp] != 0:
            _ml[exp] = _ml[exp] - _mr[exp]
            _mr[exp] = 0
    sys.stdout.write('Reduced form: ')
    print_step(_ml, _mr)
    print_degree(_ml)
    solve_equasion(_ml, lc, rc)


poly = ""

if len(sys.argv) == 1:
    print "Please specify a polynomial.";
    exit(0);
elif len(sys.argv) == 2:
    poly = sys.argv[1]
else:
    poly = ''.join(sys.argv[1 : len(sys.argv)])

poly = poly.replace(' ', '')
if check_poly(poly):
    simplify(poly)
else:
    print "is not polynomial"
