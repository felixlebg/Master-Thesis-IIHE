#include <iostream>
#include <map>
#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "TH2.h"

#include<math.h>
#include "Event/OecEvt.h"
#include "TCanvas.h"
#include "Event/SimHeader.h"
#include "TGraph.h"
#include "Event/SimTrack.h"
#include "Event/SimEvt.h"
#include <list>

#include <typeinfo>

// C++ program to illustrate std::istringstream                                                                                                                                             
#include <sstream>
#include <string>
#include <vector>

# include <stdio.h>
# include <stdlib.h>

using namespace JM;



string intToA(int n,int radix)    //n is the number to be converted，radix is the specific base
{
	string ans="";
	do{
		int t=n%radix;
		if(t>=0&&t<=9)	ans+=t+'0';
		else ans+=t-10+'a';
		n/=radix;
	}while(n!=0);	//use do{}while（）to prevent the input being 0
	reverse(ans.begin(),ans.end());
	return ans;	
}



void muons_water() {

    // set what is needed = 0
    int n_oec = 0;
    int n_true = 0;
    float eff_TT;
    int simID;
    int n_trig = 0;
    float eff_trig;
    int nbad=0;
    //vector<int> id_len;

    // outfiles

    ofstream outfile_oec_tags;
    outfile_oec_tags.open("muon_out_wpo.txt");
    outfile_oec_tags << "CD" <<"\t"<< "TT" <<"\t"<< "f" <<"\t"<< "oec_energy" <<"\t"<< "intag" <<"\t"<< "base16" << endl;

    // histograms

    TH1D* my_histo = new TH1D("myh","",1000,0,3000);

    // for loop over all the files

    for(int f=1; f<101; f++){


        int last_idx = -99;
        // set TString and TFile name (without the for loop bc we have only 1 file)
        TString oecname = TString::Format("/storage/gpfs_data/juno/junofs/users/mcolomer/J24_water/OEC_muons/oec-muon-Ec20MeV-nhitsth50-nfiredPMTs50-%d.root", int(f));

        list<int> list_last_idx;
        list_last_idx.clear(); 
        list_last_idx.push_back(last_idx);
    
        TFile *OECfile = TFile::Open(oecname);

        // avoid corrupted files :
        if (!OECfile || OECfile->IsZombie()){
            std::cout << "Error opening file" << std::endl;
            //continue;
        }

        else{

        n_trig+=1; // counting the number of files

        // path in TString to the data :
        TString oec_treename = "Event/Oec/OecEvt";
        TTree* oec_tree = (TTree*)(OECfile->Get(oec_treename));
        TString simh_treename = "Event/Sim/SimHeader";
        TTree* simh_tree = (TTree*)(OECfile->Get(simh_treename));
        // TString simevt_treename = "Event/Sim/SimEvt";
        // TTree* simevt_tree = (TTree*)(OECfile->Get(simevt_treename));

        JM::OecEvt* oecobj = 0;
        oec_tree->SetBranchAddress("OecEvt", &oecobj);
        oec_tree->GetBranch("OecEvt")->SetAutoDelete(true);

        JM::SimHeader* headobj = 0;
        simh_tree->SetBranchAddress("SimHeader", &headobj);
        simh_tree->GetBranch("SimHeader")->SetAutoDelete(true);

        // JM::SimEvt* simobj = 0;
        // simevt_tree->SetBranchAddress("SimEvt", &simobj);
        // simevt_tree->GetBranch("SimEvt")->SetAutoDelete(true);


        // new for loop with all the entries :
        for(Long64_t i=0; i<oec_tree->GetEntries(); i++){ // i = 0 to nb of entries
            // we go to enter i data
            oec_tree->GetEntry(i);
            // same for sim data
            simh_tree->GetEntry(i);   

            //det_id = m_counter
            //detsim_tree->GetEntry(detid)
            // we define the energy
            float oec_energy = oecobj->getEnergy();
            my_histo->Fill(oec_energy);

            int oec_tag_int =oecobj->getTag(); // to see if muons are detected as neutrinos

            outfile_oec_tags<<oecobj->isMuon() <<"\t"<< oecobj->isTTMuon() <<"\t"<< f <<"\t"<< i << oec_energy <<"\t"<< oec_tag_int <<"\t"<< intToA(oec_tag_int,16) <<endl;

            // check if TT muons :
            // if(oecobj->isMuon() and oecobj->isTTMuon()==0 and oecobj->isWPMuon()==0){
            //     //cout << " Event in CD; " << " OECentries : " << i << endl;
            //     n_oec+=1;
            //     //cout << i << "   " << simobj->getEventID() << "   " << oecobj->isWPMuon() << "   " << oecobj->isTTMuon() << endl;


            // }

            const std::string& oec_evt_type = headobj->getEventType();
            std::string theoec_evt_type = oec_evt_type;
            std::istringstream ss(theoec_evt_type);
            std::string token;
            vector<string> playerInfoVector;
            while(std::getline(ss, token, ':')) {
              token.erase(std::remove( token.begin(), token.end(), ';'), token.end());
              playerInfoVector.push_back(token);
            }
            
            if(playerInfoVector.size()>0 and oecobj->isTTMuon()==0 and oecobj->isWPMuon()==0){
                int this_idx = stoi(playerInfoVector[1]);
                if(last_idx != this_idx){
                    n_true+=1;
                    if(oecobj->isMuon()) n_oec+=1;
                    //cout << i << "   "  << playerInfoVector[0] << "  " << playerInfoVector[1] << "   " << oecobj->isWPMuon() << "   " << oecobj->isTTMuon() << "   " << oecobj->isMuon() << "   " << oecobj->getEnergy() << endl;
                }
                //if(oecobj->isMuon()) n_oec+=1;
                last_idx = this_idx;
            }
            if(playerInfoVector.size()==0 and oecobj->isTTMuon()==0 and oecobj->isWPMuon()==0){
                    if(oecobj->isMuon()) nbad+=1;
            }


        } // end of entries loop

        //OECfile->Close();
        //delete OECfile;
        //delete oecobj;
        //delete simobj;

        } // end of else

    } // end of files loop

    eff_trig = (static_cast<float>(n_true)/(n_trig*200))*100;
    eff_TT = (static_cast<float>(n_oec)/n_true)*100;

    cout << n_oec << endl;
    cout << n_true << endl;
    cout << "Efficiency in CD = " << eff_TT << "%" << " bad tags: " << nbad << endl;
    //cout << n_trig << endl;
    cout << "Efficiency trigger = " << eff_trig << "%" << endl;


    TCanvas* cva = new TCanvas();
    cva->cd();
    cva->SetLogy();
    my_histo->Draw();
    cva->Print("energy-plot.png");
}