# Ce script permet de comparer les distributions de charge entre les données réelles et les simulations
# de muons et de supernovas (CCSN) pour déterminer la plage d'énergie optimale pour la détection

import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
import numpy as np
import matplotlib.pyplot as plt
from ROOT import TFile, TTree, TH1
import os
import json


bittags = json.load(open(os.path.join(os.environ["JUNOTOP"],"junosw/OEC/OECTutorial/share/DummyCommonConfig_water.json")))
tags = bittags["tag"]
bittags = bittags["tagBits"]

for i in bittags:
    aux = i["tag"]
    aux = int(aux.replace(",",""), 2)
    i["tag"] = aux


# Paramètres de simulation
n_files = 200            # Nombre de fichiers simulées
t_ccs = 3               # Durée de détection pour chaque supernova (en secondes)
#runs = [3322, 3323, 3326]  # Full water
runs = [4332] # solo run
#runs = [4332, 4333, 4334, 4335] # LS Filling 20%

for run in runs:
    # Initialisation
    total_charge_data = []
    total_charge_muons = []
    total_charge_ccsn = []
    t_data = 0              # Temps total des données réelles
    t_muons = 0             # Temps total des simulations de muons
    n_error = 0
    for i in range(n_files):
        t_prev = 0
        t_prev_mu = 0
        if run >= 4330:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.LSFilling.ds-2.global_trigger_cotiwaverec_J25.2.2_{i+1}.root'
        elif run >= 3990:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.TEST.ds-2.global_trigger_cotiwaverec_J25.1.6_{i+1}.root'
        elif run < 3793:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.WaterFull.ds-2.global_trigger_cotiwaverec_J25.1.3_{i}.root'
        else:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.LSFilling.ds-2.global_trigger_cotiwaverec_J25.1.6_{i+1}.root'
        # simu_muons = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_muons/tqcalib_muon_output_{i+1000}.root' 
        #simu_ccsn = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD--J25.1.3-{i+1}.root'
        #simu_ccsn = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn_half/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD-half-J25.2.2-{i}.root'
        simu_ccsn = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn_LS/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD-LS-J25.2.2-{i}.root'
        
        
        try:
            root_data =  TFile.Open(data,"READ")
            root_simu_ccsn = TFile.Open(simu_ccsn,"READ")
            # root_simu_muons = TFile.Open(simu_muons,"READ")
        except:
            n_error += 1
            print(f"Error opening file {data} or {simu_ccsn}")
            continue

        # Traitement des données réelles
        for cd_evt in root_data.cd_events:
            t_evt = cd_evt.t_ns*10**(-9) + cd_evt.t_sec  # temps auquel s'est produit la détection
            if t_prev != 0:
                t_data += t_evt - t_prev  # calcul de la durée entre 2 détections
            t_prev = t_evt

            #total_charge_data.append(cd_evt.npe_tot)
            total_charge_data.append(cd_evt.nhits) 
        
        # Traitement des simulations de muons
        #for cd_evt in root_simu_muons.cd_events:
        #    t_evt = cd_evt.t_ns*10**(-9) + cd_evt.t_sec
        #    if t_prev_mu != 0:
        #        t_muons += t_evt - t_prev_mu
        #    t_prev_mu = t_evt
        #    
        #    total_charge_muons.append(cd_evt.npe_tot)

        # Traitement des simulations de supernovas
        for cd_evt in root_simu_ccsn.cd_events:
            #total_charge_ccsn.append(cd_evt.npe_tot)
            total_charge_ccsn.append(cd_evt.nhits)


    # 2 sous-figures
    fig, axs = plt.subplots(figsize=(12, 5))

    min_charge = min(min(total_charge_data), min(total_charge_ccsn))
    max_charge = max(max(total_charge_data), max(total_charge_ccsn))
    if min_charge < 1e1:
        min_charge = 1e1
    if max_charge > 1e7:
        max_charge = 1e7
    min_charge = np.log10(min_charge)
    max_charge = np.log10(max_charge)

    # Création des histogrammes normalisés
    # Les poids sont calculés pour convertir les comptages en taux (Hz)
    axs.hist(total_charge_data, bins=np.logspace(min_charge, max_charge, 200), weights=(1/t_data)*np.ones_like(total_charge_data), alpha=0.7, color='green', label=f"DATA RUN {run}")
    # Pour les ccsn on doit diviser par la durée de détection des ccsn (+-3sec) et par le nombre de supernova simulée
    axs.hist(total_charge_ccsn, bins=np.logspace(min_charge, max_charge, 200), weights=(1/(t_ccs*(n_files - n_error)))*np.ones_like(total_charge_ccsn), alpha=0.6, color='blue', label="Simulation CCSN")
    
    # Configuration des axes et du titre
    axs.set_title("Charges due to muons and ccsn")
    axs.set_xlabel("Charge")
    axs.set_ylabel("Rate (Hz)")
    axs.set_xscale('log')  # Axe X en log
    axs.set_yscale('log')  # Axe Y en log
    axs.legend()

    plt.tight_layout()
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/data_simu_20kpc_nhits_full_run{run}_{n_files - n_error}files.png", dpi=300)