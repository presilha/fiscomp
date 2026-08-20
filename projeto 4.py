#O presente código refere-se ao projeto feito durante a disciplina de física computacional. 
#A ideia é tentar simular a aleatorieade, dado a natureza deterministica da máquina, e com isso conseguir plotar um gráfico da evolução temporal do ruído (beta_0)



import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

class LCG: 
    def __init__(self, seed=42, a=1103515245, c=12345, m=2**31):
        self.a = a
        self.b = c
        self.m = m
        self.state = seed % m

    def uniform(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m
    def sample(self, n):
        return [self.uniform() for _ in range(n)]

def uniform_deviation(u, low=-0.02, high=0.02):
    return low + (high - low)*u

beta0 = 1.2         #mev^-1
N = 500             #núemro de pontos da evolução temporal
dt = 0.01           #passo temporal

gen = LCG(seed=12345)

u_values = gen.sample(N)
deltas = [uniform_deviation(u) for u in u_values]

t = [i*dt for i in range(N)]
beta_t = [beta0 + d for d in deltas]

media = sum(beta_t)/N
variancia = (sum(b - media) **2 for b in beta_t)/N
desvio_padrao = variancia ** 0.5

print(f"Média de beta(t)      : {media:.5f} meV^-1  (esperando - {beta0})")
print(f"Desvio padrão : {desvio_padrao:.5f}")
print(f"Mínimo/Máximo   : {min(beta_t):.5f}/{max(beta_t):.5f}")

plt.figure(figsize=(9, 4.5))
plt.plot(t, beta_t, color="#1f77b4", linewidth=0.9)
plt.axhline(beta0, color="black", linestyle="--", linewidth=1, label=r"$\beta_0 = 1.2$ meV$^{-1}$")
plt.fill_between(t, beta0 - 0.02, beta0 + 0.02, color="gray", alpha=0.15, label="Faixa de ruído $[-0.02, 0.02]$")
plt.xlabel("t (s)")
plt.ylabel(r"$\beta(t)$ (meV$^{-1}$)")
plt.title(r"Flutuação térmica estocástica de $\beta(t) = \beta_0 + \delta_i$ via LCG manual")
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("/home/claude/beta_ruidoso.png", dpi=150)
plt.show()