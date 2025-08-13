import numpy as np
import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
import matplotlib.pyplot as plt
from functions import Opt_E_range1, Opt_E_range2
import sys



# Paramètres
number_of_bins = 200 # même valeur que pour l'affichage

#run = int(sys.argv[1])
runs = [5946, 5947, 5956, 5957, 5958, 5959, 5961, 5963, 5965, 5970, 5971, 5972, 
        5977, 5985, 5989, 5993, 5994, 5995, 5996, 5999, 6007, 6009, 6010, 
        6011, 6012, 6042, 6043, 6044, 6045, 6046, 6050, 6051, 6052, 6053, 6054, 
        6056, 6060, 6062, 6063, 6064, 6065]
filling = "half"
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