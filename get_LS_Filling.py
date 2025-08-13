import numpy as np

def get_mass_values(date_input, file_path='massVolumeLS.txt'):

    vol_s1 = []
    vol_s2 = []
    vol = 23227.8

    with open(file_path, 'r') as f:
        lines = f.readlines()

# 7714 7715 7716 7786 7787 7788 7789 7790 7880 7883 7886 7897 7901 7903 7905 7906 7908 7909 7910 7949 7992 7993 7994
    for line in lines:
        if line.strip() == "":
            continue

        parts = line.strip().split()
        try:
            date_str = parts[0][0:10]  # Extraire la date au format YYYY-MM-DD
        except:
            continue  # Skip invalid lines

        # Chercher la date la plus proche sans être future
        if date_input == date_str:
            vol_s1.append(float(parts[6]))  # Colonne mass_s1/ton
            vol_s2.append(float(parts[10]))  # Colonne mass_s2/ton

    proportion_s1 = 100*np.mean(vol_s1)/vol  # 20ktons max
    proportion_s2 = 100*np.mean(vol_s2)/vol  # 20ktons max

    return proportion_s1, proportion_s2  

p1, p2 = get_mass_values("2025-07-13") # run 6043 pour 50% LS (range: run 5540 à 6330 pour 45% à 55% LS en un mois)
print(f"Proportion of LS for sensor 1: {round(1000*p1)/1000}%")
print(f"Proportion of LS for sensor 2: {round(1000*p2)/1000}%")
