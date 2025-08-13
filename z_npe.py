# ce script vise à démontre que les pics à 2e5 et 2e6 npe sont dues à des interactions dans un milieu différent
# cad soit eau soit LS en montrant le z d'interaction en fonction du nombre de npe générés
import matplotlib.pyplot as plt
import numpy as np

run = 4418
n_files = 20
min_charge = 1e5
max_charge = 1e7
npe = []
z = []
veto = "_veto1"
veto = ""
for i in range(n_files):
    file = f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data{veto}_run{run}_file{i + 1}.txt"
    with open(file, "r") as f:  
        lines = f.readlines()
        if len(lines) == 0:
                continue 

        for i in range(len(lines) - 1):
            line = lines[i]
            data = line.strip().split() 
            if float(data[0]) > min_charge:
                z.append(float(data[3]))
                npe.append(float(data[0]))


# Plot
plt.figure(figsize=(8, 5))
#plt.scatter(npe, z, color='dodgerblue', alpha=0.7)
binsx = np.logspace(np.log10(min_charge), np.log10(max_charge), 200)
binsy = np.linspace(-15000,15000,200)
plt.hist2d(npe, z, bins=(binsx,binsy))
plt.xscale('log')  # Axe x en échelle logarithmique
plt.colorbar()
plt.xlabel("Number of photoelectrons [log]")
plt.ylabel("Height of interaction (mm)")
plt.title("Distribution of interaction in JUNO")
plt.grid(True)

plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/z_npe{veto}_{run}_{n_files}files.png", dpi=300, bbox_inches='tight')
