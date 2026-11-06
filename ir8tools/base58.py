#!/usr/bin/python3
"""Base58 encode/decode, mirroring the interface of GNU coreutils base64."""
import argparse
import os
import signal
import sys

from ir8tools import __version__

PROG = "base58"
ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
INDEX = {c: i for i, c in enumerate(ALPHABET)}
DEFAULT_WRAP = 76

# 58**5 fits in a single 30-bit CPython limb, so divmod/multiply by it stays
# on the fast single-digit path while handling 5 base58 digits per step.
CHUNK_DIGITS = 5
CHUNK = 58**CHUNK_DIGITS

HELP = """\
Usage: {prog} [OPTION]... [FILE]
Base58 encode or decode FILE, or standard input, to standard output.

With no FILE, or when FILE is -, read standard input.

Mandatory arguments to long options are mandatory for short options too.
  -d, --decode          decode data
  -i, --ignore-garbage  when decoding, ignore non-alphabet characters
  -w, --wrap=COLS       wrap encoded lines after COLS character (default {wrap}).
                          Use 0 to disable line wrapping
      --help        display this help and exit
      --version     output version information and exit

The data are encoded using the Bitcoin base58 alphabet:
  {alphabet}
Leading zero bytes are encoded as '1'. When decoding, the input may contain
newlines in addition to the bytes of the base58 alphabet. Use --ignore-garbage
to attempt to recover from any other non-alphabet bytes in the encoded stream.
""".format(prog=PROG, wrap=DEFAULT_WRAP, alphabet=ALPHABET.decode())


class Base58Error(Exception):
    pass


def encode(data):
    stripped = data.lstrip(b"\0")
    zeros = len(data) - len(stripped)

    n = int.from_bytes(stripped, "big")
    digits = []
    while n:
        n, chunk = divmod(n, CHUNK)
        for _ in range(CHUNK_DIGITS):
            chunk, d = divmod(chunk, 58)
            digits.append(ALPHABET[d])
    # The last chunk may have been padded with zero digits ('1'); drop them.
    while digits and digits[-1] == ALPHABET[0]:
        digits.pop()

    return ALPHABET[0:1] * zeros + bytes(reversed(digits))


def decode(text):
    stripped = text.lstrip(ALPHABET[0:1])
    zeros = len(text) - len(stripped)

    n = 0
    for start in range(0, len(stripped), CHUNK_DIGITS):
        group = stripped[start : start + CHUNK_DIGITS]
        value = 0
        for c in group:
            try:
                value = value * 58 + INDEX[c]
            except KeyError:
                raise Base58Error("invalid input")
        n = n * 58 ** len(group) + value

    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\0" * zeros + body


def wrap(data, cols):
    if not data:
        return b""
    if cols == 0:
        return data
    lines = [data[i : i + cols] for i in range(0, len(data), cols)]
    return b"\n".join(lines) + b"\n"


def die(msg, show_try=False):
    sys.stderr.write("{}: {}\n".format(PROG, msg))
    if show_try:
        sys.stderr.write("Try '{} --help' for more information.\n".format(PROG))
    sys.exit(1)


class Parser(argparse.ArgumentParser):
    def error(self, message):
        die(message, show_try=True)


def parse_args(argv):
    parser = Parser(prog=PROG, add_help=False)
    parser.add_argument("-d", "--decode", action="store_true")
    parser.add_argument("-i", "--ignore-garbage", action="store_true")
    parser.add_argument("-w", "--wrap", default=str(DEFAULT_WRAP))
    parser.add_argument("--help", action="store_true")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)

    if args.help:
        sys.stdout.write(HELP)
        sys.exit(0)
    if args.version:
        sys.stdout.write("{} (ir8tools) {}\n".format(PROG, __version__))
        sys.exit(0)

    if not args.wrap.isdigit():
        die("invalid wrap size: '{}'".format(args.wrap))
    args.wrap = int(args.wrap)

    if len(args.files) > 1:
        die("extra operand '{}'".format(args.files[1]), show_try=True)
    args.file = args.files[0] if args.files else "-"
    return args


def read_input(path):
    if path == "-":
        return sys.stdin.buffer.read()
    try:
        with open(path, "rb") as f:
            return f.read()
    except IsADirectoryError as e:
        die("read error: {}".format(e.strerror))
    except OSError as e:
        die("{}: {}".format(path, e.strerror))


def main(argv=None):
    # Die silently on SIGPIPE like coreutils instead of raising BrokenPipeError.
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = read_input(args.file)

    try:
        if args.decode:
            if args.ignore_garbage:
                text = bytes(c for c in data if c in INDEX)
            else:
                text = data.replace(b"\n", b"")
            out = decode(text)
        else:
            out = wrap(encode(data), args.wrap)
        sys.stdout.buffer.write(out)
        sys.stdout.buffer.flush()
    except Base58Error as e:
        die(str(e))
    except BrokenPipeError:
        # Fallback where SIGPIPE doesn't exist: avoid a second error when
        # Python flushes stdout at shutdown.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(1)


if __name__ == "__main__":
    main()
