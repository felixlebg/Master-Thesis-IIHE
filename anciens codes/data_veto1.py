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

# Initialisation
n_error = 0
t_data = 0

for i in range(n_files):
    t_prev = 0
    outfile = open(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data_veto1_run{run}_file{i+1}.txt", "w")
    data = open_file(["data", run], i)
        
    try:
        root_data =  TFile.Open(data,"READ")
        # root_simu_muons = TFile.Open(simu_muons,"READ")
    except:
        n_error += 1
        print(f"Error opening file {data}")
        continue

    # Optension des temps des événements du bruit de fond
    dt = 1
    for cd_evt in root_data.cd_events:
        correl = False

        # weight
        t_evt = cd_evt.t_ns*1e-9 + cd_evt.t_sec  # temps auquel s'est produit la détection
        if t_prev != 0:
            dt =  t_evt - t_prev
            t_data += dt
        t_prev = t_evt 

        # veto 1
        if abs(dt) < 25e-6:
            continue

        # range en énergie optimal pour discriminer les neutrinos 
        #npe = cd_evt.npe_tot
        #if npe < npe_min or npe > npe_max:
        #    continue
        
        if run > 4330:
            print(cd_evt.npe_tot, cd_evt.nhits, t_evt, cd_evt.vz, file=outfile)
        else:
            print(cd_evt.npe_tot, cd_evt.nhits, t_evt, file=outfile)
            
    weight = 1/t_data
    print(run, weight, "veto1", file=outfile)
    outfile.close()