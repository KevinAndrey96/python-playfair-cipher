import io
import subprocess
import sys

import pytest

from playfair.cli import main


def run(argv: list[str], stdin: str = "") -> tuple[int, str]:
    output = io.StringIO()
    status = main(argv, stdin=io.StringIO(stdin), stdout=output)

    return status, output.getvalue()


def test_encrypts_in_pairs() -> None:
    assert run(["encrypt", "-k", "Yoan Pinzon", "--pairs", "this secret"]) == (
        0,
        "WE DL LK HW LY\n",
    )


def test_decrypts_from_stdin_and_strips_fillers() -> None:
    assert run(
        ["decrypt", "-k", "Yoan Pinzon", "--strip-fillers"], "WE DL LK HW LY LF XP QP HF DL"
    ) == (0, "THISSECRETMESSAGEIS\n")


def test_decrypt_keeps_fillers_by_default() -> None:
    assert run(["decrypt", "-k", "Yoan Pinzon", "XPQP"]) == (0, "SXSA\n")


def test_prints_the_square() -> None:
    status, output = run(["square", "Yoan Pinzon"])

    assert status == 0
    assert output.splitlines()[0] == "Y O A N P"


def test_reports_errors_with_exit_code_two(capsys: pytest.CaptureFixture[str]) -> None:
    assert run(["encrypt", "-k", "KEY", "123"]) == (2, "")
    assert run(["decrypt", "-k", "KEY", "ABC"]) == (2, "")
    assert capsys.readouterr().err.count("error:") == 2


def test_module_entry_point() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "playfair", "encrypt", "-k", "playfair example", "hide"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert completed.stdout == "BMOD\n"
