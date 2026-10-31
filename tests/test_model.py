"""The functions must reproduce the pamphlet's own worked examples."""
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
import marxian as M
import sialkot as S


def test_two_industry_example_7_1():
    r, prices = M.prices_of_production([(50, 100, 100), (150, 100, 100)])
    assert r == pytest.approx(0.5)
    assert prices == pytest.approx([225, 375])
    assert M.commodity_value(50, 100, 100) == 250
    assert M.commodity_value(150, 100, 100) == 350
    assert prices[0] - 250 == pytest.approx(-25)
    assert prices[1] - 350 == pytest.approx(25)


def test_total_price_equals_total_value():
    _, prices = M.prices_of_production([(50, 100, 100), (150, 100, 100)])
    assert sum(prices) == pytest.approx(250 + 350)


@pytest.mark.parametrize("c,v,s", [(50, 100, 100), (150, 100, 100), (300, 100, 50)])
def test_equation_7_2_agrees_with_7_1(c, v, s):
    direct = M.profit_rate(s, c, v)
    via = M.profit_rate_from_composition(M.exploitation_rate(s, v), M.organic_composition(c, v))
    assert via == pytest.approx(direct)


def test_working_day_adds_up():
    n, x = M.working_day_split(9, 56.29, 17.08)
    assert n + x == pytest.approx(9)
    assert round(n, 1) == 6.9 and round(x, 1) == 2.1


def test_sialkot_matches_the_pamphlet():
    d = S.derive(S.inputs())
    assert d["DailyPayPKR"] == 480 and d["DailyHours"] == 9 and d["HourlyWage"] == 53.33 and d["MonthlyPayPKR"] == 9600
    assert d["MaterialsPKR"] == 143.68 and d["VariableCapitalPKR"] == 56.29 and d["ConstantCapitalPKR"] == 154.52 and d["CostSum"] == 210.81
    assert d["ProducerPrice"] == 227.91 and d["Surplus"] == 17.08 and d["NewValue"] == 73.37 and d["SurplusOverWage"] == 30.3
    assert d["RetailPKR"] == 46183 and d["HoursToBuy"] == 866 and d["BallsToBuy"] == 289 and d["DaysToBuy"] == 96.2
    assert d["ExportAvgUSD"] == 4.44
