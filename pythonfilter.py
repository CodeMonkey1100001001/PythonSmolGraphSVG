#!/usr/bin/python3
import sys

for line in sys.stdin:
    line = line.replace('stroke="#000000','stroke="#ffffff')
    # line = line.replace('','')
    line = line.replace('fill="#000000"', 'fill="#ffffff"')
    line = line.replace('stroke = "#000"','stroke = "#ffffff"')
    line = line.replace('stroke="#000"','stroke="#ffffff"')
    line = line.replace('fill="#000"', 'fill="#ffffff"')

    print(line,end='')


