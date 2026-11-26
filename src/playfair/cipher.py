"""Playfair digraph substitution (Wheatstone, 1854)."""

from __future__ import annotations

from playfair.square import ALPHABET, KeySquare, normalize

FILLER = "X"
ALTERNATE_FILLER = "Q"


class CiphertextError(ValueError):
    """Raised when a ciphertext could not have been produced by Playfair."""


def _filler_for(letter: str) -> str:
    return ALTERNATE_FILLER if letter == FILLER else FILLER


def digraphs(plaintext: str) -> list[str]:
    """Splits text into pairs, never pairing a letter with itself.

    A filler X goes between doubled letters (Q when the doubled letter is X)
    and pads an odd final letter.
    """
    letters = normalize(plaintext)
    pairs: list[str] = []
    index = 0
    while index < len(letters):
        first = letters[index]
        second = letters[index + 1] if index + 1 < len(letters) else None
        if second is None or second == first:
            pairs.append(first + _filler_for(first))
            index += 1
        else:
            pairs.append(first + second)
            index += 2

    return pairs


def _substitute(square: KeySquare, pair: str, step: int) -> str:
    (row_a, col_a), (row_b, col_b) = square.position(pair[0]), square.position(pair[1])
    if row_a == row_b:
        return square.at(row_a, col_a + step) + square.at(row_b, col_b + step)
    if col_a == col_b:
        return square.at(row_a + step, col_a) + square.at(row_b + step, col_b)

    return square.at(row_a, col_b) + square.at(row_b, col_a)


def encrypt(plaintext: str, key: str) -> str:
    """Same row: letters to the right. Same column: letters below.

    Otherwise each letter takes the corner of the rectangle in its own row.
    """
    square = KeySquare.from_key(key)

    return "".join(_substitute(square, pair, 1) for pair in digraphs(plaintext))


def validate_ciphertext(ciphertext: str) -> list[str]:
    """Returns the digraphs of a well formed ciphertext."""
    letters = "".join(char for char in ciphertext.upper() if not char.isspace())
    if any(char not in ALPHABET for char in letters):
        raise CiphertextError("ciphertext may only contain the letters A-Z without J")
    if len(letters) % 2:
        raise CiphertextError("ciphertext must have an even number of letters")
    pairs = [letters[index : index + 2] for index in range(0, len(letters), 2)]
    if any(pair[0] == pair[1] for pair in pairs):
        raise CiphertextError("ciphertext digraphs never repeat a letter")

    return pairs


def decrypt(ciphertext: str, key: str) -> str:
    """Inverse substitution; fillers stay in place, see remove_fillers."""
    square = KeySquare.from_key(key)

    return "".join(_substitute(square, pair, -1) for pair in validate_ciphertext(ciphertext))


def remove_fillers(text: str) -> str:
    """Best effort removal of the fillers that encrypt inserts.

    Drops X between two equal letters (Q between two X) and a trailing
    filler. Genuine letters in those spots are lost, so read the result as
    a suggestion rather than an exact inverse.
    """
    output: list[str] = []
    for index, letter in enumerate(text):
        between_twins = (
            0 < index < len(text) - 1
            and index % 2 == 1
            and text[index - 1] == text[index + 1]
            and letter == _filler_for(text[index - 1])
        )
        if not between_twins:
            output.append(letter)
    if len(text) % 2 == 0 and len(output) > 1 and output[-1] == _filler_for(output[-2]):
        output.pop()

    return "".join(output)
