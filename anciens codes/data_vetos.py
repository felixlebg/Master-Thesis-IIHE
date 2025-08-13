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
# runs = [3322, 3323, 3326]  # Full water
#runs = [4332, 4333, 4334, 4335] # LS Filling 20%
run = int(sys.argv[1])
file_dividing = 100
dt_max = 10e-6

# Initialisation
n_error = 0
t_data = 0

# vetos

for i in range(n_files):
    t_prev = 0
    outfile = open(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data_vetos_run{run}_file{i+1}.txt", "w")
    data = open_file(["data", run], i)

    try:
        root_data =  TFile.Open(data,"READ")
        # root_simu_muons = TFile.Open(simu_muons,"READ")
    except:
        n_error += 1
        print(f"Error opening file {data}")
        continue

    cd_evt_l, wp_evt_divided = sub_list(root_data, file_dividing, dt_max)
    
    #print(cd_evt_l[:10])
    #print(wp_evt_divided[0][:10])  # les temps dans la waterpool ne correspondent pas bien aux temps dans le cd

    # Optension des temps des événements du bruit de fond
    dt = 1
    for j in range(len(cd_evt_l)):
        cd_evt = cd_evt_l[j]
        correl = False

        # weight
        t_evt = cd_evt[2]  # temps auquel s'est produit la détection
        if t_prev != 0:
            dt =  t_evt - t_prev
            t_data += dt
        t_prev = t_evt 

        # veto 1
        if abs(dt) < 25e-6:
            continue

        # range en énergie optimal pour discriminer les neutrinos (on laisse en commentaire pour mieux visualiser la meilleure zone)
        #if cd_evt.npe_tot < npe_min or cd_evt.npe_tot > npe_max:
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
            if run > 4330:
                print(cd_evt[0], cd_evt[1], t_evt, cd_evt[3], file=outfile)
            else:
                print(cd_evt[0], cd_evt[1], t_evt, file=outfile)

            
    weight = 1/t_data
    print(run, weight, "vetos", file=outfile)
    outfile.close()
