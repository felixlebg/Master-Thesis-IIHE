import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
import numpy as np
import matplotlib.pyplot as plt
from ROOT import TFile, TTree, TH1
import sys
from functions import read_file_display



def plot_data(data, n, n_files):
    all_values = []
    all_weights = []
    runs = []
    all_dates = []
    min_charge = 100000
    max_charge = 0

    # Lire les données de tous les fichiers
    for run_files in data:
        values, weight, (run, date), veto = read_file_display(run_files, n)
        all_dates.append(date)
        all_values.append(values)
        all_weights.append(weight * np.ones_like(values))
        runs.append(f"{run}")
        min_charge = min(min(values), min_charge)
        max_charge = max(max(values), max_charge)


    if len(data) == 1:
        run_name = runs[0]
        date_name = all_dates[0]
    else:
        run_name = f"run{runs[0]}_to_run{runs[-1]}"
        date_name = f"{all_dates[0]}_to_{all_dates[-1]}"
    
    
    if n == "nhits":
        if filling == "water":
            min_charge_plot = 2e1
        elif filling == "half":
            min_charge_plot = 2e2
        elif filling == "full":
            min_charge_plot = 2e2  # à changer lorsque les données seront disponibles
    
    elif n == "npe":
        if filling == "water":
            min_charge_plot = 2e1
        elif filling == "half":
            min_charge_plot = 2e2
        elif filling == "full":
            min_charge_plot = 2e2  # à changer lorsque les données seront disponibles

    if min_charge < min_charge_plot:
            min_charge = min_charge_plot
    #if max_charge > max_charge_plot:
    #    max_charge = max_charge_plot
    min_charge = np.log10(min_charge)
    max_charge = np.log10(max_charge)


    # Créer le plot
    fig, axs = plt.subplots(figsize=(12, 5))

    # Tracer les histogrammes
    for values, weight, _ in zip(all_values, all_weights, runs):
        #axs.hist(values, bins=bins, weights=weights, alpha=0.3, label=run)
        axs.hist(values, bins=np.logspace(min_charge, max_charge, 200), weights=weight*np.ones_like(values), alpha=0.7, color='green', label=f"DATA RUN {run_name} done the {date_name}")
    
    
    # Configuration des axes et du titre
    axs.set_title(f"Charges ({n}) due to natural background radiations and CCSN")
    axs.set_xlabel(f"Charge ({n})")
    axs.set_ylabel("Rate (Hz)")
    axs.set_xscale('log')
    axs.set_yscale('log')
    axs.legend()


    plt.tight_layout()
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/data_simu/data/{veto}/data_{n}_{veto}_run{run_name}_{n_files}files.png", dpi=300)


def plot_ccsn(ccsns, n, n_files, filling, veto, distance):
    all_values = []
    all_weights = []
    runs = []
    all_dates = []

    # Lire les données de tous les fichiers
    for files in ccsns:
        values, weight, (run, date), veto = read_file_display(files, n)
        all_dates.append(date)
        all_values.append(values)
        all_weights.append(weight * np.ones_like(values))
        runs.append(f"run{run}")
    
    
    min_charge = min(all_values)
    max_charge = max(all_values)
    if n == "nhits":
        if filling == "water":
            min_charge_plot = 2e1
        elif filling == "half":
            min_charge_plot = 2e2
        elif filling == "full":
            min_charge_plot = 2e2  # à changer lorsque les données seront disponibles
    
    elif n == "npe":
        if filling == "water":
            min_charge_plot = 2e1
        elif filling == "half":
            min_charge_plot = 2e2
        elif filling == "full":
            min_charge_plot = 2e2  # à changer lorsque les données seront disponibles

    if min_charge < min_charge_plot:
            min_charge = min_charge_plot
    #if max_charge > max_charge_plot:
    #    max_charge = max_charge_plot
    min_charge = np.log10(min_charge)
    max_charge = np.log10(max_charge)


    # Créer le plot
    fig, axs = plt.subplots(figsize=(12, 5))

    # Tracer les histogrammes
    for values, weight, _ in zip(all_values, all_weights, runs):
        #axs.hist(values, bins=bins, weights=weights, alpha=0.3, label=run)
        axs.hist(values, bins=np.logspace(min_charge, max_charge, 200), weights=weight*np.ones_like(values), alpha=0.7, color='blue', label=f"Simulation CCSN for {filling} filling of LS at {distance} kpc")
    
    
    # Configuration des axes et du titre
    axs.set_title(f"Charges ({n}) due to natural background radiations and CCSN")
    axs.set_xlabel(f"Charge ({n})")
    axs.set_ylabel("Rate (Hz)")
    axs.set_xscale('log')
    axs.set_yscale('log')
    axs.legend()


    plt.tight_layout()
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/simu_ccs_{distance}kpc_{n}_{veto}_{filling}_{n_files}files.png", dpi=300)


