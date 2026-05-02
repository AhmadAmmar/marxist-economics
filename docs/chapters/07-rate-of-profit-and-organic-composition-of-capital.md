# Rate of profit and organic composition of capital

%=========================================================

The **rate of profit} is the central ratio from the capitalist point
of view. It measures the surplus value obtained per unit of total capital
advanced:

$$
  r = \frac{s}{c + v}.
  
$$


From the definition of the exploitation rate in Eq.~\eqref{eq:exploitation-time},
\(e = s/v\), we have \(s = e v\), so we can rewrite the rate of profit as
$$
  r = \frac{e v}{c + v}
    = \frac{e}{1 + c/v}
    = \frac{e}{1 + \organiccomp},
  
$$

where \(\organiccomp = c/v\) is the organic composition of capital.




## Illustration: varying the organic composition


Suppose, for simplicity, that the exploitation rate is fixed at
$\exploitrate = 100%$, i.e.\ $\surplus = \varcap$, and set $\varcap=100$
as a numéraire. We examine what happens to $\profitrate$ as the ratio
$\constcap/\varcap$ rises.

\begin{center}
\begin{tabular}{@{}lrrr@{}}
\toprule
$c/v$ & $c$ & $s$ & $r = \dfrac{s}{c+v}$ \\
\midrule
$0.5$ & $50$  & $100$ & $\approx 66.7%$ \\
$1.0$ & $100$ & $100$ & $50.0%$        \\
$2.0$ & $200$ & $100$ & $\approx 33.3%$ \\
$4.0$ & $400$ & $100$ & $20.0%$        \\
$8.0$ & $800$ & $100$ & $\approx 11.1%$ \\
\bottomrule
\end{tabular}
\end{center}

Even with a constant rate of exploitation $e = s/v = 100%$, the rate of profit $r$ falls as capital becomes more “machine-heavy” relative to wages (as the ratio $c/v$ rises). This logical connection between a rising organic composition of capital $c/v$ and a falling profit rate $r$ is at the heart of Marx’s *law of the tendency of the rate of profit to fall} (TRPF).[Roberts2015,Shaikh2016]


## Competition, average profit, and prices of production



So far we have treated $\surplus$ and $\profitrate$ at the level of production:
surplus value is produced where living labour is set to work, and the profit rate
is $\profitrate = \surplus/(\constcap+\varcap)$ (Eq.~\eqref{eq:profit-rate-basic}).
But on the surface of capitalist society, capitals do not simply pocket the surplus
they individually produce. They compete, they move, and they compare returns.
This movement produces a *tendency} toward an *average} rate of profit.

\paragraph{Three related levels: values, prices of production, market prices.}
It helps to be explicit about three levels of analysis that are often conflated in casual discussion:

[leftmargin=1.5em]
  - **Values} express socially necessary labour time (in this pamphlet, expressed in money via the simplifying convention stated earlier). At this level, for industry $i$,
  \[
    w_i = \constcap_i + \varcap_i + \surplus_i.
  \]
  - **Prices of production} are the *regulating} prices associated with competitive equalisation of profit rates. At this level,
  \[
    p_i = k_i(1+\profitrate), \qquad k_i = \constcap_i + \varcap_i.
  \]
  - **Market prices} are the actual prices paid on the day. They deviate from regulating prices of production due to supply and demand fluctuations, credit conditions, state policy, and monopoly power; in competitive conditions they tend to oscillate around regulating prices, but in many real markets they can be persistently displaced.


When we do simple arithmetic in earlier sections (for example the smartphone example), we are effectively working at level (1)---as if market prices coincided with values---to keep the exploitation relation transparent.
In this section we introduce level (2) to show that even without fraud, ``overcharging,'' or an individual capitalist ``being greedy,''
competition redistributes surplus value across capitals, generating systematic deviations between $w_i$ and $p_i$.

To formalise this, index industries (or branches of production) by $i$.
Let the capital advanced in industry $i$ be $(\constcap_i + \varcap_i)$.
Assume, for clarity, that the *rate of exploitation} is uniform across industries,
so that in each industry
\[
  \surplus_i = \exploitrate\,\varcap_i.
\]
Then the **value} (in money terms) of the industry's output (at this level of abstraction)
can be written as
$$
  w_i = \constcap_i + \varcap_i + \surplus_i
      = \constcap_i + (1+\exploitrate)\,\varcap_i.
  
