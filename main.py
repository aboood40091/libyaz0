#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# libyaz0
# Version 0.3
# Copyright © 2017 MasterVermilli0n / AboodXD

# This file is part of libyaz0.

# libyaz0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# libyaz0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import sys

from __init__ import decompress, compress, guessFileExt


def printInfo():
    print("\nUsage:")
    print("  main [option...] input")
    print("\nOptions:")
    print(" -o <output>       Output file, if not specified, the output file will have the same name as the intput file")
    print(" -c                Compress (Will try to decompress if not specified)")
    print("\nCompression options:")
    print(" -level <level>    compression level (1-9) (1 is the default)")
    print("                   0: No compression (Fastest)")
    print("                   9: Best compression (Slowest)")
    print(" -unk <unk>        the unknown value that will be located at 0x8-0xC (0x00000000 is the default)")

    sys.exit()


def main():
    print("libyaz0 v0.3")
    print("(C) 2017 MasterVermilli0n / AboodXD")

    if len(sys.argv) < 2:
        printInfo()

    input_ = sys.argv[-1]

    if not os.path.isfile(input_):
        printInfo()

    compressYaz = False

    if "-c" in sys.argv:
        compressYaz = True

    if "-o" in sys.argv:
        output_ = sys.argv[sys.argv.index("-o") + 1]
    else:
        output_ = os.path.splitext(input_)[0]

    if compressYaz:
        if "-unk" in sys.argv:
            unk = int(sys.argv[sys.argv.index("-unk") + 1], 0)
        else:
            unk = 0

        if "-level" in sys.argv:
            level = int(sys.argv[sys.argv.index("-level") + 1], 0)
        else:
            level = 1

        if not 0 <= level <= 9:
            printInfo()

        with open(input_, "rb") as inf:
            inb = inf.read()

        data = compress(inb, unk, level)

        with open(output_ + ".yaz0", "wb+") as out:
            out.write(data)

    else:
        with open(input_, "rb") as inf:
            inb = inf.read()

        data = decompress(inb)

        ext = guessFileExt(data)

        with open(output_ + ext, "wb+") as out:
            out.write(data)


if __name__ == '__main__':
    main()
