# Rate of profit and organic composition of capital

The **rate of profit** is the central ratio from the capitalist point
of view. It measures the surplus value obtained per unit of total capital
advanced:

\begin{equation}
  r = \frac{s}{c + v}.
  
\end{equation}

From the definition of the exploitation rate in Eq.~\eqref{eq:exploitation-time},
\(e = s/v\), we have \(s = e v\), so we can rewrite the rate of profit as
\begin{equation}
  r = \frac{e v}{c + v}
    = \frac{e}{1 + c/v}
    = \frac{e}{1 + \organiccomp},
  
\end{equation}

where \(\organiccomp = c/v\) is the organic composition of capital.

## Illustration: varying the organic composition

Suppose, for simplicity, that the exploitation rate is fixed at
$\exploitrate = 100\%$, i.e.\ $\surplus = \varcap$, and set $\varcap=100$
as a numéraire. We examine what happens to $\profitrate$ as the ratio
$\constcap/\varcap$ rises.

\begin{tabular}{@{}lrrr@{}}
\toprule
$c/v$ & $c$ & $s$ & $r = \dfrac{s}{c+v}$ 

\midrule
$0.5$ & $50$  & $100$ & $\approx 66.7\%$ 

$1.0$ & $100$ & $100$ & $50.0\%$        

$2.0$ & $200$ & $100$ & $\approx 33.3\%$ 

$4.0$ & $400$ & $100$ & $20.0\%$        

$8.0$ & $800$ & $100$ & $\approx 11.1\%$ 

\bottomrule
\end{tabular}

Even with a constant rate of exploitation $e = s/v = 100\%$, the rate of profit $r$ falls as capital becomes more “machine-heavy” relative to wages (as the ratio $c/v$ rises). This logical connection between a rising organic composition of capital $c/v$ and a falling profit rate $r$ is at the heart of Marx’s *law of the tendency of the rate of profit to fall* (TRPF).[Roberts2015,Shaikh2016]

## Competition, average profit, and prices of production

So far we have treated $\surplus$ and $\profitrate$ at the level of production:
surplus value is produced where living labour is set to work, and the profit rate
is $\profitrate = \surplus/(\constcap+\varcap)$ (Eq.~\eqref{eq:profit-rate-basic}).
But on the surface of capitalist society, capitals do not simply pocket the surplus
they individually produce. They compete, they move, and they compare returns.
This movement produces a *tendency* toward an *average* rate of profit.

To formalise this, index industries (or branches of production) by $i$.
Let the capital advanced in industry $i$ be $(\constcap_i + \varcap_i)$.
Assume, for clarity, that the *rate of exploitation* is uniform across industries,
so that in each industry
$$
\surplus_i = \exploitrate\,\varcap_i.
$$
Then the **value** (in money terms) of the industry's output (at this level of abstraction)
can be written as
\begin{equation}
  w_i = \constcap_i + \varcap_i + \surplus_i
      = \constcap_i + (1+\exploitrate)\,\varcap_i.
  
\end{equation}

Define the **cost price** (capital advanced that must be replaced) as
\begin{equation}
  k_i = \constcap_i + \varcap_i.
  
\end{equation}

Total surplus value and total capital advanced are
$$
\surplus = \sum_i \surplus_i,
  \qquad
  K = \sum_i (\constcap_i + \varcap_i) = \sum_i k_i.
$$
Competition tends to equalise profit rates, so the **average rate of profit** is
\begin{equation}
  \profitrate = \frac{\surplus}{K}.
  
\end{equation}

Under this tendency, the regulating price is not the direct value $w_i$ but the
**price of production**, which yields the average profit on the capital advanced:
\begin{equation}
  p_i = k_i(1+\profitrate) = (\constcap_i + \varcap_i)(1+\profitrate).
  
\end{equation}
The profit *received* by industry $i$ is therefore
$$
\pi_i = p_i - k_i = \profitrate\,k_i = \profitrate(\constcap_i+\varcap_i).
$$
Compare this with surplus value *produced* in that industry, $\surplus_i=\exploitrate\varcap_i$.
The difference is
$$
\pi_i - \surplus_i = \profitrate(\constcap_i+\varcap_i) - \exploitrate\varcap_i,
$$
which expresses the redistribution of surplus value across industries through competition.

