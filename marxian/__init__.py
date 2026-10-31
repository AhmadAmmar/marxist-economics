"""The pamphlet's equations as small functions. Symbols follow Appendix A: c constant capital, v variable capital, s surplus value.

Each function states one definition used in the text. They do the arithmetic only: whether a money figure can stand in for a
value magnitude is an argument the pamphlet makes in context.
"""


def cost_price(c, v):
    """k = c + v."""
    return c + v


def commodity_value(c, v, s):
    """w = c + v + s."""
    return c + v + s


def exploitation_rate(s, v):
    """e = s / v (Eq. 5.2)."""
    return s / v


def profit_rate(s, c, v):
    """r = s / (c + v) (Eq. 7.1)."""
    return s / (c + v)


def organic_composition(c, v):
    """OCC = c / v, used as shorthand for the organic composition of capital."""
    return c / v


def profit_rate_from_composition(e, occ):
    """r = e / (1 + OCC) (Eq. 7.2)."""
    return e / (1 + occ)


def working_day_split(hours, v, s):
    """Necessary and surplus labour time, dividing the day in proportion to v and s."""
    necessary = hours * v / (v + s)
    return necessary, hours - necessary


def prices_of_production(industries):
    """Average profit rate and prices of production for industries given as (c, v, s): p = (c + v)(1 + r)."""
    r = sum(i[2] for i in industries) / sum(i[0] + i[1] for i in industries)
    return r, [(c + v) * (1 + r) for c, v, _ in industries]


def hourly_from_piece(piece_rate, hours_per_unit):
    """A piece wage rewritten as a time wage."""
    return piece_rate / hours_per_unit


def wage_hours_to_buy(price, hourly_wage):
    """Hours of waged work needed to earn a price."""
    return price / hourly_wage
