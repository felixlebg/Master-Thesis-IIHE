import numpy as np
import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
import matplotlib.pyplot as plt
from functions import Opt_E_range1, Opt_E_range2
import sys



# Paramètres
number_of_bins = 200 # même valeur que pour l'affichage

#run = int(sys.argv[1])
runs = [7097, 7099, 7137, 7145, 7146, 7147, 7148, 7246, 7247, 7302, 7317, 7318, 
        7341, 7359, 7360, 7361, 7366, 7373, 7375, 7377, 7378, 7379, 
        7450, 7451, 7602, 7603, 7604, 7688, 7689, 7714, 
        7715, 7716, 7786, 7787, 7788, 7789, 7790, 7880, 7883, 7886, 7897, 7901, 
        7903, 7906, 7908, 7909, 7910]
filling = "75%"
distance = 60 # en kpc

number_of_files = 1000
thresholds1 = [1 + 300*i for i in range(12)]
thresholds2 = [1+100*i for i in range(20)]

files_ccsn = []
if filling == "75%":
    for i in range(number_of_files):
        if i%2==0:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/half/out_simu_vetos_file{i%100 + 1}.txt")
        else:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/LS/out_simu_vetos_file{i%100 + 1}.txt")
elif filling == "25%":
    for i in range(number_of_files):
        if i%2==0:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/half/out_simu_vetos_file{i%100 + 1}.txt")
        else:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/water/out_simu_vetos_file{i%100 + 1}.txt")
else:
    for i in range(number_of_files):
        files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/{filling}/out_simu_vetos_file{i%100 + 1}.txt")


files_data = []
for run in runs:
    for i in range(number_of_files):
        files_data.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data_vetos_run{run}_file{i + 1}.txt")


opt_range1 = Opt_E_range1(files_ccsn, files_data, thresholds1, number_of_bins, distance, runs, filling)
opt_range2 = Opt_E_range2(files_ccsn, files_data, thresholds2, number_of_bins, distance, runs, filling)
print(f"Optimal range with method 1: {opt_range1}")
print(f"Optimal range with method 2: {opt_range2}")

# solution for run 6043 [8700.030654428703, 49287.579185991126]