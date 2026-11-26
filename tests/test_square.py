import pytest
from hypothesis import given
from hypothesis import strategies as st

from playfair import ALPHABET, KeySquare, normalize


def test_builds_the_square_of_the_original_example() -> None:
    assert KeySquare.from_key("Yoan Pinzon").rows() == [
        "YOANP",
        "IZBCD",
        "EFGHK",
        "LMQRS",
        "TUVWX",
    ]


def test_prints_as_a_grid() -> None:
    assert str(KeySquare.from_key("")).splitlines()[0] == "A B C D E"


def test_wraps_around_edges() -> None:
    square = KeySquare.from_key("")

    assert square.at(0, 5) == "A"
    assert square.at(-1, 0) == "V"
    assert square.position("Z") == (4, 4)


def test_normalize_folds_j_accents_and_symbols() -> None:
    assert normalize("¡Jamón, ñandú!") == "IAMONNANDU"


def test_rejects_invalid_squares() -> None:
    with pytest.raises(ValueError, match="exactly once"):
        KeySquare("ABC")


@given(st.text())
def test_every_key_yields_a_permutation_of_the_alphabet(key: str) -> None:
    assert sorted(KeySquare.from_key(key).letters) == sorted(ALPHABET)
