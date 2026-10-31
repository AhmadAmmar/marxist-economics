"""The checker must catch drift, and the arithmetic must match a hand calculation."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import check_sync as C
import sialkot as S


def test_hand_calculation():
    d = S.derive(S.inputs())
    assert d["DailyPayPKR"] == 160 * 3 == 480
    assert d["HourlyWage"] == 53.33
    assert d["MonthlyPayPKR"] == 9600
    assert d["ExportAvgUSD"] == 4.44


def test_changed_input_changes_the_result():
    i = S.inputs()
    i["PieceRatePKR"] = 200
    assert S.derive(i)["MonthlyPayPKR"] == 12000


def test_a_number_missing_from_the_web_is_caught():
    assert C.number_problems("cost is 56.29 and 9{,}600", "cost is 56.29") == ["number 9,600 is in the LaTeX but not on the web"]


def test_large_text_drift_is_caught_but_moved_footnotes_are_not():
    words = " ".join(f"word{chr(97 + i % 26)}x" for i in range(200))
    assert C.word_problems("alpha beta gamma delta", "gamma delta alpha beta") == []
    assert C.word_problems(words, "other text") != []


def test_macros_carry_the_shared_values():
    m = S.macros()
    assert r"\newcommand{\pPKR}{227.91}" in m and r"\newcommand{\PieceRatePKR}{160}" in m