$$
Here $w_i$ is the value of output expressed in money terms (under the simplifying convention stated earlier),
not yet a regulating competitive price. In other words, $w_i$ belongs to level (1) above.

Define the **cost price} (capital advanced that must be replaced) as
$$
  k_i = \constcap_i + \varcap_i.
  
$$
The cost price $k_i$ is the relevant base for competitive profit comparison: capitals compare returns on the total capital they advance,
not only on the variable capital that purchases labour-power.

Total surplus value and total capital advanced are
\[
  \surplus = \sum_i \surplus_i,
  \qquad
  K = \sum_i (\constcap_i + \varcap_i) = \sum_i k_i.
\]
Competition tends to equalise profit rates, so the **average rate of profit} is
$$
  \profitrate = \frac{\surplus}{K}.
  
$$
This is the regulating (tendential) profit rate generated by the movement of capitals.
It is not an *ethical} average but a competitive one: capitals flow away from below-average returns and into above-average returns,
pressuring outcomes toward the social average.

Under this tendency, the regulating price is not the direct value $w_i$ but the
**price of production}, which yields the average profit on the capital advanced:
$$
  p_i = k_i(1+\profitrate) = (\constcap_i + \varcap_i)(1+\profitrate).
  
$$
The profit *received} by industry $i$ is therefore
\[
  \pi_i = p_i - k_i = \profitrate\,k_i = \profitrate(\constcap_i+\varcap_i).
\]
Compare this with surplus value *produced} in that industry, $\surplus_i=\exploitrate\varcap_i$.
The difference is
\[
  \pi_i - \surplus_i = \profitrate(\constcap_i+\varcap_i) - \exploitrate\varcap_i,
\]
which expresses the redistribution of surplus value across industries through competition.
In Marx's terms: surplus value is produced in production by living labour, but it is distributed across capitals through competition,
so that each capital tends to receive profit proportional to the total capital it advances, not proportional to the surplus it directly produces.

It is useful to make the dependence on the *organic composition} explicit.
Let $C=\sum_i \constcap_i$ and $V=\sum_i \varcap_i$. With $\surplus=\exploitrate V$ we have
\[
  \profitrate = \frac{\surplus}{C+V} = \frac{\exploitrate V}{C+V}
  = \frac{\exploitrate}{1 + C/V}.
\]
Then, using $\Omega = C/V$ as the **average} organic composition, one can show
$$

p_i - w_i
=
\frac{\exploitrate\,\varcap_i}{1+\Omega}
\left(
  \frac{\constcap_i}{\varcap_i}-\Omega
\right).
$$
So industries with *above-average} $\constcap_i/\varcap_i$ tend to have $p_i>w_i$
(they receive more profit than the surplus they themselves produce), while those with
*below-average} $\constcap_i/\varcap_i$ tend to have $p_i<w_i$.

\paragraph{Scope note (what this example abstracts from).}
Under these simplifying assumptions,\footnote{We abstract from fixed capital turnover-time differences, depreciation schedules,
joint production, rent and taxation, credit and interest, state subsidies, and open-economy complications (exchange rates, tariffs,
and persistent monopoly power). These matter greatly for how value magnitudes map onto observed accounting categories, but they do
not change the core point demonstrated here: surplus value is produced by living labour in production and then redistributed through
competition and further shaped by credit and state power.}
the logic is sharp: equalisation of profit rates implies systematic divergences between the value of output $w_i$ and the regulating
competitive price $p_i$, even when each industry's exploitation rate is assumed the same. This is why observed profit in a given sector
cannot be read off as ``the surplus produced here'' without specifying the level of abstraction and the redistribution mechanisms.


### A two-industry illustration (values vs.\ prices of production)


\begin{example}[Two industries and the redistribution of surplus value]
Assume two industries, $A$ and $B$, with a common exploitation rate $\exploitrate = 100%$,
so $\surplus_i = \varcap_i$. Let $\varcap_A=\varcap_B=100$, and let $A$ be lower-composition
and $B$ higher-composition:
\[
  \constcap_A=50,\qquad \constcap_B=150.
\]

\paragraph{Step 1: Surplus value produced and values.}
Since $\exploitrate=100%$, we have
\[
  \surplus_A=\varcap_A=100,\qquad \surplus_B=\varcap_B=100.
\]
So values (Eq.~\eqref{eq:value-output-industry}) are:
\[
\begin{aligned}
w_A &= c_A + v_A + s_A = 50 + 100 + 100 = 250,\\
w_B &= c_B + v_B + s_B = 150 + 100 + 100 = 350.
\end{aligned}
\]

