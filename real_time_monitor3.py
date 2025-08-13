# Ce script simule le moniteur supernova en temps réel pour déterminer combien d'évenements sont nécessaire
# pour déclancher le trigger supernova par rapport au bruit de fond, en utilisant une méthode de fenetre glissante
import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
import numpy as np
import matplotlib.pyplot as plt
from ROOT import TFile, TTree, TH1
import sys
import json
from functions import read_file_monitor, find_threshold_index
import random


t_start_ccs = 5  # Temps à partir duquel est détectée la supernova

n_ccs = 0  # Nombre de supernova simulées

v = "_vetos"
filling = "75%"
distance = 60  # en kpc
scaling = (20/distance)**2

if filling == "water":
    nhits_min = 100
    nhits_max = 1000
    run = 3322
elif filling == "25%":
    E_range = [[6624.577081663394, 40425.516618294896]]
    runs = [5016, 5017, 5018, 5019, 5020, 5021, 5022, 5023, 
        5044, 5046, 5047, 5048, 5050, 5053, 5054, 5057, 5110, 
        5111, 5115, 5116, 5117, 5119, 5120, 5121, 5122
    ]  # entre 23% et 27% LS
elif filling == "half":
    E_range = [[6624.577081663394, 40425.516618294896]]
    runs = [5946, 5947, 5956, 5957, 5958, 5959, 5961, 5963, 5965, 5970, 5971, 5972, 
        5977, 5985, 5989, 5993, 5994, 5995, 5996, 5999, 6007, 6009, 6010, 
        6011, 6012, 6042, 6043, 6044, 6045, 6046, 6050, 6051, 6052, 6053, 6054, 
        6056, 6060, 6062, 6063, 6064, 6065
    ]  # entre 48% et 52% LS
elif filling == "75%":
    E_range = [[9371.33577171753, 38471.144041726664]]
    runs = [7097, 7099, 7137, 7145, 7146, 7147, 7148, 7246, 7247, 7302, 7317, 7318, 
        7341, 7359, 7360, 7361, 7366, 7373, 7375, 7377, 7378, 7379, 
        7450, 7451, 7602, 7603, 7604, 7688, 7689, 7714, 
        7715, 7716, 7786, 7787, 7788, 7789, 7790, 7880, 7883, 7886, 7897, 7901, 
        7903, 7906, 7908, 7909, 7910
    ]  # à 75% LS
elif filling == "LS":
    nhits_min = 3e3
    nhits_max = 51976.0 + 1 # à adapter
    run = 5540 # à modifier lorsque les runs sont disponibles

#run = int(sys.argv[1])
#runs = [run]


if n_ccs != 0:
    n_data = 0  # Visualisationen temps réel de la supernova -> pas trop de fichiers pour voir l'augmentation plus facilement
else:
    n_data = 2000  # nombre de fichiers par run 

files_ccsn = []
if filling == "75%":
    for i in range(n_ccs):
        if i%2==0:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/half/out_simu_vetos_file{i%100 + 1}.txt")
        else:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/LS/out_simu_vetos_file{i%100 + 1}.txt")
elif filling == "25%":
    for i in range(n_ccs):
        if i%2==0:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/half/out_simu_vetos_file{i%100 + 1}.txt")
        else:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/water/out_simu_vetos_file{i%100 + 1}.txt")
else:
    for i in range(n_ccs):
        files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/{filling}/out_simu_vetos_file{i%100 + 1}.txt")

files_ccsn=[files_ccsn]  # Pour garder la compatibilité avec read_file_monitor


files_data = []
for run in runs:
    files_run = []
    for i in range(n_data):
        files_run.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data{v}_run{run}_file{i+1}.txt")
    files_data.append(files_run)


time_data = []
time_ccsn = []

# Optension des temps des événements du bruit de fond et simulation supernova 
# Read file
ccsn_events, _ = read_file_monitor(files_ccsn)
data_runs, n_data = read_file_monitor(files_data)


if n_data != 0:
    t_prev_evt = 0
    cumulative_pause = 0
    t_prev_end = 0
    for i, data_run in enumerate(data_runs):
        t_start_run = float(data_run[0][2])  # Temps de départ du run
        t_end_run = float(data_run[-1][2])  # Temps de fin du run
        # If there is a gap between the previous run's end and this run's start, accumulate it (plus 2s buffer)
        if t_start_run > t_prev_end:
            cumulative_pause += (t_start_run - t_prev_end)
        else:
            print(f"Error: the start of the run {runs[i]} start before the last event of run {runs[i-1]}")
        # print(f"Time interval between the two runs : {dt_run} seconds")  # ok
        for data_evt in data_run:
            nhits = float(data_evt[1])
            t_evt = float(data_evt[2])
            for nhits_min, nhits_max in E_range:
                if nhits_min < nhits < nhits_max:
                    if abs(t_evt - t_prev_evt) > 70e-6: 
                        # Remove the initial offset and the cumulative pause between runs
                        time_data.append(t_evt - cumulative_pause)
            t_prev_evt = t_evt
        t_prev_end = t_end_run + 2 # On met à jour le temps de départ du run précédent (2sec de battement poru éviter les chevauchements)


