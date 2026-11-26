"""Command line interface: encrypt, decrypt and print the key square."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import TextIO

from playfair.cipher import CiphertextError, decrypt, digraphs, encrypt, remove_fillers
from playfair.square import KeySquare


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="playfair", description="Cifrado Playfair con cuadrado de 5 x 5."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    encrypter = commands.add_parser("encrypt", help="cifrar")
    decrypter = commands.add_parser("decrypt", help="descifrar")
    decrypter.add_argument(
        "--strip-fillers", action="store_true", help="quitar las X de relleno probables"
    )
    for command in (encrypter, decrypter):
        command.add_argument("--key", "-k", required=True, help="palabra o frase clave")
        command.add_argument("--pairs", action="store_true", help="separar la salida en dígrafos")
        command.add_argument("text", nargs="?", help="texto; si se omite se lee de stdin")
    square = commands.add_parser("square", help="mostrar el cuadrado de una clave")
    square.add_argument("key", help="palabra o frase clave")

    return parser


def _grouped(text: str) -> str:
    return " ".join(text[index : index + 2] for index in range(0, len(text), 2))


def main(
    argv: Sequence[str] | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
) -> int:
    arguments = _parser().parse_args(argv)
    target = stdout or sys.stdout
    if arguments.command == "square":
        target.write(f"{KeySquare.from_key(arguments.key)}\n")

        return 0
    text = arguments.text if arguments.text is not None else (stdin or sys.stdin).read()
    if arguments.command == "encrypt":
        if not digraphs(text):
            print("error: el texto no contiene letras", file=sys.stderr)

            return 2
        result = encrypt(text, arguments.key)
    else:
        try:
            result = decrypt(text, arguments.key)
        except CiphertextError as error:
            print(f"error: {error}", file=sys.stderr)

            return 2
        if arguments.strip_fillers:
            result = remove_fillers(result)
    target.write((_grouped(result) if arguments.pairs else result) + "\n")

    return 0
