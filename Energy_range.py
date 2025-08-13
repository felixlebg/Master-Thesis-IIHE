import numpy as np
import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
import matplotlib.pyplot as plt
from functions import Opt_E_range
import sys


# Paramètres
number_of_files = 1000


number_of_bins = 200 # même valeur que pour l'affichage

#run = int(sys.argv[1])
filling = ["25%", "half", "75%"][int(sys.argv[1])]
distance = 60 # en kpc


files_ccsn = []
if filling == "75%":
    runs = [7097, 7099, 7137, 7145, 7146, 7147, 7148, 7246, 7247, 7302, 7317, 7318, 
        7341, 7359, 7360, 7361, 7366, 7373, 7375, 7377, 7378, 7379, 
        7450, 7451, 7602, 7603, 7604, 7688, 7689, 7714, 
        7715, 7716, 7786, 7787, 7788, 7789, 7790, 7880, 7883, 7886, 7897, 7901, 
        7903, 7906, 7908, 7909, 7910]
    thresholds = [1+250*i for i in range(21)]
    for i in range(number_of_files):
        if i%2==0:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/half/out_simu_vetos_file{i%100 + 1}.txt")
        else:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/LS/out_simu_vetos_file{i%100 + 1}.txt")
elif filling == "25%":
    runs = [5016, 5017, 5018, 5019, 5020, 5021, 5022, 5023, 
        5044, 5046, 5047, 5048, 5050, 5053, 5054, 5057, 5110, 
        5111, 5115, 5116, 5117, 5119, 5120, 5121, 5122]
    thresholds = [1+100*i for i in range(21)]
    for i in range(number_of_files):
        if i%2==0:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/half/out_simu_vetos_file{i%100 + 1}.txt")
        else:
            files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/water/out_simu_vetos_file{i%100 + 1}.txt")
elif filling == "half":
    runs = [5946, 5947, 5956, 5957, 5958, 5959, 5961, 5963, 5965, 5970, 5971, 5972, 
        5977, 5985, 5989, 5993, 5994, 5995, 5996, 5999, 6007, 6009, 6010, 
        6011, 6012, 6042, 6043, 6044, 6045, 6046, 6050, 6051, 6052, 6053, 6054, 
        6056, 6060, 6062, 6063, 6064, 6065]
    thresholds = [1+2500*i for i in range(21)]
    for i in range(number_of_files):
        files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/{filling}/out_simu_vetos_file{i%100 + 1}.txt")



files_data = []
for run in runs:
    for i in range(number_of_files):
        files_data.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data_vetos_run{run}_file{i + 1}.txt")


opt_range1 = Opt_E_range(files_ccsn, files_data, thresholds, number_of_bins, distance, runs, filling)
print(f"Filling {filling}, méthode 1")
print(f"Optimal range with method 1: {opt_range1}")

# solution for run 6043 [8700.030654428703, 49287.579185991126]