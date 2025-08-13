# Ce script permet d'écrire dans une liste les charges des données réelles en appliquant le veto 2

import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
from ROOT import TFile, TTree, TH1
import os
import sys
from functions import*


# Paramètres de simulation
npe_min = 1e4
npe_max = 1e5
n_files = 100            # Nombre de fichiers simulées
t_ccs = 3

filling = int(sys.argv[1])
if filling == 0:
    filling = "water"
elif filling == 1:
    filling = "half"
elif filling == 2:
    filling = "LS"

# Initialisation
n_error = 0

for i in range(n_files):
    outfile = open(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/{filling}/out_simu_file{i+1}.txt", "w")
    simu_ccsn = open_file(["ccsn", filling], i)

    try:
        root_simu_ccsn = TFile.Open(simu_ccsn,"READ")
    except:
        n_error += 1
        print(f"Error opening file {simu_ccsn}")
        continue

    # Optension des temps des événements simulation supernova
    for cd_evt in root_simu_ccsn.cd_events:
        t_evt = cd_evt.t_ns*1e-9 + cd_evt.t_sec  # temps auquel s'est produit la détection

        # range en énergie optimal pour discriminer les neutrinos 
        #npe = cd_evt.npe_tot
        #if npe < npe_min or npe > npe_max:
        #    continue

        print(cd_evt.npe_tot, cd_evt.nhits, t_evt, cd_evt.vz, file=outfile)
            
    weight = 1/(t_ccs*(n_files - n_error))
    print("simu", weight, "noveto", file=outfile)
    outfile.close()