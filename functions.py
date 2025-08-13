import os
os.environ["MPLCONFIGDIR"] = "/storage/gpfs_data/juno/junofs/users/frosso/"
from ROOT import TFile, TTree, TH1



def sub_list(root_file, file_dividing, minE_wp):
    # initialisation
    cd_evt_l = []
    wp_evt_l = []
    wp_evt_divided = []


    # Acquisition des données utiles
    for cd_evt in root_file.cd_events:
        t_cd = cd_evt.t_ns*1e-9 + cd_evt.t_sec  # temps auquel s'est produit la détection cd
        cd_evt_l.append([cd_evt.npe_tot, cd_evt.nhits, t_cd, cd_evt.vz])
        #cd_evt_l.append([cd_evt.npe_tot, cd_evt.nhits, t_cd])

    for wp_evt in root_file.wp_events:
        t_wp = wp_evt.t_ns*1e-9 + wp_evt.t_sec  # temps auquel s'est produit la détection wp
        if wp_evt.npe_tot_wp > minE_wp:  # si npe dans wp est suffisant que pour avoir muon interaction
            wp_evt_l.append(t_wp)

    print(f"Number of muons detection in the water pool: {len(wp_evt_l)}")
    
    wp_evt_l_sorted = sorted(wp_evt_l)
    if wp_evt_l_sorted != wp_evt_l:
        print("Warning: wp_evt_l is not sorted, this may cause problems.")
    
    wp_evt_l = wp_evt_l_sorted

     # créations des sous-listes wp pour réduire le temps de calcul
    if len(wp_evt_l) > 2*file_dividing:
        for i in range(file_dividing):
            l = len(wp_evt_l)
            wp_evt_divided.append(wp_evt_l[int(l*i/file_dividing): int(l*(i+1)/file_dividing)+1])

    else:
        wp_evt_divided = [wp_evt_l]

    return cd_evt_l, wp_evt_divided


def open_file(info, i):
    if info[0] == "data":
        run = info[1]
        for name in ["LSFilling", "Physics", "TEST"]:
            for version in ["2.2", "3.0", "3.0.a", "3.0.b","4.1", "4.1.a"]:
                for incr in [1, 1000]:
                    try:
                        file = f'/storage/gpfs_data/juno/junofs/users/mcolomer/water_data/data/{run}/CalibTQ/RUN.{run}.JUNODAQ.{name}.ds-2.global_trigger_cotiwaverec_J25.{version}_{i+incr}.esd.root'
                        TFile.Open(file)
                        return file
                    except OSError:
                        continue
        print(f"Error: File not found for data run {run} with index {i}")
        return "No_file"

    elif info[0] == "ccsn":
        filling = info[1]
        if filling == "water":
            file = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn_water/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD-water-J25.2.2-{i+1}.root'
        elif filling == "half":
            file = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn_half/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD-half-J25.2.2-{i+1}.root'
        elif filling == "LS":
            file = f'/storage/gpfs_data/juno/junofs/users/mcolomer/ana_water_J25/TQ_ccsn_LS/tqcalib_ccsn_output_calib-globaltrigg-thre100-20kpc-IBD-LS-J25.2.2-{i+1}.root'
        else:
            print('info[1] should be "water", "half" or "LS".')
        return file
    else:
        print('info[0] should be "data" or "water".')
        return "No_file"



def read_file_display(files, n):
    # Read file
    npe = []
    nhits = []
    for file in files:
        try:
            with open(file, "r") as f:  
                lines = f.readlines()
                if len(lines) == 0:
                    continue 

                for i in range(len(lines) - 1):
                    line = lines[i]
                    data = line.strip().split() 
                    npe.append(float(data[0])) 
                    nhits.append(float(data[1]))
        except FileNotFoundError:
            continue

        last_lign = lines[-1].strip().split()

    run = (last_lign[0], last_lign[-1])
    weight = float(last_lign[1])
    veto = last_lign[2]

    # Sélection des données à afficher
    if n == "npe":
        values = npe 
    elif n == "nhits":
        values = nhits
    else:
        print('Error : the second argument of plot should be "npe" or "nhits"')
        
    return values, weight, run, veto


def read_file_monitor(files):
    # Read file
    n_files = 0
    data = []
    for files_run in files:
        n_error = 0
        data_run = []
        for file in files_run:
            try:
                with open(file, "r") as f:  
                    lines = f.readlines()
                    if len(lines) == 0:
                        continue 

                    for i in range(len(lines) - 1):
                        line = lines[i]
                        data_run.append(line.strip().split()) 

                    n_files += 1

            except FileNotFoundError:
                print(f"File {file} not found, skipping.")
                n_error += 1
                if n_error > 50:
                    print("Too many errors while reading files, stopping.")
                    break  # Stop reading files if too many errors
                continue

        data.append(data_run)

    return data, n_files


def find_threshold_index(sorted_list, treshold):
    if sorted_list[0] > treshold:
        return 0
    index = len(sorted_list)
    length_list = len(sorted_list)
    for i in range(length_list):
        time = sorted_list[i]
        if time > treshold:
            return i
    return index