def plot_comparison(files_data, files_ccsn, n, n_files, filling, distance):
    values_data, weight_data, run, veto = read_file_display(files_data, n)
    values_ccs, _, _, veto = read_file_display(files_ccsn, n)

    weight_ccs = ((20/distance)**2)/(3*n_files) 

    run, date = run
    # min and max values
    print(f"The maximum value of {n} for {filling} CCSN simulation is {max(values_ccs)}")

    min_charge = min(min(values_data), min(values_ccs))
    max_charge = max(max(values_data), max(values_ccs))
    if n == "nhits":
        if filling == "water":
            min_charge_plot = 2e1
        elif filling == "half":
            min_charge_plot = 2e2
        elif filling == "full":
            min_charge_plot = 2e2  # à changer lorsque les données seront disponibles
    
    elif n == "npe":
        if filling == "water":
            min_charge_plot = 2e1
        elif filling == "half":
            min_charge_plot = 2e2
        elif filling == "full":
            min_charge_plot = 2e2  # à changer lorsque les données seront disponibles

    if min_charge < min_charge_plot:
            min_charge = min_charge_plot
    #if max_charge > max_charge_plot:
    #    max_charge = max_charge_plot
    min_charge = np.log10(min_charge)
    max_charge = np.log10(max_charge)


    # Display (les poids sont calculés pour convertir les comptages en fréquence (Hz))
    fig, axs = plt.subplots(figsize=(12, 5))
    axs.hist(values_data, bins=np.logspace(min_charge, max_charge, 200), weights=weight_data*np.ones_like(values_data), alpha=0.7, color='green', label=f"DATA RUN {run} done the {date}")
    axs.hist(values_ccs, bins=np.logspace(min_charge, max_charge, 200), weights=weight_ccs*np.ones_like(values_ccs), alpha=0.7, color='blue', label=f"Simulation CCSN for {filling} filling of LS at {distance} kpc")

    # Configuration des axes et du titre
    axs.set_title(f"Charges ({n}) due to natural background radiations and CCSN")
    axs.set_xlabel(f"Charge ({n})")
    axs.set_ylabel("Rate (Hz)")
    axs.set_xscale('log')
    axs.set_yscale('log')
    axs.legend()

    plt.tight_layout()
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/data_simu/{n}/{veto}/{filling}/data_simu_{distance}kpc_run{run}_{n_files}files.png", dpi=300)


# Paramètres
n = "npe"
v = "_vetos"
#v = ""
run = int(sys.argv[1])
runs = [run]
fillings = ["half"]
d = 20  # en kpc
number_of_files = 2000

ccsns = []
for filling in fillings:
    files_ccsn = []
    for i in range(number_of_files):
        files_ccsn.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/simu/{filling}/out_simu{v}_file{i%100 + 1}.txt")
    ccsns.append(files_ccsn)

#plot_ccsn(ccsns, n, number_of_files, fillings)

data = []
for run in runs:
    files_data = []
    for i in range(number_of_files):
        files_data.append(f"/storage/gpfs_data/juno/junofs/users/frosso/out/{run}/out_data{v}_run{run}_file{i + 1}.txt")
    data.append(files_data)

#plot_data(data, n, number_of_files)

#plot_data(data, n, number_of_files)
plot_comparison(files_data, files_ccsn, n, number_of_files, filling, d)

