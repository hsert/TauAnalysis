#include "DYToMuMuFilter.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"


DYToMuMuFilter::DYToMuMuFilter(const edm::ParameterSet& iConfig):
    inputTag_(iConfig.getParameter<edm::InputTag>("inputTag"))
{
}


DYToMuMuFilter::~DYToMuMuFilter() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


bool DYToMuMuFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {


    edm::Handle<reco::GenParticleCollection> gen_handle;
    iEvent.getByLabel(inputTag_, gen_handle);
    
    for(unsigned int i = 0; i < gen_handle->size(); i++)
    {
		// Check if Z Boson decayed into two leptons
		if (gen_handle->at(i).pdgId() == 23 && gen_handle->at(i).numberOfDaughters() == 2)
		{
			//Debug output
			//std::cout << "pdgId" << gen_handle->at(i).pdgId() << std::endl;
			//std::cout << "nDau" << gen_handle->at(i).numberOfDaughters() << std::endl;
			//std::cout << "Dau1" << gen_handle->at(i)->daughters->at(0).pdgId() << std::endl;
			//std::cout << "Dau2" << gen_handle->at(i).numberOfDaughters() << std::endl;
			//std::cout << "Dau1 " << gen_handle->at(i).daughter(0)->pdgId() << std::endl;
			//std::cout << "Dau2 " << gen_handle->at(i).daughter(1)->pdgId() << std::endl;
			//std::cout << gen_handle->at(i).daughter(1)->pdgId()+gen_handle->at(i).daughter(0)->pdgId() << std::endl;
			
			// Check if daugther particles are muons
		  if (abs(gen_handle->at(i).daughter(0)->pdgId()) == 13  
		      && fabs(gen_handle->at(i).daughter(0)->eta())<2.8  
		      && fabs(gen_handle->at(i).daughter(1)->eta())<2.8)
			{
			  //std::cout << "pdgId" << gen_handle->at(i).pdgId() << std::endl;
			  //std::cout << "nDau" << gen_handle->at(i).numberOfDaughters() << std::endl;
			  //std::cout << "Dau1 " << gen_handle->at(i).daughter(0)->pdgId() << std::endl;
			  //std::cout << "Dau1 pt " << gen_handle->at(i).daughter(0)->pt() << std::endl;
			  //std::cout << "Dau1 pt " << gen_handle->at(i).daughter(0)->eta() << std::endl;
			  //std::cout << "Dau2 " << gen_handle->at(i).daughter(1)->pdgId() << std::endl;
			  //std::cout << "Dau2 pt " << gen_handle->at(i).daughter(1)->pt() << std::endl;
			  //std::cout << "Dau2 pt " << gen_handle->at(i).daughter(1)->eta() << std::endl;
			  //std::cout << gen_handle->at(i).daughter(1)->pdgId()+gen_handle->at(i).daughter(0)->pdgId() << std::endl;
			  return true;
			}
			else
			{ 
				return false;
			}
		}
    }
    return false;
}

// ------------ method called once each job just before starting event loop  ------------
void DYToMuMuFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void DYToMuMuFilter::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool DYToMuMuFilter::beginRun(edm::Run&, edm::EventSetup const&) { 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool DYToMuMuFilter::endRun(edm::Run&, edm::EventSetup const&) {
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
DYToMuMuFilter::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool DYToMuMuFilter::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void DYToMuMuFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(DYToMuMuFilter);
