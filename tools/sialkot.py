"""Work out the Sialkot figures from data/sialkot.json and write them as LaTeX macros.

    python tools/sialkot.py        writes latex/generated/sialkot_numbers.tex
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def inputs():
    data = json.loads((ROOT / "data/sialkot.json").read_text(encoding="utf8"))
    return {k: v["value"] for k, v in data["inputs"].items()}


def derive(i):
    """Figures calculated from the inputs, at the precision the documents state."""
    daily_pay = i["PieceRatePKR"] * i["BallsPerDay"]
    daily_hours = i["HoursPerBall"] * i["BallsPerDay"]
    monthly = daily_pay * i["WorkDaysMonth"]
    price = i["ReportedTotalCostPKR"] * (1 + i["MarkupPct"] / 100)
    surplus = round(price, 2) - i["ReportedTotalCostPKR"]
    return {
        "DailyPayPKR": daily_pay, "DailyHours": daily_hours, "HourlyWage": round(daily_pay / daily_hours, 2), "MonthlyPayPKR": monthly,
        "CostSum": round(i["ConstantCapitalPKR"] + i["VariableCapitalPKR"], 2), "ProducerPrice": round(price, 2), "Surplus": round(surplus, 2),
        "NewValue": round(i["VariableCapitalPKR"] + surplus, 2), "ExportAvgUSD": round(i["ValueUSDMillion"] / i["BallsMillion"], 2),
    }


def macros():
    i = inputs()
    d = derive(i)
    rows = {"PieceRatePKR": i["PieceRatePKR"], "BallsPerDay": i["BallsPerDay"], "HoursPerBall": i["HoursPerBall"], "WorkDaysMonth": i["WorkDaysMonth"],
            "LivingWageQuotePKR": i["LivingWageQuotePKR"], "LivingWageUrbanPKR": i["LivingWageUrbanPKR"], "LivingWageRuralPKR": i["LivingWageRuralPKR"],
            "cPKR": i["ConstantCapitalPKR"], "vPKR": i["VariableCapitalPKR"], "kPKR": i["ReportedTotalCostPKR"], "MarkupPct": i["MarkupPct"],
            "pPKR": d["ProducerPrice"], "sPKR": d["Surplus"], "NewValuePKR": d["NewValue"], "RetailUSD": i["RetailUSD"], "ExportAvgUSD": d["ExportAvgUSD"]}
    return "% Written by tools/sialkot.py from data/sialkot.json. Do not edit by hand.\n" + "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in rows.items())


if __name__ == "__main__":
    out = ROOT / "latex/generated/sialkot_numbers.tex"
    out.parent.mkdir(exist_ok=True)
    out.write_text(macros(), encoding="utf8", newline="\n")
    print("wrote", out)
