import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Définir la fonction à tracer
def two_flavors_oscill(L, E):
    return np.sin(2*2*pi*33.68/360)**2*np.sin(1.27*7.49e-5*L/E)**2

def three_flavors_oscill(L, E):
    P_slow = np.sin(2*2*pi*33.68/360)**2*np.cos(2*pi*8.56/360)**4*np.sin(1.27*7.49e-5*L/E)**2
    P_fast = np.sin(2*2*pi*8.56/360)**2*np.sin(1.27*2.513e-3*L/E)**2
    return 1-P_slow-P_fast, 1-P_slow, 1-P_fast


# Créer un ensemble de points x
x = np.linspace(0, 300, 500)  # de 0 à 300 avec 500 points

# Calculer les valeurs de la fonction
E0 = 3e-3
# 2 flavors oscillation
two_flavors_oscill_plot = two_flavors_oscill(x, E0)
survival_probability = 1 - two_flavors_oscill_plot

plt.figure(figsize=(8, 4))
plt.plot(x, two_flavors_oscill_plot, label=r'$P_{\nu_e \rightarrow \nu_\mu}$', color='blue')
plt.plot(x, survival_probability, label=r'$P_{\nu_e \rightarrow \nu_e}$', color='orange')
plt.xlabel('L (km)')
plt.ylabel('Oscillation probability')
plt.title('Oscillation probability with respect to distance L for a given energy')
plt.legend()
plt.grid(True)
plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/2flavor_oscillation.png", dpi=300)
plt.close()

# 3 flavors oscillation
x = np.linspace(0, 120, 500)  # de 0 à 300 avec 500 points
three_flavors_oscill_plot, slow, fast = three_flavors_oscill(x, E0)

plt.figure(figsize=(8, 4))
plt.plot(x, three_flavors_oscill_plot, label=r'$P_{\nu_e \rightarrow \nu_e}$', color='blue')
plt.plot(x, slow, label=r'slow', color='red')
plt.plot(x, fast, label=r'fast', color='green')
plt.title('Oscillation probability in the slow/fast approximation')
plt.xlabel('L (km)')
plt.ylabel('Oscillation probability')
plt.legend()
plt.grid(True)
plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/3flavor_oscillation.png", dpi=300)
plt.close()
