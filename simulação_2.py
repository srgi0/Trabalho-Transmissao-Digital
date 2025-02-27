import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# Parâmetros da simulação
M = 256                      # Ordem da modulação PSK (potência de 2)
N_bits = 10**6             # Número aproximado de bits
EbN0_dB_range = np.arange(0, 13, 2)  # Valores de SNR em dB

# 1. Ajustar número de bits para múltiplo de log2(M)
k = int(np.log2(M))
N_bits = (N_bits // k) * k  # Corrige para ser múltiplo exato

# 2. Gerar mapeamento Gray para M-PSK
gray_code = np.array([np.binary_repr(i ^ (i >> 1), width=k)
                     for i in range(M)])

# 3. Funções auxiliares
def theoretical_ser(EbN0_lin, M):
    EsN0_lin = EbN0_lin * np.log2(M)
    return 2 * 0.5*(1 - erf(np.sqrt(EsN0_lin)*np.sin(np.pi/M)/np.sqrt(2)))

def theoretical_ber(EbN0_lin, M):
    return theoretical_ser(EbN0_lin, M)/np.log2(M)

# 4. Simulação Monte Carlo
ser_sim = []
ber_sim = []

for EbN0_dB in EbN0_dB_range:
    # Conversão de dB para linear
    EbN0_lin = 10**(EbN0_dB/10)
    EsN0_lin = EbN0_lin * np.log2(M)
    N0 = 1/EsN0_lin

    # Geração de bits e reshape
    bits = np.random.randint(0, 2, N_bits)
    symbols = bits.reshape(-1, k)

    # Conversão para símbolos decimais
    dec_symbols = np.packbits(symbols, axis=1, bitorder='little').flatten()
    dec_symbols = np.right_shift(dec_symbols, 8 - k)  # Ajuste para k bits

    # Geração do sinal PSK
    tx_phase = 2*np.pi*dec_symbols/M
    tx_signal = np.exp(1j*tx_phase)

    # Adição de ruído
    noise = np.sqrt(N0/2)*(np.random.randn(len(tx_signal)) + 1j*np.random.randn(len(tx_signal)))
    rx_signal = tx_signal + noise

    # Demodulação
    rx_phase = np.angle(rx_signal) % (2*np.pi)
    dec_rx = np.round(rx_phase*M/(2*np.pi)).astype(int) % M

    # Cálculo de erros
    ser = np.mean(dec_rx != dec_symbols)

    # Cálculo de BER usando Gray code
    tx_bits = np.array([list(gray_code[s]) for s in dec_symbols]).flatten().astype(int)
    rx_bits = np.array([list(gray_code[s]) for s in dec_rx]).flatten().astype(int)
    ber = np.mean(rx_bits != tx_bits)

    ser_sim.append(ser)
    ber_sim.append(ber)

# 5. Cálculo das curvas teóricas
EbN0_lin_range = 10**(EbN0_dB_range/10)
theory_ser = [theoretical_ser(e, M) for e in EbN0_lin_range]
theory_ber = [theoretical_ber(e, M) for e in EbN0_lin_range]

# 6. Plot dos resultados
plt.figure(figsize=(12, 6))

# Curva SER
plt.subplot(121)
plt.semilogy(EbN0_dB_range, theory_ser, 'r-', label='Teórico')
plt.semilogy(EbN0_dB_range, ser_sim, 'b--o', label='Simulado')
plt.title(f'Probabilidade de Erro de Símbolo (M={M})')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('SER')
plt.grid(True)
plt.legend()

# Curva BER
plt.subplot(122)
plt.semilogy(EbN0_dB_range, theory_ber, 'r-', label='Teórico')
plt.semilogy(EbN0_dB_range, ber_sim, 'b--o', label='Simulado')
plt.title(f'Probabilidade de Erro de Bit (M={M})')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()