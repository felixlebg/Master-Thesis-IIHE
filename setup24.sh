#!/bin/bash

export LC_ALL=C
export CMTCONFIG=amd64_linux26
#source /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J22.1.0-rc4/setup.sh #1120/Pre-Release/J22.2.x/setup.sh
source /cvmfs/juno.ihep.ac.cn/el9_amd64_gcc11/Release/J25.1.3/setup.sh
export PYTHONPATH=/storage/gpfs_data/juno/junofs/users/mcolomer/pyinstalled:$PYTHONPATH
#Pre-Release/J23.1.x/setup.sh
#source /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Pre-Release/J23.1.0-rc1/setup.sh
#source /cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc1120/Release/J24.1.2/setup.sh


#export MCTRUTH=/storage/gpfs_data/juno/junofs/users/mcolomer/topo_reco_local/TopoTrackReco/libraries/mctruth/lib/
#export LD_LIBRARY_PATH=$MCTRUTH:$LD_LIBRARY_PATH
#export BOOST_ROOT=/cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J21v1r0-branch/ExternalLibs/Boost/1.75.0
#export BOOST_LIB_DIR=/cvmfs/juno.ihep.ac.cn/centos7_amd64_gcc830/Pre-Release/J21v1r0-branch/ExternalLibs/Boost/1.75.0/lib

#source /usr/share/htc/condor/9/enable

alias bobs="bjobs"
alias con_td="condor_transfer_data -pool cm01-htc -name sn01-htc mcolomer"
alias con_q="condor_q -pool cm01-htc -name sn01-htc"
alias con_sub="condor_submit -pool cm01-htc -name sn01-htc"
alias con_rm_all="condor_rm -pool cm01-htc -name sn01-htc"
alias con_rm_done="condor_rm -pool cm01-htc -name sn01-htc frosso -constraint 'JobStatus == 4'"
alias rt="root -l"
export jhome=/storage/gpfs_data/juno/junofs/users/frosso
export EDITOR=vim
alias cdh="cd $jhome"
