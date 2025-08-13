# Ce script permet d'écrire dans une liste les charges des données réelles en appliquant le veto 2

import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
from ROOT import TFile, TTree, TH1
import os
import sys
from functions import*



# Paramètres de simulation
n_files = 2000            # Nombre de fichiers simulées

run = int(sys.argv[1])

file_dividing = 1000
dt_max_veto1 = 60e-6
dt_max_veto2 = 10e-6


minE_muons = 10000  # en pe
minE_wp = 100  # en pe


# vetos
veto = "_veto2"
#veto = ""

if veto == "_veto1":
    veto1 = True
    veto2 = False
    veto_print = "veto1"
elif veto == "_veto2":
    veto1 = False
    veto2 = True
    veto_print = "veto2"
elif veto == "_vetos":
    veto1 = True
    veto2 = True
    veto_print = "vetos"
elif veto == "":
    veto1 = False
    veto2 = False
    veto_print = "noveto"


# Initialisation
n_error = 0
t_data = 0
Error_file_dividing = 0

data0 = open_file(["data", run], 0)
root_file0=TFile.Open(data0,"READ")
root_file0.cd_events.GetEntry(0)
date = root_file0.cd_events.m_date
date = str(date)
date = f"{date[6:8]}/{date[4:6]}/{date[0:4]}"

for i in range(n_files):
    outfile = open(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data{veto}_run{run}_file{i+1}.txt", "w")
    data = open_file(["data", run], i)

    
    try:
        root_data =  TFile.Open(data,"READ")
        # root_simu_muons = TFile.Open(simu_muons,"READ")
    except:
        n_error += 1
        print(f"Error opening file {data}")
        if n_error > 50:
            print("Too many errors opening files, exiting.")
            break
        continue

    cd_evt_l, wp_t_divided = sub_list(root_data, file_dividing, minE_wp)


    # Optension des temps des événements du bruit de fond
    t_prev = 0
    t_last_mu = 0
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
        if veto1: 
            dt_veto1 = t_evt - t_last_mu  # temps entre la détection actuelle et la dernière détection de muon
            if abs(dt_veto1) < dt_max_veto1:  # on ne garde que les événements avec plus de 1000 hits
                continue

            if cd_evt[0] > minE_muons:
                t_last_mu = t_evt  # on garde le temps du dernier muon détecté

        # range en énergie optimal pour discriminer les neutrinos (on laisse en commentaire pour mieux visualiser la meilleure zone)
        #if cd_evt.npe_tot < npe_min or cd_evt.npe_tot > npe_max:
        #    continue

        # veto 2
        if veto2:
            if len(wp_t_divided) == 1:
                index = 0
                wp_evt_i = wp_t_divided[index]
            else:
                if t_evt > wp_t_divided[-1][-1] - dt_max_veto2:
                    index = len(wp_t_divided) - 1
                    wp_evt_i = wp_t_divided[index]
                elif t_evt < wp_t_divided[0][0] + dt_max_veto2:
                    index = 0
                    wp_evt_i = wp_t_divided[index]
                else:
                    for k, wp_evt_i in enumerate(wp_t_divided):
                        if wp_evt_i[0] - dt_max_veto2 <= t_evt <= wp_evt_i[-1] + dt_max_veto2:
                            index = k
                    wp_evt_i = wp_t_divided[index]

                    # Vérification de la méthode file dividing 
                    if len(wp_evt_i) > 0 and (t_evt < wp_evt_i[0] - dt_max_veto2 or t_evt > wp_evt_i[-1] + dt_max_veto2):
                        Error_file_dividing += 1
                        print(t_evt-1748006790, wp_evt_i[0]-1748006790, wp_evt_i[-1]-1748006790)

            # Vérification de la coïncidence avec les muons de la waterpool
            for wp_t in wp_evt_i:  # coïncidences avec les muons de la waterpool
                dt_wp = wp_t - t_evt
                if abs(dt_wp) < dt_max_veto2 and cd_evt[0] > minE_muons:
                    t_last_mu = t_evt  # on garde le temps du dernier muon détecté
                    correl = True
                    break

        if not correl:
            if run > 4330:
                print(cd_evt[0], cd_evt[1], t_evt, cd_evt[3], file=outfile)
            else:
                print(cd_evt[0], cd_evt[1], t_evt, file=outfile)

    weight = 1/t_data
    print(run, weight, veto_print, date, file=outfile)
    outfile.close()

print(f"Error in File Dividing: {Error_file_dividing}")
