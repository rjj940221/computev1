#!/usr/bin/python

import sys;
import re;


def checkPoly(poly):
    if re.match(
        "^(\s*[+-]?\d*[xX]?(?:\^[012]{1})?)(?:\s*([+\-*/])\s(\s*[+-]?\d*[xX]?(?:\^[012]{1})?)\s*)*\s*=\s*(\s*[+-]?\d*[xX]?(?:\^[012]{1})?)(?:\s*([+\-*/])\s(\s*[+-]?\d*[xX]?(?:\^[012]{1})?)\s*)*\s*$",
        poly):
        print "is polynomial";
    else:
        print "is not polynomial";


if len(sys.argv) == 1:
    print "Please specify a polynomial.";
    exit(0);
elif len(sys.argv) == 2:
    print "Got Polynomial[" + sys.argv[1] + ']';
else:
    poly = ' '.join(sys.argv[1:len(sys.argv)])
    print "made Polynomial[" + poly + ']';

checkPoly(poly);