\paragraph{Step 2: The average profit rate.}
Totals are $C=200$, $V=200$, $\surplus=200$, so the average profit rate is
\[
  \profitrate=\frac{\surplus}{C+V}=\frac{200}{400}=50%.
\]

\paragraph{Step 3: Prices of production and profits received.}
Prices of production (Eq.~\eqref{eq:price-of-production}) are:
\[
\begin{aligned}
p_A &= (c_A + v_A)(1+r) = (50+100)(1.5) = 225,\\
p_B &= (c_B + v_B)(1+r) = (150+100)(1.5) = 375.
\end{aligned}
\]
Profits received are \(\pi_i = p_i - (c_i+v_i)=r(c_i+v_i)\), hence
\[
\begin{aligned}
\pi_A &= 0.5 \times 150 = 75,\\
\pi_B &= 0.5 \times 250 = 125.
\end{aligned}
\]

\paragraph{Step 4: Who transfers surplus value, and who receives it?}
Industry $A$ sells *below} its value ($225<250$) and receives less profit than the surplus it produces:
\[
  \pi_A-\surplus_A = 75-100 = -25 \quad\Rightarrow\quad \text{$A$ transfers 25.}
\]
Industry $B$ sells *above} its value ($375>350$) and receives more profit than the surplus it produces:
\[
  \pi_B-\surplus_B = 125-100 = +25 \quad\Rightarrow\quad \text{$B$ receives 25.}
\]

\medskip
\begingroup
\setlength{\tabcolsep}{6pt}
\renewcommand{\arraystretch}{1.15}
\begin{center}
\begin{tabular}{@{}lrrrrrrr@{}}
\toprule
Industry & $c$ & $v$ & $s$ (produced) & $w=c+v+s$ & $k=c+v$ & $p=k(1+\profitrate)$ & $\pi=\profitrate k$ \\
\midrule
$A$ & 50  & 100 & 100 & 250 & 150 & 225 & 75  \\
$B$ & 150 & 100 & 100 & 350 & 250 & 375 & 125 \\
\midrule
Total & 200 & 200 & 200 & 600 & 400 & 600 & 200 \\
\bottomrule
\end{tabular}
\end{center}
\endgroup

\paragraph{Aggregate identities (the punchline).}
Under these simplifying assumptions,\footnote{This stylised example abstracts from fixed capital and turnover-time differences, depreciation schedules, joint production, rent, taxes, interest-bearing capital, state subsidies, and open-economy complications (exchange rates, tariffs, unequal exchange). These omissions affect how value magnitudes map onto observed accounting categories and how long-run centres of gravitation are formed, but they do not change the core point established here: surplus value is produced by living labour in production and then redistributed through competition, credit, and state power.}
\[
  \sum_i p_i = \sum_i w_i,
  \qquad
  \sum_i \pi_i = \sum_i \surplus_i.
\]
So prices of production redistribute surplus value; they do not create it. Market prices can
fluctuate around $p_i$ due to demand, supply, monopoly power, state policy, and world-market
conditions, but the competitive tendency toward average profit is the key mediating mechanism
through which labour-time asserts itself in the long run.[Marx1894,Shaikh2016]

\paragraph{Clarifying note on ``asserts itself''.}
Saying that labour-time ``asserts itself'' does not mean that values are directly observable in prices at any moment, nor that there is a frictionless equilibrium.
It means that, through the movement of capitals and the coercive discipline of competition, production is reorganised over time so that
techniques, branch allocations, and capacities are pressured toward the social average, with crises and devaluation as violent moments of rebalancing.
This is why Marx treats prices of production as *mediations}: they are the forms through which the underlying value relations
appear and operate in capitalist reality, not a separate sphere that floats free of production.
\end{example}


## Modern intuition


Think of the evolution of car production. A hundred years ago, producing a
car required many hours of relatively low-mechanisation labour. Today, large
parts of the process are automated: robots weld, paint, and assemble; software
optimises flows. The ratio $\constcap/\varcap$ has risen massively.

At the level of an individual firm, this may boost profits for a while,
because the firm gets ahead of the social average and sells at prices that
embody more labour time than it actually expends. But as the new technology
diffuses, the industry-wide \snlt{} falls, values fall, and competitive
pressures reassert themselves. At a given or even rising exploitation rate,
the long-run tendency is for \profitrate{} to come under pressure.

%=========================================================
