#!/usr/bin/python3
# example:
#  cat /tmp/misc/input.svg | python3 ./pythonfilter.py >/tmp/misc/output.svg

import sys

for line in sys.stdin:
    # line = line.replace('','')
    line = line.replace('stroke="#000000','stroke="#ffffff')
    line = line.replace('fill="#000000"', 'fill="#ffffff"')
    line = line.replace('stroke = "#000"','stroke = "#ffffff"')
    line = line.replace('stroke="#000"','stroke="#ffffff"')
    line = line.replace('fill="#000"', 'fill="#ffffff"')
    print(line,end='')


