# Uso
- Install Python3.12.3
- Install pip
`python3 -m venv .venv`
`source .venv/bin/activate`
`python3 -m pip install -r requirements.txt`
`python3 simulação_2.py`

# Questão
Considere um sistema M-PSK onde os símbolos transmitidos são representados por números complexos de valor absoluto $1$ e ângulos regularmente espeçados em uma circunferência. Assuma que o código Gray é empregado no mapeamento. Assuma ruído complexo gaussiano com variância $N_0/2$. Plote a probabilidade de erro de símbolo teórica versus a energia média de símbolo por $N_0$. Plote também a probabilidade de erro de bit teórica versus a energia média de bit por $N_0$. Através de simulações de Monte Carlo, emule a transmissão de $N$ bits no sistema acima e calcule a taxa de erro de símbolo versus a energia média de símbolo por $N_0$ e a taxa de erro de bit teórica versus a energia média de bit por $N_0$. Compare a exatidão das curvas obtidas por simulação e as teóricas.

- A taxa de erro de símbolo simulada é comparada com a fórmula teórica:
$$P_s=2Q\left(\sqrt{2E_s/N_0}\cdot sin\left(\frac{\pi}{M}\right)\right)$$
- A taxa de erro de bit teórica é aproximada como:
$$P_b=\frac{P_s}{log_2(M)}$$