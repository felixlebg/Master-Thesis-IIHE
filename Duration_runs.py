# Ce script simule le moniteur supernova en temps réel pour déterminer combien d'évenements sont nécessaire
# pour déclancher le trigger supernova par rapport au bruit de fond, en utilisant une méthode de fenetre glissante
import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
from functions import read_file_duration


t_start_ccs = 5  # Temps à partir duquel est détectée la supernova

n_ccs = 0  # Nombre de supernova simulées

v = "_vetos"
filling = "half"
distance = 60  # en kpc
scaling = (20/distance)**2


runs= [5016, 5017, 5018, 5019, 5020, 5021, 5022, 5023, 
        5044, 5046, 5047, 5048, 5050, 5053, 5054, 5057, 5110, 
        5111, 5115, 5116, 5117, 5119, 5120, 5121, 5122, 5946, 5947, 5956, 5957, 5958, 5959, 5961, 5963, 5965, 5970, 5971, 5972, 
        5977, 5985, 5989, 5993, 5994, 5995, 5996, 5999, 6007, 6009, 6010, 
        6011, 6012, 6042, 6043, 6044, 6045, 6046, 6050, 6051, 6052, 6053, 6054, 
        6056, 6060, 6062, 6063, 6064, 6065, 7097, 7099, 7137, 7145, 7146, 7147, 7148, 7246, 7247, 7302, 7317, 7318, 
        7341, 7359, 7360, 7361, 7366, 7373, 7375, 7377, 7378, 7379, 
        7450, 7451, 7602, 7603, 7604, 7688, 7689, 7714, 
        7715, 7716, 7786, 7787, 7788, 7789, 7790, 7880, 7883, 7886, 7897, 7901, 
        7903, 7906, 7908, 7909, 7910
    ]  # à 75% LS


if n_ccs != 0:
    n_data = 0  # Visualisationen temps réel de la supernova -> pas trop de fichiers pour voir l'augmentation plus facilement
else:
    n_data = 2000  # nombre de fichiers par run 


files_data = []
for run in runs:
    files_run = []
    for i in range(n_data):
        files_run.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data{v}_run{run}_file{i+1}.txt")
    files_data.append(files_run)


# Optension des temps des événements du bruit de fond et simulation supernova 
# Read file
duration_runs = read_file_duration(files_data)
print(duration_runs)

if n_data != 0:
    t_prev_evt = 0
    cumulative_pause = 0
    t_prev_end = 0
    for i, duration_run in enumerate(duration_runs):
        run = runs[i]
        dt, n_files = duration_run
        print(f"Run {run} for {n_files} and a total duration of : {dt/3600} hours")
