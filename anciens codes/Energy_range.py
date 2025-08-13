import numpy as np
import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
import matplotlib.pyplot as plt
from functions import read_file_display
from math import log


def Opt_threshold(files_ccsn, files_data, number_of_bins, scaling, n="nhits"):
    #  Cette fonction calcul le nombre de neutrinos détectés et le nombre de données pour un threshold donné pour les plot a different thresholds

    nhits_data, weight_data, _, _ = read_file_display(files_data, n)
    nhits_ccs, weight_ccs, _, _ = read_file_display(files_ccsn, n)

    nhits_data = sorted(nhits_data)
    nhits_ccs = sorted(nhits_ccs)

    min_nhits = max(nhits_data[0], nhits_ccs[0])
    max_nhits = min(nhits_data[-1], nhits_ccs[-1])
    # print(f"min_nhits = {min_nhits}, max_nhits = {max_nhits}")

    # echelle logarithmique
    coeff = (max_nhits/min_nhits)**(1/number_of_bins)


    n_ccs_list = []
    n_data_list = []
    n_ccs_tot = 0
    n_data_tot = 0
    end_bin = min_nhits
    for i in range(number_of_bins):
        n_data = 0
        n_ccs = 0
        start_bin = end_bin
        end_bin = end_bin*coeff
        for j in range(len(nhits_data)):
            if nhits_data[j] >= start_bin and nhits_data[j] < end_bin:
                n_data += weight_data


        for j in range(len(nhits_ccs)):
            if nhits_ccs[j]>= start_bin and nhits_ccs[j] < end_bin:
                n_ccs += weight_ccs*scaling
            

        # Ajoute des bins seulement si le nombre d'evenements est dans une certaine proportion
        if n_data == 0:
            print(f"Warning: No data in bin {i} ({start_bin}, {end_bin})")
            n_data = 1e-5  # pour éviter la division par 0
        n_ccs_list.append(n_ccs)
        n_data_list.append(n_data)


    # optimal range methode 1:
    # upper bound
    min_width = 5.7   # à partir du graphe
    width_index = log(min_width, coeff)
    opt0 = 0
    opt_lower_index = 0
    opt_upper_index = 0
    for lower_index in range(number_of_bins - int(width_index)):
        upper_index = int(lower_index + width_index)
        n_ccs_tot = sum(n_ccs_list[lower_index:upper_index])
        n_data_tot = sum(n_data_list[lower_index:upper_index])
        opt = n_ccs_tot/n_data_tot
        if opt > opt0:
            opt_lower_index = lower_index
            opt_upper_index = upper_index
            opt0 = opt
    
    print(f"Range avant élargissement pour méthode 1: {[min_nhits*coeff**opt_lower_index, min_nhits*coeff**opt_upper_index]}")

    # range optimal pour une largeur de min_width -> on aimerait pouvoir elargir cette valeur
    # lower index
    for lower_index in range(opt_lower_index):
        n_ccs_tot = sum(n_ccs_list[lower_index:opt_upper_index])
        n_data_tot = sum(n_data_list[lower_index:opt_upper_index])
        opt = n_ccs_tot/n_data_tot
        if opt >= 0.95*opt0:
            opt_lower_index = lower_index
            opt0 = opt

    # upper index
    for upper_index in range(opt_upper_index, number_of_bins):
        n_ccs_tot = sum(n_ccs_list[opt_lower_index:upper_index])
        n_data_tot = sum(n_data_list[opt_lower_index:upper_index])
        opt = n_ccs_tot/n_data_tot
        if opt >= 0.95*opt0:
            opt_upper_index = upper_index
            opt0 = opt


    opt_range1 = [min_nhits*coeff**opt_lower_index, min_nhits*coeff**opt_upper_index]
    

    # optimal range méthode 2:
    # upper bound
    min_width = 5.7   # à partir du graphe
    width_index = log(min_width, coeff)
    opt0 = 0
    opt_lower_index = 0
    opt_upper_index = 0
    for lower_index in range(number_of_bins - int(width_index)):
        upper_index = int(lower_index + width_index)
        n_data_tot = sum(n_data_list[lower_index:upper_index])
        opt = 1/n_data_tot
        if opt > opt0:
            opt_lower_index = lower_index
            opt_upper_index = upper_index
            opt0 = opt
    
    print(f"Range avant élargissement pour méthode 2: {[min_nhits*coeff**opt_lower_index, min_nhits*coeff**opt_upper_index]}")

    # range optimal pour une largeur de min_width -> on aimerait pouvoir elargir cette valeur
    # lower index
    for lower_index in range(opt_lower_index):
        n_data_tot = sum(n_data_list[lower_index:opt_upper_index])
        opt = 1/n_data_tot
        if opt >= 0.95*opt0:
            opt_lower_index = lower_index
            opt0 = opt

    # upper index
    for upper_index in range(opt_upper_index, number_of_bins):
        n_data_tot = sum(n_data_list[opt_lower_index:upper_index])
        opt = 1/n_data_tot
        if opt >= 0.95*opt0:
            opt_upper_index = upper_index
            opt0 = opt
    
    opt_range2 = [min_nhits*coeff**opt_lower_index, min_nhits*coeff**opt_upper_index]

   
    return opt_range1, opt_range2



# Paramètres
number_of_bins = 200 # même valeur que pour l'affichage

run = 6043
filling = "half"
distance = 20 # en kpc
scaling = (20/distance)**2

number_of_files = 1000


files_ccsn = []
for i in range(number_of_files):
    files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/{filling}/out_simu_vetos_file{i%100 + 1}.txt")


files_data = []
for i in range(number_of_files):
    files_data.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data_vetos_run{run}_file{i + 1}.txt")


opt_range1, opt_range2 = Opt_threshold(files_ccsn, files_data, number_of_bins, scaling)
print(f"Optimal range with method 1: {opt_range1}")
print(f"Optimal range with method 2: {opt_range2}")

# solution for run 6043 [8700.030654428703, 49287.579185991126]