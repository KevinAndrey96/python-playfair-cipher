import pytest
from hypothesis import given
from hypothesis import strategies as st

from playfair import CiphertextError, decrypt, digraphs, encrypt, normalize, remove_fillers

ORIGINAL_PLAINTEXT = "THIS SECRET MESSAGE IS ENCRYPTED"
ORIGINAL_CIPHERTEXT = "WEDLLKHWLYLFXPQPHFDLHYHWOYYLKP"


def test_reproduces_the_original_2020_example() -> None:
    assert encrypt(ORIGINAL_PLAINTEXT, "Yoan Pinzon") == ORIGINAL_CIPHERTEXT


def test_reproduces_the_wikipedia_example() -> None:
    assert encrypt("hide the gold in the tree stump", "playfair example") == (
        "BMODZBXDNABEKUDMUIXMMOUVIF"
    )


@pytest.mark.parametrize(
    ("plaintext", "pairs"),
    [
        ("BALLOON", ["BA", "LX", "LO", "ON"]),
        ("XXL", ["XQ", "XL"]),
        ("CAT", ["CA", "TX"]),
        ("TAX", ["TA", "XQ"]),
        ("", []),
    ],
)
def test_digraph_rules(plaintext: str, pairs: list[str]) -> None:
    assert digraphs(plaintext) == pairs


def test_decrypt_keeps_fillers_and_remove_fillers_strips_them() -> None:
    raw = decrypt(ORIGINAL_CIPHERTEXT, "Yoan Pinzon")

    assert raw == "THISSECRETMESXSAGEISENCRYPTEDX"
    assert remove_fillers(raw) == normalize(ORIGINAL_PLAINTEXT)


def test_decrypt_accepts_spaced_lowercase_pairs() -> None:
    assert decrypt("bm od zb xd", "playfair example") == "HIDETHEG"


@pytest.mark.parametrize(
    ("ciphertext", "message"),
    [
        ("ABC", "even number"),
        ("AJ", "without J"),
        ("A1", "without J"),
        ("AA", "never repeat"),
    ],
)
def test_rejects_malformed_ciphertext(ciphertext: str, message: str) -> None:
    with pytest.raises(CiphertextError, match=message):
        decrypt(ciphertext, "KEY")


@given(st.text(), st.text())
def test_ciphertext_is_valid_and_decrypts_to_the_digraphs(plaintext: str, key: str) -> None:
    ciphertext = encrypt(plaintext, key)

    assert decrypt(ciphertext, key) == "".join(digraphs(plaintext))


@given(st.text(alphabet="ABCDEFGHIKLMNOPRSTUVWYZ", min_size=1))
def test_remove_fillers_inverts_padding_for_texts_without_x_or_q(plaintext: str) -> None:
    assert remove_fillers(decrypt(encrypt(plaintext, "MONARCHY"), "MONARCHY")) == plaintext
