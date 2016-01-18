#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

class DYToMuMuGenFilter: public edm::EDFilter {
public:
  explicit DYToMuMuGenFilter(const edm::ParameterSet&);
  ~DYToMuMuGenFilter();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  virtual void beginJob() override;
  virtual bool filter(edm::Event&, const edm::EventSetup&)override;
  virtual void endJob() override;
  edm::InputTag inputTag_;
  edm::EDGetTokenT<reco::GenParticleCollection> genParticleCollection_;
  
  //virtual bool beginRun(edm::Run&, edm::EventSetup const&)override;
  // virtual bool endRun(edm::Run&, edm::EventSetup const&)override;
  //virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)override;
  //virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)override;

};


DYToMuMuGenFilter::DYToMuMuGenFilter(const edm::ParameterSet& iConfig)
{
  inputTag_= iConfig.getParameter<edm::InputTag>("inputTag");
  genParticleCollection_ = consumes<reco::GenParticleCollection>(inputTag_);
}


DYToMuMuGenFilter::~DYToMuMuGenFilter() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


bool DYToMuMuGenFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {


    edm::Handle<reco::GenParticleCollection> gen_handle;
    iEvent.getByToken(genParticleCollection_, gen_handle);
    
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
		      && fabs(gen_handle->at(i).daughter(0)->eta())<2.5  
		      && fabs(gen_handle->at(i).daughter(1)->eta())<2.5
		      && gen_handle->at(i).daughter(0)->pt()>8
		      && gen_handle->at(i).daughter(1)->pt()>8)
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
void DYToMuMuGenFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void DYToMuMuGenFilter::endJob() {
}
/*
// ------------ method called when starting to processes a run  ------------
bool DYToMuMuGenFilter::beginRun(edm::Run&, edm::EventSetup const&) { 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool DYToMuMuGenFilter::endRun(edm::Run&, edm::EventSetup const&) {
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
DYToMuMuGenFilter::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool DYToMuMuGenFilter::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
  return true;
}
*/
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void DYToMuMuGenFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(DYToMuMuGenFilter);
