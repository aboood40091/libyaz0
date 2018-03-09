#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# libyaz0
# Version 0.5
# Copyright © 2017-2018 MasterVermilli0n / AboodXD

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

import struct


def DecompressYaz(src):
    dest_end = struct.unpack(">I", src[4:8])[0]
    dest = bytearray(dest_end)

    src_end = len(src)

    code = src[16]

    src_pos = 17
    dest_pos = 0

    while src_pos < src_end and dest_pos < dest_end:
        for _ in range(8):
            if src_pos >= src_end or dest_pos >= dest_end:
                break

            if code & 0x80:
                dest[dest_pos] = src[src_pos]
                src_pos += 1
                dest_pos += 1

            else:
                b1 = src[src_pos]
                src_pos += 1
                b2 = src[src_pos]
                src_pos += 1

                copy_src = dest_pos - ((b1 & 0x0f) << 8 | b2) - 1

                n = b1 >> 4
                if not n:
                    n = src[src_pos] + 0x12
                    src_pos += 1

                else:
                    n += 2

                while n > 0:
                    n -= 1
                    dest[dest_pos] = dest[copy_src]
                    copy_src += 1
                    dest_pos += 1

            code <<= 1

        else:
            if src_pos >= src_end or dest_pos >= dest_end:
                break

            code = src[src_pos]
            src_pos += 1

    return dest


def CompressYaz(src, opt_compr):
    if opt_compr == 1:
        range_ = 0x100

    elif opt_compr == 9:
        range_ = 0x1000

    elif not opt_compr:
        range_ = 0

    elif opt_compr < 9:
        range_ = 0x10e0 * opt_compr / 9 - 0x0e0

    else:
        range_ = 0x1000

    src_pos = 0
    src_end = len(src)

    dest = bytearray(len(src) + (len(src) + 8) // 8)
    dest_pos = 0

    mask = 0
    code_byte_pos = dest_pos

    max_len = 0x111

    while src_pos < src_end:
        if not mask:
            code_byte_pos = dest_pos
            dest[dest_pos] = 0; dest_pos += 1
            mask = 0x80

        found_len = 1

        if src_pos + 2 < src_end:
            search = src_pos - range_
            if search < 0:
                 search = 0

            cmp_end = src_pos + max_len
            if cmp_end > src_end:
                cmp_end = src_end

            c1 = src[src_pos:src_pos + 1]
            while search < src_pos:
                search = src.find(c1, search, src_pos)
                if search == -1:
                    break

                cmp1 = search + 1
                cmp2 = src_pos + 1

                while cmp2 < cmp_end and src[cmp1] == src[cmp2]:
                    cmp1 += 1; cmp2 += 1

                len_ = cmp2 - src_pos

                if found_len < len_:
                    found_len = len_
                    found = search
                    if found_len == max_len:
                        break

                search += 1

        if found_len >= 3:
            delta = src_pos - found - 1

            if found_len < 0x12:
                dest[dest_pos] = delta >> 8 | ( found_len - 2 ) << 4; dest_pos += 1
                dest[dest_pos] = delta; dest_pos += 1

            else:
                dest[dest_pos] = delta >> 8; dest_pos += 1
                dest[dest_pos] = delta; dest_pos += 1
                dest[dest_pos] = found_len - 0x12; dest_pos += 1

            src_pos += found_len

        else:
            dest[code_byte_pos] |= mask
            dest[dest_pos] = src[src_pos]; dest_pos += 1; src_pos += 1

        mask >>= 1

    return dest[:dest_pos]
