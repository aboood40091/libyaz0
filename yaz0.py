#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# libyaz0
# Version 0.1
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

import math
import struct
from io import BytesIO

def DecompressYaz(src):
    dest_end = struct.unpack(">I", src[4:8])[0]
    dest = BytesIO()

    src_end = len(src)

    code = 0
    code_len = 0

    pos = 16

    while pos < src_end and dest.tell() < dest_end:
        if not code_len:
            code = ord(src[pos:pos + 1])
            pos += 1
            code_len = 8

        if code & 0x80:
            dest.write(src[pos:pos + 1])
            pos += 1

        else:
            b1 = ord(src[pos:pos + 1])
            pos += 1
            b2 = ord(src[pos:pos + 1])
            pos += 1

            old_pos = dest.tell()

            copy_src = old_pos - ((b1 & 0x0f) << 8 | b2) - 1

            n = b1 >> 4
            if not n:
                n = ord(src[pos:pos + 1]) + 0x12
                pos += 1

            else:
                n += 2

            assert (3 <= n <= 0x111)

            dest.seek(copy_src)
            copy_data = dest.read(n)

            if not copy_data:
                copy_data = bytearray(n)
                print(n)

            if len(copy_data) < n:
                new_data = [copy_data]
                diff = n - len(copy_data)

                for _ in range(diff // len(copy_data)):
                    new_data.append(copy_data)

                new_data.append(copy_data[:(diff % len(copy_data))])
                copy_data = b''.join(new_data)

            dest.seek(old_pos)
            dest.write(copy_data)

        code <<= 1
        code_len -= 1

    return dest.getvalue()


def CompressYaz(src, level):
    dest = bytearray()

    assert (1 <= level <= 9)

    if level:
        data_range = 0x10e0 * level // 9 - 0x0e0
    else:
        data_range = 0

    pos = 0

    while pos < len(src):
        buffer = bytearray()
        code_byte = 0

        for i in range(8):
            max_len = math.ceil(15 * data_range / 0x1000 + 2)

            old_pos = pos

            search = old_pos - data_range
            if search < 0:
                search = 0
                search_len = old_pos
            else:
                search_len = data_range

            found_len = max_len
            if pos + found_len > len(src):
                found_len = len(src) - pos

            c1 = src[pos:pos + found_len]
            pos = search
            search_data = src[pos:pos + search_len]
            pos = old_pos + len(c1)

            found = search_data.rfind(c1)

            while found == -1 and found_len > 3:
                pos = old_pos

                found_len -= 1
                c1 = src[pos:pos + found_len]
                pos += found_len

                if len(c1) < found_len:
                    found_len = len(c1)

                found = search_data.rfind(c1)

            if found_len >= 3 and found != -1:
                delta = search_len - found - 1
                buffer += bytes([delta >> 8 | (found_len - 2) << 4])
                buffer += bytes([delta & 0xFF])

            else:
                pos = old_pos
                byte = src[pos:pos + 1]
                pos += 1

                if byte:
                    buffer += byte
                code_byte = (1 << (7 - i)) | code_byte

        dest += bytes([code_byte])
        dest += buffer

    return dest
