#!/usr/bin/env python
import re


def check(code):
    if re.search(r"^[0-9A-Fa-f]{3}-[0-9A-Fa-f]{2}[8-9A-Fa-f]$", code):
        return True

    if re.search(r"^[0-9A-Fa-f]{3}-[0-9A-Fa-f]{2}[8-9A-Fa-f]-[0-9A-Fa-f]{3}$", code):
        x = int(code[8], 16) ^ int(code[9], 16)
        if x == 0 or x > 7:
            return True

    return False


def rr8(n, shift):
    return (n >> shift) | (n << (8 - shift)) & 0xff


def rl8(n, shift):
    return ((n << shift) | (n >> (8 - shift))) & 0xff


def encode(addr, val, orig=None):
    code = '%02X' % val
    code += '%X-%02X%X' % ((addr & 0xf00) >> 8, addr & 0xff, 0xf - (addr >> 12))

    if orig is not None:
        num = rl8(orig ^ 0x45, 2) ^ 0xff
        chk = ((num & 0xf0) >> 4) ^ 0x08
        code += '-%X%X%X' % ((num & 0xf0) >> 4, chk, num & 0x0f)

    return code


def decode(code):
    if not check(code):
        return False

    val  = int(code[:2], 16)
    addr = (0xf - int(code[6], 16)) << 12 | int(code[2] + code[4] + code[5], 16)
    result = {'addr': addr, 'value': val}

    if len(code) > 7:
        result['original'] = rr8(int(code[8] + code[10], 16) ^ 0xff, 2) ^ 0x45

    return result


def usage(prog):
    print('usage:    %s <code>' % prog)
    print('          %s <addr> <value> [original]' % prog)
    print('')
    print('examples:\n')
    print('\tdecode: %s 001-5CA-E62' % prog)
    print('\t        %s 001-5CA' % prog)
    print('')
    print('\tencode: %s 0x7654 0x01' % prog)
    print('\t        %s 0x7654 0x02 0xff' % prog)
    print('\t        %s 1234 ab cd\n' % prog)


def main():
    import sys

    if len(sys.argv) < 2:
        usage(sys.argv[0])
        sys.exit(-1)

    if len(sys.argv) == 2:
        val = decode(sys.argv[1])
        if not val:
            print('error: invalid game genie code detected')
            sys.exit(-1)

        if val['original']:
            print('0x%04x: 0x%02x => 0x%02x' % (val['addr'], val['original'], val['value']))
        else:
            print('0x%04x: 0x%02x' % (val['addr'], val['value']))

    else:
        addr = int(sys.argv[1], 16)
        val  = int(sys.argv[2], 16)

        if len(sys.argv) > 3:
            orig = int(sys.argv[3], 16)
        else:
            orig = None

        print('code: %s' % encode(addr, val, orig))


if __name__ == '__main__':
    main()
