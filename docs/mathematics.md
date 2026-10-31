# The mathematics, step by step

This page explains each main equation in the pamphlet, starting from what every letter means. You only need arithmetic. Each step is written out, with a worked example.

**Try it yourself:**
[Excel calculator](downloads/marxian_calculator.xlsx){ .md-button }
[Printable cheat sheet](downloads/marxian_cheatsheet.pdf){ .md-button }
[Python code](https://github.com/AhmadAmmar/marxist-economics/tree/main/marxian){ .md-button }

## Before the sums: what kind of numbers are these?

Marx's categories are about social relations measured in labour time. Examples usually express them in money, as if money were proportional to value. That is a teaching convention, stated wherever it is used. A firm's accounts do not directly show surplus value, so an accounting figure can only stand in for it, with care.

## The letters

| Symbol | Name | Plain meaning |
|:--|:--|:----|
| $c$ | Constant capital | Value of materials and machinery used up. It passes into the product and adds no new value |
| $v$ | Variable capital | Value advanced as wages to buy labour-power |
| $s$ | Surplus value | New value produced beyond the value of labour-power |
| $k$ | Cost price | What the capitalist advances for this output |
| $w$ | Value of output | Old value passed on, plus new value |
| $e$ | Rate of exploitation | Surplus value for each unit of wages |
| $r$ | Rate of profit | Surplus value for each unit of capital advanced |
| $\mathrm{OCC}$ | Organic composition | Used here as shorthand for $c/v$ |
| $T$ | Working day | Hours worked in a day |
| $T_n$, $T_s$ | Necessary and surplus labour time | The parts of the day that replace the wage and produce surplus value |

Labour-power is the capacity to work, which is what a worker sells. Labour is the activity performed. The whole argument rests on the gap between the two.

## 1. Value of the output

Old value is passed on, and living labour adds new value:

$$
w = c + v + s
$$

**Example.** With $c = 100$, $v = 100$ and $s = 100$:

$$
w = 100 + 100 + 100 = 300
$$

New value is $v + s = 200$. The other 100 was already there.

## 2. Cost price

The capitalist's outlay leaves out surplus value, which is why profit can look as if it arises from selling:

$$
k = c + v = 100 + 100 = 200
$$

## 3. Rate of exploitation

Compare surplus value with wages, because only living labour creates new value:

$$
e = \frac{s}{v} = \frac{100}{100} = 1 = 100\%
$$

## 4. The working day

If new value is produced evenly through the day, the day splits in the same proportion as $v$ and $s$:

$$
T_n = T \times \frac{v}{v + s}
$$

$$
T_s = T - T_n
$$

**Example.** In an 8-hour day with $v = s$:

$$
T_n = 8 \times \frac{100}{200} = 4 \text{ hours}
$$

$$
T_s = 8 - 4 = 4 \text{ hours}
$$

This also gives $e = T_s / T_n$, so exploitation can be read in hours as well as in money.

## 5. Rate of profit

Capitalists compare profit with everything they advanced:

$$
r = \frac{s}{c + v} = \frac{100}{100 + 100} = 50\%
$$

So $r$ is always smaller than $e$ when $c$ is above zero. They measure different things: $e$ measures the relation between capital and labour, and $r$ measures the return on capital.

## 6. Linking the two rates

Start from $r$. Since $e = s/v$, we can replace $s$ with $ev$:

$$
r = \frac{s}{c + v} = \frac{e v}{c + v}
$$

Divide the top and bottom by $v$:

$$
r = \frac{e}{\frac{c}{v} + 1}
$$

Write $\mathrm{OCC} = c/v$:

$$
r = \frac{e}{1 + \mathrm{OCC}}
$$

**What it shows.** If $e$ stays fixed and $\mathrm{OCC}$ rises, $r$ falls. This is the arithmetic behind the tendency of the rate of profit to fall. Rising exploitation and cheaper machinery can offset it, so it is a tendency and not a forecast.

**Example.** With $e = 100\%$:

$$
\mathrm{OCC} = 1: \quad r = \frac{1}{1 + 1} = 50\%
$$

$$
\mathrm{OCC} = 3: \quad r = \frac{1}{1 + 3} = 25\%
$$

## 7. Prices of production

Competition pushes capital towards higher returns, so industries tend towards a common rate of profit. Add up all surplus value and all capital advanced:

$$
r = \frac{\sum_i s_i}{\sum_i (c_i + v_i)}
$$

Each industry's price of production is its costs plus the average profit:

$$
p_i = (c_i + v_i)(1 + r)
$$

**Example 7.1.** Industry A has $c = 50$, $v = 100$, $s = 100$. Industry B has $c = 150$, $v = 100$, $s = 100$.

$$
r = \frac{100 + 100}{150 + 250} = 50\%
$$

$$
p_A = 150 \times 1.5 = 225
$$

$$
p_B = 250 \times 1.5 = 375
$$

The values are $w_A = 250$ and $w_B = 350$. So A sells 25 below value and B sells 25 above it, and total price equals total value at 600. This is a simplified illustration. It leaves the inputs valued at their values, which is the subject of the long debate known as the transformation problem.

## Worked example: Sialkot footballs

This example combines published figures from different sources and years, so it is an illustration and not the accounts of one firm.

**Time wage from a piece rate.** At PKR 160 a ball and 3 hours a ball:

$$
w_{\text{hour}} = \frac{160}{3} \approx 53.33 \text{ PKR per hour}
$$

**Costs per ball.** The cost table gives:

$$
c = 154.52, \qquad v = 56.29
$$

$$
c + v = 210.81
$$

The source reports a total of 210.83, and the difference is rounding in its table.

**Profit at this stage.** A reported margin of 8.1% on the reported total gives:

$$
p = 210.83 \times 1.081 \approx 227.91
$$

$$
\text{profit} = 227.91 - 210.83 = 17.08
$$

**Profit over wages.**

$$
\frac{17.08}{56.29} \approx 30.3\%
$$

**What this does and does not show.** It shows how these categories work with real figures. It is not a measured rate of exploitation, because reported profit is only a stand-in for surplus value, and it covers one stage of a long chain. The pay and cost figures also come from different studies: the cost table's stitching cost of PKR 39.24 differs from the reported PKR 160 piece rate.

The [full working](examples/sialkot.md) goes further. The pamphlet uses the same figures in [section 5.8](chapters/05-labour-power-wages-surplus-labour-and-surplus-value.md#subsec-sialkot-football-stitching).

## Using the Python code

```bash
git clone https://github.com/AhmadAmmar/marxist-economics
cd marxist-economics
python -m marxian rates --c 100 --v 100 --s 100
python -m marxian industries 50,100,100 150,100,100
```

The second command prints the Example 7.1 results above. The tests in `tests/test_model.py` check the functions against the pamphlet's examples.

Found a mistake? [Report it here](contribute.md).
