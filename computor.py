#!/usr/bin/python

import sys;
import re;


def check_poly(_poly):
    return re.match(
        "^(\s*-?(?:(?:\d*[xX])|(?:\d+))(?:\^[012]{1})?)(?:\s*([+\-*])\s*(\s*-?(?:(?:\d*[xX])|(?:\d+))(?:\^[012]{1})?)\s*)*\s*(=)(\s*-?(?:(?:\d*[xX])|(?:\d+))(?:\^[012]{1})?)(?:\s*([+\-*])\s*(\s*-?(?:(?:\d*[xX])|(?:\d+))(?:\^[012]{1})?)\s*)*$",
        _poly)


def multipy(_terms):
    i = 1
    while i < len(_terms):
        sign = 1;
        base = False
        if _terms[i][0] == '*':
            if re.match('-', _terms[i]) and re.match('-', _terms[i - 1]):
                sign = 1
            elif re.match('-', _terms[i]) or re.match('-', _terms[i - 1]):
                sign = -1;
            _t1 = re.match("(?:[*]-?|[+\-])(?:(\d*)[xX](?:\^(\d{1}))?|(\d+))", _terms[i - 1])
            _t2 = re.match("(?:[*]-?|[+\-])(?:(\d*)[xX](?:\^(\d{1}))?|(\d+))", _terms[i])
            _t1fix = 1;
            _t12ix = 1;
            exp = ''
            if _t1.group(1) != None and _t2.group(1) != None:
                if _t1.group(2) != None and _t2.group(2) != None:
                    exp = "^" + str(int(_t1.group(2)) + int(_t2.group(2)))
                elif _t1.group(2) != None:
                    exp = "^" + str(int(_t1.group(2)) + 1)
                elif _t2.group(2) != None:
                    exp = "^" + str(int(_t2.group(2)) + 1)
                else:
                    exp = "^2"
            if _t1.group(1) != None or _t2.group(1) != None:
                base = True
            if _t1.group(1):
                _t1fix = int(_t1.group(1))
            elif _t1.group(3):
                _t1fix = int(_t1.group(3))
            if _t2.group(1):
                _t2fix = int(_t2.group(1))
            elif _t2.group(3):
                _t2fix = int(_t2.group(3))
            res = _t1fix * _t2fix
            if base:
                res = str(res) + 'x'
            res = str(res) + exp
            if sign == -1:
                res = '-' + res
            else:
                res = '+' + res
            print res
            _terms[i - 1] = res
            _terms.remove(_terms[i])
        else:
            i = i + 1


def map_terms(_list):
    _map = {'0': 0, '1': 0, '2': 0}
    try:
        for t in _list:
            m = re.match("([+-])(?:(\d*)[xX](?:\^(\d{1}))?|(\d+))", t)
            if m.group(4) != None:
                if m.group(1) == '-':
                    _map['0'] = _map['0'] - int(m.group(4))
                else:
                    _map['0'] = _map['0'] + int(m.group(4))
            else:
                if m.group(1) == '-':
                    if m.group(2):
                        _map[m.group(3)] = _map[m.group(3)] - int(m.group(2))
                    else:
                        _map[m.group(3)] = _map[m.group(3)] - 1
                else:
                    if m.group(2):
                        _map[m.group(3)] = _map[m.group(3)] + int(m.group(2))
                    else:
                        _map[m.group(3)] = _map[m.group(3)] + 1
    except KeyError:
        print "Exceeds the 2nd degree found degree {0}".format(m.group(3))
        sys.exit(0);
    return _map


def print_step(_ml, _mr):
    for i in ['0', '1', '2']:
        if _ml[i] != 0:
            if _ml[i] > 0 :
                if i == '0':
                    sys.stdout.write(str(_ml[i]))
                else:
                    sys.stdout.write("+ " + str(_ml[i]))
            else:
                sys.stdout.write("- " + str(_ml[i] * -1))
            if i == '2':
                sys.stdout.write("X^" + str(i))
            elif i == '1':
                sys.stdout.write('X')
            else:
                sys.stdout.write(' ')
    sys.stdout.write(" = ")
    if _mr['0'] == 0 and _mr['1'] == 0 and _mr['2'] == 0:
        sys.stdout.write('0')
    else:
        for i in ['0', '1', '2']:
            if _mr[i] != 0:
                if _mr[i] > 0:
                    if i == '0':
                        sys.stdout.write(str(_mr[i]))
                    else:
                        sys.stdout.write("+ " + str(_mr[i]))
                else:
                    sys.stdout.write("- " + str(_mr[i] * -1))
                if i == '2':
                    sys.stdout.write("X^" + str(i))
                elif i == '1':
                    sys.stdout.write('X')
                else:
                    sys.stdout.write(' ')
    print ""


def simplify(_poly):
    pattern = "\s*[+\-*\/]?\s*(?:-)?\s*(?:(?:\d*[xX])|\d+)(?:\^[012]{1})?\s*";
    _split = _poly.split('=')
    print "left: " + _split[0];
    _left = re.findall(pattern, _split[0])
    _right = re.findall(pattern, _split[1])
    if not re.match("^[+\-*]", _left[0]):
        _left[0] = "+" + _left[0]
    if not re.match("^[+\-*]", _right[0]):
        _right[0] = "+" + _right[0]
    print _left;
    print _right;
    multipy(_left)
    multipy(_right)
    for t in _left:
        if _right.__contains__(t):
            _left.remove(t)
            _right.remove(t)
    _ml = map_terms(_left)
    _mr = map_terms(_right)
    print_step(_ml, _mr)
    for i in ['0', '1', '2']:
        _ml[i] = _ml[i] - _mr[i]
        _mr[i] = 0
    print_step(_ml, _mr)


poly = "";

if len(sys.argv) == 1:
    print "Please specify a polynomial.";
    exit(0);
elif len(sys.argv) == 2:
    poly = sys.argv[1];
    print "Got Polynomial[" + sys.argv[1] + ']';
else:
    poly = ''.join(sys.argv[1:len(sys.argv)])
    print "made Polynomial[" + poly + ']';

poly = poly.replace(' ', '')
if check_poly(poly):
    simplify(poly);
else:
    print "is not polynomial";
