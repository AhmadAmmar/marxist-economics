"""Work out the Sialkot figures from data/sialkot.json with the marxian package, and write them as LaTeX macros.

    python tools/sialkot.py        writes latex/generated/sialkot_numbers.tex
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import marxian as M


def inputs():
    data = json.loads((ROOT / "data/sialkot.json").read_text(encoding="utf8"))
    return {k: v["value"] for k, v in data["inputs"].items()}


def thousands(x):
    return f"{x:,}".replace(",", "{,}")


def derive(i):
    """Figures calculated from the inputs, at the precision the documents state."""
    daily_pay = i["PieceRatePKR"] * i["BallsPerDay"]
    daily_hours = i["HoursPerBall"] * i["BallsPerDay"]
    hourly = round(M.hourly_from_piece(i["PieceRatePKR"], i["HoursPerBall"]), 2)
    k = i["ReportedTotalCostPKR"]
    price = round(k * (1 + i["MarkupPct"] / 100), 2)
    surplus = round(price - k, 2)
    v = round(i["CuttingLabourPKR"] + i["StitchingLabourPKR"] + i["OtherLabourPKR"], 2)
    materials = round(i["RexinePKR"] + i["ClothPKR"] + i["LatexPKR"] + i["BladderPKR"], 2)
    c = round(materials + i["OverheadPKR"], 2)
    retail = round(i["RetailUSD"] * i["USDPKR"])
    hours = round(M.wage_hours_to_buy(retail, hourly))
    necessary, surplus_hours = M.working_day_split(daily_hours, v, surplus)
    return {
        "DailyPayPKR": daily_pay, "DailyHours": daily_hours, "HourlyWage": hourly, "MonthlyPayPKR": daily_pay * i["WorkDaysMonth"],
        "MaterialsPKR": materials, "VariableCapitalPKR": v, "ConstantCapitalPKR": c, "CostSum": round(M.cost_price(c, v), 2),
        "ProducerPrice": price, "Surplus": surplus, "NewValue": round(v + surplus, 2), "SurplusOverWage": round(100 * M.exploitation_rate(surplus, v), 1),
        "ExportAvgUSD": round(i["ValueUSDMillion"] / i["BallsMillion"], 2), "RetailPKR": retail, "HoursToBuy": hours,
        "BallsToBuy": round(hours / i["HoursPerBall"]), "DaysToBuy": round(hours / daily_hours, 1),
        "NecessaryHours": round(necessary, 1), "SurplusHours": round(surplus_hours, 1),
    }


def macros():
    i = inputs()
    d = derive(i)
    rows = {"USDPKR": i["USDPKR"], "RateDate": i["RateDate"], "PieceRatePKR": i["PieceRatePKR"], "BallsPerDay": i["BallsPerDay"], "HoursPerBall": i["HoursPerBall"], "WorkDaysMonth": i["WorkDaysMonth"],
            "LivingWageQuotePKR": i["LivingWageQuotePKR"], "LivingWageUrbanPKR": i["LivingWageUrbanPKR"], "LivingWageRuralPKR": i["LivingWageRuralPKR"],
            "cPKR": d["ConstantCapitalPKR"], "vPKR": d["VariableCapitalPKR"], "kPKR": i["ReportedTotalCostPKR"], "MarkupPct": i["MarkupPct"],
            "pPKR": d["ProducerPrice"], "sPKR": d["Surplus"], "NewValuePKR": d["NewValue"], "RetailUSD": i["RetailUSD"], "ExportAvgUSD": d["ExportAvgUSD"],
            "NecessaryHours": d["NecessaryHours"], "SurplusHours": d["SurplusHours"],
            # the same figures as the pamphlet prints them
            "SkHourly": d["HourlyWage"], "SkMonthly": thousands(d["MonthlyPayPKR"]), "SkLiving": thousands(i["LivingWageQuotePKR"]), "SkRetail": thousands(d["RetailPKR"]),
            "SkHours": d["HoursToBuy"], "SkBalls": d["BallsToBuy"], "SkDays": d["DaysToBuy"], "SkMaterials": d["MaterialsPKR"], "SkOverhead": i["OverheadPKR"],
            "SkStitch": i["StitchingLabourPKR"], "SkCostSum": d["CostSum"], "SkSurplusOverWage": d["SurplusOverWage"]}
    return "% Written by tools/sialkot.py from data/sialkot.json. Do not edit by hand.\n" + "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in rows.items())


def write():
    out = ROOT / "latex/generated/sialkot_numbers.tex"
    out.parent.mkdir(exist_ok=True)
    out.write_text(macros(), encoding="utf8", newline="\n")
    return out


if __name__ == "__main__":
    print("wrote", write())
