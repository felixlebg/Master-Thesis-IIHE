from functions import read_file_display
import matplotlib.pyplot as plt
import numpy as np
import sys


def npe_nhits(files, filling):
    npe_list, _, _, _ = read_file_display(files, "npe")
    nhits_list, _, _, veto = read_file_display(files, "nhits")

    
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(npe_list, nhits_list, alpha=0.5, s=1)

    ax.set_xlabel('Number of Photoelectrons (npe)', fontsize=18)
    ax.set_ylabel('Number of hits (nhits)', fontsize=18)
    ax.set_title('Correlation between npe and nhits', fontsize=18)
    
    # Compute percentiles to focus on the central 98% of points
    npe_min, npe_max = np.percentile(npe_list, [0.2, 100])
    nhits_min, nhits_max = np.percentile(nhits_list, [0.2, 100])

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(npe_min, npe_max)
    ax.set_ylim(nhits_min, nhits_max)
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/npe_nhits_{filling}_{veto}.png", dpi=300)

    
    return fig, ax


# Paramètres
#v = "_vetos"
v = ""
run = int(sys.argv[1])
filling = "half"
number_of_files = 10


files_data = []
for i in range(number_of_files):
    files_data.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data{v}_run{run}_file{i + 1}.txt")


npe_nhits(files_data, filling)

