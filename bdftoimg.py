#!/usr/bin/env python3
import sys, re
from collections import OrderedDict
from math import *
from optparse import OptionParser
from PIL import Image

def jisx0208_to_shiftjis(code):
    if code >= 0x2121:
        row = (code >> 8 & 0xFF) - 0x21
        col = (code & 0xFF) - 0x20
        code -= 0x2121 + row * 161
        code += (row // 2 - 1) * 66
        if row % 2 == 0 and col >= 64:
            code += 1
        return code + 0x8140
    else:
        return code

if __name__ == '__main__':
    parser = OptionParser(usage="Usage: %prog <filename> <outputfile> [--jis-to-sjis]")
    parser.add_option('--jis-to-sjis', action='store_true', dest='jis_to_sjis', default=False, help="convert encoding from JIS to SJIS")
    parser.add_option('--offset', dest='offset', default=0, help="Add character offsets to output image.")
    (options, args) = parser.parse_args()
    if len(args) != 2:
        sys.stderr.write("Input and output files must be specified.\n")
        sys.exit(-1)
    inputFile = args[0]
    outputFile = args[1]

    try:
        with open(inputFile) as f:
            inputData = f.read()
    except OSError:
        sys.stderr.write("Could not open '%s'." % args[0])

    syntax = "FONT_{}\n{}"
    clauseRegex = re.compile(r'STARTCHAR(?s:.+?)ENCODING\s+(\d+)(?s:.+?)BBX\s+(\d+)\s+(\d+)\s+(-*\d+)\s+(-*\d+)\s*\nBITMAP\s*\n((?s:.*?))\n?ENDCHAR\n')
    result = {}
    maxSize = (0, 0)
    for char in clauseRegex.finditer(inputData):
        image = []
        encoding = char.group(1)
        size = (int(char.group(2)), int(char.group(3)))
        maxSize = (max(size[0], maxSize[0]), max(size[1], maxSize[1]))
        bitmap = char.group(6).split('\n')
        if bitmap == ['']:
            continue
        for line in bitmap:
            bitwidth = len(line) * 4
            bin = int(line, 16)
            for _ in range(-int(char.group(4))):
                image.append(0)
            for _ in range(-int(char.group(4)), size[0]):
                if bin & (0b01 << (bitwidth - 1)):
                    image.append(255)
                else:
                    image.append(0)
                bin = bin << 1
        code = int(encoding)
        if options.jis_to_sjis:
            code = jisx0208_to_shiftjis(code)
        result[code] = Image.frombytes('L', size, bytes(image))

    result = OrderedDict(sorted(result.items())).items()
    resultIter = iter(result)
    current = next(resultIter)
    first = current[0] - int(options.offset)
    rows = ceil((next(reversed(result))[0] - first) / 16)
    image = Image.new('L', (maxSize[0] * 16, maxSize[1] * rows))
    try:
        for row in range(rows):
            for col in range(16):
                index = 16 * row + col
                if index == current[0] - first:
                    image.paste(current[1], (maxSize[0] * col, maxSize[1] * row))
                    current = next(resultIter)
    except StopIteration:
        pass
    image.save(outputFile)
