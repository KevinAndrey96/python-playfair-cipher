"""The 5 x 5 Playfair key square, with I and J sharing a cell."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
SIDE = 5


def normalize(text: str) -> str:
    """Uppercase Latin letters only, accents removed and J folded into I."""
    decomposed = unicodedata.normalize("NFD", text.upper()).replace("J", "I")

    return "".join(char for char in decomposed if char in ALPHABET)


@dataclass(frozen=True, slots=True)
class KeySquare:
    """Key letters first (without repeats), then the rest of the alphabet."""

    letters: str
    _positions: dict[str, tuple[int, int]] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if sorted(self.letters) != sorted(ALPHABET):
            raise ValueError("a key square needs each of the 25 letters exactly once")
        positions = {letter: divmod(index, SIDE) for index, letter in enumerate(self.letters)}
        object.__setattr__(self, "_positions", positions)

    @classmethod
    def from_key(cls, key: str) -> KeySquare:
        letters = dict.fromkeys(normalize(key) + ALPHABET)

        return cls("".join(letters))

    def position(self, letter: str) -> tuple[int, int]:
        return self._positions[letter]

    def at(self, row: int, column: int) -> str:
        return self.letters[(row % SIDE) * SIDE + column % SIDE]

    def rows(self) -> list[str]:
        return [self.letters[start : start + SIDE] for start in range(0, len(self.letters), SIDE)]

    def __str__(self) -> str:
        return "\n".join(" ".join(row) for row in self.rows())
