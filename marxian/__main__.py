"""Command line for the pamphlet's equations.

    python -m marxian rates --c 100 --v 100 --s 100
    python -m marxian industries 50,100,100 150,100,100
"""
import argparse

from . import commodity_value, cost_price, exploitation_rate, organic_composition, prices_of_production, profit_rate


def main():
    ap = argparse.ArgumentParser(prog="marxian", description="Work through the pamphlet's equations.")
    sub = ap.add_subparsers(dest="command", required=True)
    r = sub.add_parser("rates", help="rates of exploitation and profit for one capital")
    for name, meaning in (("c", "constant capital"), ("v", "variable capital"), ("s", "surplus value")):
        r.add_argument("--" + name, type=float, required=True, help=meaning)
    i = sub.add_parser("industries", help="average profit rate and prices of production")
    i.add_argument("industry", nargs="+", help="c,v,s for each industry")
    a = ap.parse_args()
    if a.command == "rates":
        print(f"cost price k = {cost_price(a.c, a.v):g}")
        print(f"value w = {commodity_value(a.c, a.v, a.s):g}")
        print(f"rate of exploitation e = {exploitation_rate(a.s, a.v):.1%}")
        print(f"rate of profit r = {profit_rate(a.s, a.c, a.v):.1%}")
        print(f"organic composition c/v = {organic_composition(a.c, a.v):.2f}")
    else:
        industries = [tuple(float(x) for x in item.split(",")) for item in a.industry]
        rate, prices = prices_of_production(industries)
        print(f"average rate of profit r = {rate:.1%}")
        for n, ((c, v, s), p) in enumerate(zip(industries, prices), 1):
            w = commodity_value(c, v, s)
            print(f"industry {n}: value {w:g}, price of production {p:g}, transfer {p - w:+g}")


if __name__ == "__main__":
    main()
