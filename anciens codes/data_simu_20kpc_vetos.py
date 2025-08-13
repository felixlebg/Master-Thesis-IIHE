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
n_files = 189            # Nombre de fichiers simulées
t_ccs = 3               # Durée de détection pour chaque supernova (en secondes)
# runs = [3322, 3323, 3326, 3371, 3413, 3416]  # Full water
runs = [4335] # LS Filling 20%
#runs = [4332, 4333, 4334, 4335] # LS Filling 20%

for run in runs:
    # Initialisation
    total_charge_data = []
    total_charge_ccsn = []
    time_ccsn_wp = []
    t_data = 0              # Temps total des données réelles
    t_muons = 0             # Temps total des simulations de muons
    n_error = 0

    for i in range(n_files):
        simu_ccsn = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD--J25.1.3-{i+1}.root'
        
        try:
            root_simu_ccsn = TFile.Open(simu_ccsn,"READ")
        except:
            print(f"Error opening file {simu_ccsn}")
            continue

        # Création d'une liste des temps auxquels un evt ccsn est détecté dans la waterpool pour veto2
        for wp_evt in root_simu_ccsn.wp_events:
            t_evt = wp_evt.t_ns*1e-9 + wp_evt.t_sec  # temps auquel s'est produit la détection
            time_ccsn_wp.append(t_evt)

    time_ccsn_wp = sorted(time_ccsn_wp)
    for i in range(n_files):
        t_prev = 0
        t_prev_ccsn = 0
        if run >= 4330:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.LSFilling.ds-2.global_trigger_cotiwaverec_J25.2.2_{i+1}.root'
        elif run >= 3990:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.TEST.ds-2.global_trigger_cotiwaverec_J25.1.6_{i+1}.root'
        elif run < 3793:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.WaterFull.ds-2.global_trigger_cotiwaverec_J25.1.3_{i+1}.root'
        else:
            data = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/{run}/simple_out/TQ/tqcalib_output_RUN.{run}.JUNODAQ.LSFilling.ds-2.global_trigger_cotiwaverec_J25.1.6_{i+1}.root'
        # simu_muons = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_muons/tqcalib_muon_output_{i+1000}.root' 
        simu_ccsn = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD--J25.1.3-{i+1}.root'
        #simu_ccsn = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn_half/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD-half-J25.2.2-{i}.root'
        # simu_ccsn = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn_LS/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD-LS-J25.2.2-{i}.root'
        
        try:
            root_data =  TFile.Open(data,"READ")
            root_simu_ccsn = TFile.Open(simu_ccsn,"READ")
            # root_simu_muons = TFile.Open(simu_muons,"READ")
        except:
            n_error += 1
            print(f"Error opening file {data} or {simu_ccsn}")
            continue

        # Traitement des données réelles
        dt = 1
        for cd_evt in root_data.cd_events:
            correl = False
            t_evt = cd_evt.t_ns*1e-9 + cd_evt.t_sec  # temps auquel s'est produit la détection
            if t_prev != 0:
                    dt =  t_evt - t_prev
                    t_data += dt  # calcul de la durée entre 2 détections
            t_prev = t_evt

            # range en énergie optimal pour discriminer les neutrinos (on laisse en commentaire pour mieux visualiser la meilleure zone)
            #if cd_evt.npe_tot < npe_min or cd_evt.npe_tot > npe_max:
            #    continue

            # veto 1   
            if dt < 25e-6:
                continue

            # veto 2
            for wp_evt in root_data.wp_events:  # coïncidences avec les muons
                wp_t = wp_evt.t_ns*1e-9 + wp_evt.t_sec
                dt_wp = wp_t - t_evt
                if abs(dt_wp) < 200e-9 and wp_evt.npe_tot_wp > 1000:
                    correl = True
                    break
            for wp_t in time_ccsn_wp:  # coïncidence avec les neutrinos
                dt_wp = wp_t - t_evt
                if abs(dt_wp) < 200e-9 and wp_evt.npe_tot_wp > 1000:
                    correl = True
                    break
                elif dt_wp > 200e-9: # comme la liste time_ccsn_wp est sorted, on peut arrêter la boucle lorsque wp_t se passe après t_evt
                    break
            if not correl:
                total_charge_data.append(cd_evt.npe_tot)
                #total_charge_data.append(cd_evt.nhits)

        # Traitement des simulations de supernovas
        dt = 1
        for cd_evt in root_simu_ccsn.cd_events:
            correl = False
            t_evt = cd_evt.t_ns*1e-9 + cd_evt.t_sec  # temps auquel s'est produit la détection
            if t_prev_ccsn != 0:
                    dt =  t_evt - t_prev_ccsn
                    t_data += dt  # calcul de la durée entre 2 détections
            t_prev_ccsn = t_evt

            # range en énergie optimal pour discriminer les neutrinos (on laisse en commentaire pour mieux visualiser la meilleure zone)
            #if cd_evt.npe_tot < npe_min or cd_evt.npe_tot > npe_max:
            #    continue

            # veto 1   
            if dt < 25e-6:
                continue

            # veto 2
            for wp_evt in root_data.wp_events:  # coïncidences avec les muons
                wp_t = wp_evt.t_ns*1e-9 + wp_evt.t_sec
                dt_wp = wp_t - t_evt
                if abs(dt_wp) < 200e-9 and wp_evt.npe_tot_wp > 1000:
                    correl = True
                    break
            for wp_t in time_ccsn_wp:  # coïncidence avec les neutrinos
                dt_wp = wp_t - t_evt
                if abs(dt_wp) < 200e-9 and wp_evt.npe_tot_wp > 1000:
                    correl = True
                    break
                elif dt_wp > 200e-9: # comme la liste time_ccsn_wp est sorted, on peut arrêter la boucle lorsque wp_t se passe après t_evt
                    break
            if not correl:
                total_charge_ccsn.append(cd_evt.npe_tot)
                #total_charge_ccsn.append(cd_evt.nhits)


    # 2 sous-figures
    fig, axs = plt.subplots(figsize=(12, 5))

    min_charge = min(min(total_charge_data), min(total_charge_ccsn))
    max_charge = max(max(total_charge_data), max(total_charge_ccsn))
    if min_charge < 2e1:
        min_charge = 2e1
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
    plt.savefig(f"/storage/gpfs_data/juno/junofs/users/frosso/data_simu_20kpc_vetos_run{run}_{n_files - n_error}files.png", dpi=300)