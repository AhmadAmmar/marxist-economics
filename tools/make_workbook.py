"""Write the Excel calculator with live formulas, so readers can change an input and see each result change.

    python tools/make_workbook.py        writes docs/downloads/marxian_calculator.xlsx
"""
import pathlib
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
import sialkot

INPUT = PatternFill("solid", fgColor="E3F0EF")
BOLD = Font(bold=True)


def sheet(wb, title, intro, rows):
    """rows: (label, value or formula, what it means). Inputs are shaded; a formula starts with =."""
    ws = wb.create_sheet(title)
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = intro
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:C2")
    ws.row_dimensions[2].height = 48
    for col, text in zip("ABC", ("Quantity", "Value", "What it means")):
        ws[f"{col}4"] = text
        ws[f"{col}4"].font = BOLD
    for i, (label, value, meaning) in enumerate(rows, 5):
        ws[f"A{i}"], ws[f"B{i}"], ws[f"C{i}"] = label, value, meaning
        ws[f"C{i}"].alignment = Alignment(wrap_text=True, vertical="top")
        if not str(value).startswith("="):
            ws[f"B{i}"].fill = INPUT
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 80
    return ws


def build(out):
    wb = Workbook()
    start = wb.active
    start.title = "Start here"
    for i, line in enumerate(["Marxian Economics 101: calculator", "", "Change the shaded cells. Everything else recalculates.",
                              "Sheet 'Rates' works through c, v and s. 'Two industries' shows prices of production. 'Sialkot' uses the figures from the worked example.",
                              "Money figures stand in for value magnitudes only under the conventions explained in the pamphlet.",
                              "Guide: https://ahmadammar.github.io/marxist-economics/mathematics/",
                              "Report a problem: https://github.com/AhmadAmmar/marxist-economics/issues"], 1):
        start[f"A{i}"] = line
    start["A1"].font = Font(bold=True, size=14)
    start.column_dimensions["A"].width = 120
    sheet(wb, "Rates", "One capital in one period. The starting figures are an illustration.", [
        ("c, constant capital", 100, "Value of materials and machinery used up. It passes into the product without adding new value."),
        ("v, variable capital", 100, "Wages: the value advanced to buy labour-power."),
        ("s, surplus value", 100, "New value produced beyond the value of labour-power."),
        ("k = c + v, cost price", "=B5+B6", "What the capitalist advances."),
        ("w = c + v + s, value", "=B5+B6+B7", "Value of the output."),
        ("New value = v + s", "=B6+B7", "Added by living labour in this period."),
        ("e = s / v, rate of exploitation", "=B7/B6", "Surplus value per unit of wages."),
        ("r = s / (c + v), rate of profit", "=B7/(B5+B6)", "Surplus value per unit of capital advanced (Eq. 7.1)."),
        ("OCC = c / v", "=B5/B6", "Shorthand for the organic composition of capital."),
        ("r = e / (1 + OCC)", "=B11/(1+B13)", "The same rate of profit, written to show both drivers (Eq. 7.2). Must equal the line above."),
        ("Working day, hours", 8, "Length of the working day."),
        ("Necessary labour time, hours", "=B15*B6/(B6+B7)", "Part of the day that replaces the value of the wage."),
        ("Surplus labour time, hours", "=B15-B16", "Part of the day that produces surplus value."),
    ])
    sheet(wb, "Two industries", "Example 7.1. Equal rates of profit redistribute surplus value without changing the total.", [
        ("c, industry A", 50, "Lower composition."), ("v, industry A", 100, ""), ("s, industry A", 100, "Here e = 100%, so s = v."),
        ("c, industry B", 150, "Higher composition."), ("v, industry B", 100, ""), ("s, industry B", 100, ""),
        ("Average rate of profit r", "=(B7+B10)/(B5+B6+B8+B9)", "Total surplus value over total capital advanced."),
        ("Value of A's output", "=B5+B6+B7", "w = c + v + s."), ("Value of B's output", "=B8+B9+B10", ""),
        ("Price of production, A", "=(B5+B6)*(1+B11)", "p = (c + v)(1 + r)."), ("Price of production, B", "=(B8+B9)*(1+B11)", ""),
        ("Surplus value transferred, A", "=B14-B12", "Price minus value. A negative figure means value flows out."), ("Surplus value transferred, B", "=B15-B13", ""),
        ("Check: total price minus total value", "=B14+B15-B12-B13", "Must be zero in this example."),
    ])
    i = sialkot.inputs()
    sheet(wb, "Sialkot", "Illustrative benchmarks from different sources and years, as set out in the example. Sources are in data/sialkot.json.", [
        ("Piece rate, PKR per ball", i["PieceRatePKR"], "Bloomberg Businessweek, 2022."), ("Hours per ball", i["HoursPerBall"], ""), ("Balls per day", i["BallsPerDay"], ""), ("Paid days per month", i["WorkDaysMonth"], ""),
        ("Hourly wage, PKR", "=B5/B6", "Piece rate over hours per ball."), ("Daily wage, PKR", "=B5*B7", ""), ("Monthly wage, PKR", "=B10*B8", ""),
        ("Living wage quoted in 2022, PKR", i["LivingWageQuotePKR"], ""), ("Wage as a share of it", "=B11/B12", ""),
        ("Retail price, USD", i["RetailUSD"], ""), ("PKR per USD", i["USDPKR"], f"NBP Treasury rate sheet, {i['RateDate']}."), ("Retail price, PKR", "=B14*B15", ""), ("Wage-hours to buy one ball", "=B16/ROUND(B9,2)", "Uses the hourly wage rounded to 2 decimals, as the pamphlet does."),
        ("Reported total cost, PKR", i["ReportedTotalCostPKR"], "Atkin et al., Table A.1. Differs from c + v by rounding."), ("Reported margin", i["MarkupPct"] / 100, "A stand-in for surplus at this stage."),
        ("Producer price, PKR", "=B18*(1+B19)", ""), ("Profit per ball, PKR", "=B20-B18", "Money form of surplus at one stage only."),
        ("Variable capital, PKR", round(i["CuttingLabourPKR"] + i["StitchingLabourPKR"] + i["OtherLabourPKR"], 2), "Cutting, stitching and other labour in the cost table."),
        ("Profit over wages", "=B21/B22", "An accounting illustration, not a measured rate of exploitation."),
    ])
    out.parent.mkdir(exist_ok=True)
    wb.save(out)


if __name__ == "__main__":
    target = ROOT / "docs/downloads/marxian_calculator.xlsx"
    build(target)
    print("wrote", target)