t_prev_evt = -1
ccsn_events = ccsn_events[0]
for ccsn_evt in ccsn_events:
    nhits = float(ccsn_evt[1])
    for nhits_min, nhits_max in E_range:
        if nhits > nhits_min and nhits < nhits_max:
            t_evt = float(ccsn_evt[2])
            if abs(t_evt - t_prev_evt) > 70e-6: 
                time_ccsn.append(t_evt+ t_start_ccs)
                t_prev_evt = t_evt

if len(time_ccsn) != 0:
    t_start_ccsn = min(time_ccsn)


if time_data != sorted(time_data):
    print("Warning: time_data is not sorted, sorting it now.")
    time_data = sorted(time_data)
if time_ccsn != sorted(time_ccsn):
    print("Warning: time_ccsn is not sorted, sorting it now.")
    time_ccsn = sorted(time_ccsn)


# Simulation du temps réel
if len(time_data) != 0 and len(time_ccsn) != 0:
    t_end = max(max(time_data), max(time_ccsn))
    t_start = min(min(time_data), t_start_ccsn)
elif len(time_data) != 0:
    t_end = max(time_data)
    t_start = min(time_data)
elif len(time_ccsn) != 0:
    t_end = max(time_ccsn)
    t_start = min(time_ccsn)
else:
    print("Error: No data or CCSN events found.")

if len(runs) != 1:
    run=f"{runs[0]}-{runs[-1]}"

print(f'Durée entre première donnée et dernière donnée pour {len(runs)} run ({run}) avec {n_data*len(runs)} fichiers data et {n_ccs} CCSN est : {t_end}')

# Paramètres de la fenêtre glissante
window_size = 1  # 1s
step_size = window_size/10   # 100ms

data_windows = []
ccsn_windows= []
histo_windows = []
current_time = 0
index_data_prev = 0
index_ccsn_prev = 0

t_ref = 50
n_it = int(t_end/t_ref) + 1
# Séparation des comparaisons en plusieurs itérations pour éviter de surcharger le temps de calcul
for j in range(n_it):
    # Séparation des listes times en sous listes pour chaque itération, pour gagner du temps de calcul: seulement pour data car ccsn dure 20sec max
    t_end_it = t_end*(j+1)/n_it
    # print(j, t_end, t_end_it)
    index_data = find_threshold_index(time_data, t_end_it)
    time_data_it = time_data[index_data_prev:index_data]
    # print(time_data_it)
    index_data_prev = find_threshold_index(time_data, t_end_it - window_size)
    while current_time < t_end_it:
        window_start = current_time - window_size  # les infos disponibles au temps actuel sont celles de la fenêtre précédente
        window_end = current_time
        current_time += step_size
            
        # Filtrage des événements dans la fenêtre 
        # Data
        events_in_window_data = 0
        for t_data in time_data_it:
            if window_start < t_data <= window_end:
                events_in_window_data += 1

        data_windows.append(events_in_window_data)  # Nombre d'événements dans la fenêtre

        # CCSN
        events_in_window_ccsn = 0
        for t_ccsn in time_ccsn:
            if window_start < t_ccsn <= window_end:
                events_in_window_ccsn += 1*scaling
                

        ccsn_windows.append(events_in_window_ccsn)  # Nombre d'événements dans la fenêtre
        histo_windows.append(events_in_window_data + events_in_window_ccsn)  # Nombre total d'événements dans la fenêtre


# Caractérisation du processus aléatoire
if n_data != 0:
    mean = np.mean(data_windows)
    std_dev = np.std(data_windows)
    n_windows = len(data_windows)
    n_max = 20
    for i in range(n_max):
        n = 0
        for j in data_windows:
            if j == i:
                n += 1
        print(f"Proportion d'événements de valeur {i} : {n/n_windows}")
    for j in data_windows:
        if j > n_max:
            print(f"Valeur {j} supérieure à {n_max} dans les données, il faut augmenter n_max pour l'afficher")
            break
    print(f"Moyenne du bruit de fond en {n_windows} fenêtres : {mean}")
    print(f"Ecart-type du bruit de fond en {n_windows} fenêtres : {std_dev}")

    print(f"Le rapport entre le signal et le bruit de fond est : {max(ccsn_windows)/max(data_windows)}")


# Affichage de l'histogramme final
fig, ax = plt.subplots(figsize=(10, 6))

ax.clear()
ax.plot(np.arange(len(histo_windows)) * step_size, histo_windows)
# ax.hist(time, bins=100, alpha=0.7)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Number of events')
ax.set_title('Real time monitor - Event distribution')
ax.grid(True)

plt.tight_layout()
if n_ccs == 0:
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/monitor/no_ccsn/real_time_monitor_{distance}kpc_{run}_window{window_size}s_{filling}_{n_ccs}ccs_{n_data}data.png", dpi=300)
elif n_data == 0:
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/monitor/no_data/real_time_monitor_{distance}kpc_{run}_window{window_size}s_{filling}_{n_data}data.png", dpi=300)
else:
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/monitor/real_time_monitor_{distance}kpc_{run}_window{window_size}s_{filling}.png", dpi=300)
