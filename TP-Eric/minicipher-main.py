#!/usr/bin/env python

import sys
import minicipher

print("Le script s'exécute bien !")

########################
# Command Line Handler #
########################


# Argument declaration with default values

# By default, the program's action is to encrypt
encrypt = True

# Default mode of operation (how we read and write values)
binary = False

# The default key is the null key
keys = [0] * 5

# minicipher can work with only one block (in which case the program
# only reads 2 bytes) or in CBC mode with padding (which means it can
# handle an arbitrary input)
modeCBC = False

# The IV value is required with CBC mode
iv = 0

# EOF signal for the CBC mode
eof = False


def usage(msg: str):
    if len(msg) != 0:
        sys.stderr.write("%s\n\n" % msg)
    sys.stderr.write(
        "Usage: %s [-e|-d] [-b] [-1|-M] [-k <key>] [-i <iv>]\n\n" % sys.argv[0]
    )
    sys.stderr.write("  -e       encryption mode (defaut)\n")
    sys.stderr.write("  -d       decryption mode\n")
    sys.stderr.write("  -1       only one block will be en/de-crypted (defaut)\n")
    sys.stderr.write(
        "  -b       input and output are considered as binary streams (and not hexadecimal strings)\n"
    )
    sys.stderr.write("  -M       CBC mode, which allows the input to be arbitrary\n")
    sys.stderr.write("  -k <key> key definition (80 bits, or 20 hexa chars)\n")
    sys.stderr.write("           (by defaut, the null key is used)\n")
    sys.stderr.write(
        "  -i <iv>  IV (initial value), used in the CBC mode (16 bits, or 4 hexa chars)\n"
    )
    sys.stderr.write("           (the default value is a null IV)\n\n")

    sys.exit(1)


def _4b_from_hexa(c: int):
    if c >= ord("0") and c <= ord("9"):
        return c - ord("0")
    if c >= ord("A") and c <= ord("F"):
        return (c - ord("A")) + 10
    if c >= ord("a") and c <= ord("f"):
        return (c - ord("a")) + 10
    return 0xFF


def read_value(arg: bytes, nWords: int):
    if len(arg) != (nWords * 4):
        raise SyntaxError

    res = [0] * nWords

    for i in range(nWords):
        for j in range(4):
            c = _4b_from_hexa(arg[4 * i + j])
            if c == 0xFF:
                raise SyntaxError
            res[i] <<= 4
            res[i] |= c

    return res


def get_opts():
    global encrypt, binary, keys, modeCBC, iv

    i = 1
    while i < len(sys.argv):
        if sys.argv[i][0] != "-":
            usage("Invalid argument: should start with a dash (-).")

        if sys.argv[i][1] == "e":
            encrypt = True
        elif sys.argv[i][1] == "d":
            encrypt = False
        elif sys.argv[i][1] == "1":
            modeCBC = False
        elif sys.argv[i][1] == "M":
            modeCBC = True
        elif sys.argv[i][1] == "b":
            binary = True

        elif sys.argv[i][1] == "k":
            if len(sys.argv[i]) == 2:
                if len(sys.argv) <= i + 1:
                    usage("'-k' must be followed by a 20-char key.")
                i += 1
                argument = sys.argv[i]
            else:
                argument = sys.argv[i][2:]
            try:
                keys = read_value(argument.encode(), 5)
            except SyntaxError:
                usage("Invalid key.")

        elif sys.argv[i][1] == "i":
            if len(sys.argv[i]) == 2:
                if len(sys.argv) <= i + 1:
                    usage("'-i' must be followed by a 4-char key.")
                i += 1
                argument = sys.argv[i]
            else:
                argument = sys.argv[i][2:]
            try:
                iv = read_value(argument.encode(), 1)[0]
            except SyntaxError:
                usage("Invalid IV.")

        else:
            usage("Unknwon option.")

        i += 1


def get_16b_from_stdin(padding: bool):
    global eof, binary

    if not binary:
        input: list[int] = []
        for i in range(4):
            next = sys.stdin.buffer.read(1)
            if (not next) or (_4b_from_hexa(next[0]) == 0xFF):
                if padding:
                    eof = True
                    input.append(ord("8"))
                    for j in range(4 - len(input)):
                        input.append(ord("0"))
                    break
                else:
                    raise SyntaxError
            input.append(next[0])

        bytes_input = bytes(input)
        try:
            return read_value(bytes_input, 1)[0]
        except SyntaxError:
            if padding:
                eof = True
                return 0x8000
            else:
                raise SyntaxError

    else:
        # encoding == binary
        next = sys.stdin.buffer.read(2)
        if len(next) == 2:
            return (next[0] << 8) | (next[1])
        elif padding:
            eof = True
            if len(next) == 1:
                return (next[0] << 8) | 0x80
            else:
                return 0x8000
        else:
            raise SyntaxError


def print_16b(output: int):
    global binary

    if not binary:
        sys.stdout.write("%4.4x" % output)
    else:
        sys.stdout.buffer.write(bytes([output >> 8, output & 0xFF]))


def print_16b_and_truncate(output: int):
    global binary

    if not binary:
        if output == 0x8000:
            return
        elif (output & 0xFFF) == 0x800:
            sys.stdout.write("%1.1x" % (output >> 12))
        elif (output & 0xFF) == 0x80:
            sys.stdout.write("%2.2x" % (output >> 8))
        elif (output & 0xF) == 0x8:
            sys.stdout.write("%3.3x" % (output >> 4))
        else:
            sys.stderr.write("Padding Error: the final pattern could not be found.")

    else:
        # encoding == binary
        if output == 0x8000:
            return
        elif (output & 0x00FF) == 0x80:
            sys.stdout.buffer.write(bytes([output >> 8]))
        else:
            sys.stderr.write("Padding Error: the final pattern could not be found.")


def main():
    global encrypt, binary, keys, modeCBC, iv, eof

    minicipher.init_inverse_ops()
    get_opts()

    if not modeCBC:
        try:
            input = get_16b_from_stdin(False)
        except SyntaxError:
            usage("Unexpected char: the input was supposed to be hexadecimal chars.")

        if encrypt:
            output = minicipher.encrypt(input, keys)
        else:
            output = minicipher.decrypt(input, keys)

        print_16b(output)

    else:
        # Mode CBC
        if encrypt:
            while not eof:
                input = get_16b_from_stdin(True)
                output = minicipher.encrypt(input ^ iv, keys)
                iv = output ^ input
                print_16b(output)

        else:
            # Decryption
            try:
                input = get_16b_from_stdin(False)
            except SyntaxError:
                return

            while True:
                output = minicipher.decrypt(input, keys) ^ iv
                iv = input ^ output
                try:
                    input = get_16b_from_stdin(False)
                    print_16b(output)
                except SyntaxError:
                    print_16b_and_truncate(output)
                    return

    if not binary:
        sys.stdout.write("\n")

    sys.exit(0)


main()