It is useful to make the dependence on the *organic composition* explicit.
Let $C=\sum_i \constcap_i$ and $V=\sum_i \varcap_i$. With $\surplus=\exploitrate V$ we have
$$
\profitrate = \frac{\surplus}{C+V} = \frac{\exploitrate V}{C+V}
  = \frac{\exploitrate}{1 + C/V}.
$$
Then, using $\Omega = C/V$ as the **average** organic composition, one can show
\begin{equation}
  p_i - w_i
  = \exploitrate\,\varcap_i \,\frac{\big(\constcap_i/\varcap_i\big) - \Omega}{1+\Omega}.
  
\end{equation}
So industries with *above-average* $\constcap_i/\varcap_i$ tend to have $p_i>w_i$
(they receive more profit than the surplus they themselves produce), while those with
*below-average* $\constcap_i/\varcap_i$ tend to have $p_i<w_i$.

\subsubsection*{A two-industry illustration (values vs.\ prices of production)}

!!! example "Example"
    [Two industries and the redistribution of surplus value]
    Assume two industries, $A$ and $B$, with a common exploitation rate $\exploitrate = 100\%$,
    so $\surplus_i = \varcap_i$. Let $\varcap_A=\varcap_B=100$, and let $A$ be lower-composition
    and $B$ higher-composition:
    $$
    \constcap_A=50,\qquad \constcap_B=150.
    $$

    ### Step 1: Surplus value produced and values.

    Since $\exploitrate=100\%$, we have
    $$
    \surplus_A=\varcap_A=100,\qquad \surplus_B=\varcap_B=100.
    $$
    So values (Eq.~\eqref{eq:value-output-industry}) are:
    $$
    w_A=\constcap_A+\varcap_A+\surplus_A=50+100+100=250,\qquad
      w_B=\constcap_B+\varcap_B+\surplus_B=150+100+100=350.
    $$

    ### Step 2: The average profit rate.

    Totals are $C=200$, $V=200$, $\surplus=200$, so the average profit rate is
    $$
    \profitrate=\frac{\surplus}{C+V}=\frac{200}{400}=50\%.
    $$

    ### Step 3: Prices of production and profits received.

    Prices of production (Eq.~\eqref{eq:price-of-production}) are:
    $$
    p_A=(\constcap_A+\varcap_A)(1+\profitrate)=(50+100)(1.5)=225,\qquad
      p_B=(\constcap_B+\varcap_B)(1+\profitrate)=(150+100)(1.5)=375.
    $$
    Profits received are $\pi_i = p_i-(\constcap_i+\varcap_i)=\profitrate(\constcap_i+\varcap_i)$, hence
    $$
    \pi_A=0.5\times 150=75,\qquad \pi_B=0.5\times 250=125.
    $$

    ### Step 4: Who transfers surplus value, and who receives it?

    Industry $A$ sells *below* its value ($225<250$) and receives less profit than the surplus it produces:
    $$
    \pi_A-\surplus_A = 75-100 = -25 \quad\Rightarrow\quad \text{$A$ transfers 25.}
    $$
    Industry $B$ sells *above* its value ($375>350$) and receives more profit than the surplus it produces:
    $$
    \pi_B-\surplus_B = 125-100 = +25 \quad\Rightarrow\quad \text{$B$ receives 25.}
    $$

    
    
    \setlength{\tabcolsep}{6pt}
    \renewcommand{\arraystretch}{1.15}
    
    \begin{tabular}{@{}lrrrrrrr@{}}
    \toprule
    Industry & $c$ & $v$ & $s$ (produced) & $w=c+v+s$ & $k=c+v$ & $p=k(1+\profitrate)$ & $\pi=\profitrate k$ 

    \midrule
    $A$ & 50  & 100 & 100 & 250 & 150 & 225 & 75  

    $B$ & 150 & 100 & 100 & 350 & 250 & 375 & 125 

    \midrule
    Total & 200 & 200 & 200 & 600 & 400 & 600 & 200 

    \bottomrule
    \end{tabular}
    
    

    ### Aggregate identities (the punchline).

    Under these simplifying assumptions,
    $$
    \sum_i p_i = \sum_i w_i,
      \qquad
      \sum_i \pi_i = \sum_i \surplus_i.
    $$
    So prices of production redistribute surplus value; they do not create it. Market prices can
    fluctuate around $p_i$ due to demand, supply, monopoly power, state policy, and world-market
    conditions, but the competitive tendency toward average profit is the key mediating mechanism
    through which labour-time asserts itself in the long run.[Marx1894,Shaikh2016]

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
