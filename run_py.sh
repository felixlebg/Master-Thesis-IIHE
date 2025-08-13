#!/bin/bash
source /storage/gpfs_data/juno/junofs/users/frosso/setup24.sh

RUN=$1 #$(($(($1))+$(($2))))
mkdir -p /storage/gpfs_data/juno/junofs/users/frosso/out/$RUN

#python /storage/gpfs_data/juno/junofs/users/frosso/simu.py $2

python /storage/gpfs_data/juno/junofs/users/frosso/data.py $RUN


#python /storage/gpfs_data/juno/junofs/users/frosso/display.py $RUN


#python /storage/gpfs_data/juno/junofs/users/frosso/real_time_monitor.py 
#python /storage/gpfs_data/juno/junofs/users/frosso/real_time_monitor2.py
#python /storage/gpfs_data/juno/junofs/users/frosso/real_time_monitor3.py
#python /storage/gpfs_data/juno/junofs/users/frosso/real_time_monitor4.py
#python /storage/gpfs_data/juno/junofs/users/frosso/real_time_monitor6.py


#python /storage/gpfs_data/juno/junofs/users/frosso/z_npe.py


#python /storage/gpfs_data/juno/junofs/users/frosso/Energy_range.py


# chmod u+x run_py.sh pour rendre le script exécutable
# ./run_py.sh pour vérifier que l'exécution fonctionne
