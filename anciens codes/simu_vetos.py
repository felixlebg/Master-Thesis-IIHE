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
t_ccs = 3
n_files = 100            # Nombre de fichiers simulées

file_dividing = 100
dt_max = 10e-6

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
    outfile = open(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/{filling}/out_simu_vetos_file{i+1}.txt", "w")
    simu_ccsn = open_file(["ccsn", filling], i)

    try:
        root_simu_ccsn = TFile.Open(simu_ccsn,"READ")
    except:
        n_error += 1
        print(f"Error opening file {simu_ccsn}")
        continue
    
    cd_evt_l, wp_evt_divided = sub_list(root_simu_ccsn, file_dividing, dt_max)
    
    # Optension des temps des événements simulation supernova
    dt = 1
    t_prev = 0
    for j in range(len(cd_evt_l)):
        cd_evt = cd_evt_l[j]
        correl = False

        # weight
        t_evt = cd_evt[2]  # temps auquel s'est produit la détection
        if t_prev != 0:
            dt =  t_evt - t_prev
        t_prev = t_evt 

        # veto 1
        if abs(dt) < 25e-6:
            continue

        # range en énergie optimal pour discriminer les neutrinos 
        #npe = cd_evt.npe_tot
        #if npe < npe_min or npe > npe_max:
        #    continue

        # veto 2
        if len(wp_evt_divided) == 1:
            index = 0
        else:
            index = int(j*file_dividing/int(len(cd_evt_l)))
        for wp_evt in wp_evt_divided[index]:  # coïncidences avec les muons de la waterpool
            wp_t = wp_evt[1]
            dt_wp = wp_t - t_evt
            if abs(dt_wp) < dt_max and wp_evt[0] > 1000:
                correl = True
                break

        if not correl:
            print(cd_evt[0], cd_evt[1], t_evt, cd_evt[3], file=outfile)
    
    weight = 1/(t_ccs*(n_files - n_error))
    print("simu", weight, "vetos", file=outfile)
    outfile.close()
