// -*- C++ -*-
//
// Package:    TauAnalysis_new/EmbeddingProducer
// Class:      EmbeddingProducer
// 
/**\class EmbeddingProducer EmbeddingProducer.cc TauAnalysis_new/EmbeddingProducer/plugins/EmbeddingProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stefan Wayand
//         Created:  Wed, 09 Dec 2015 13:14:54 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"


#include "DataFormats/PatCandidates/interface/Muon.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenFilterInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "GeneratorInterface/Pythia8Interface/interface/Py8InterfaceBase.h"
//#include "GeneratorInterface/Pythia8Interface/interface/P8RndmEngine.h"
//#include "CLHEP/Random/RandomEngine.h"

//
// class declaration
//

class EmbeddingProducer : public edm::EDProducer {
   public:
      explicit EmbeddingProducer(const edm::ParameterSet&);
      ~EmbeddingProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      
      void reset_event_content();
      void add_to_event(edm::Event& iEvent);
      
      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::EDGetTokenT<pat::MuonCollection> muonsCollection_;
      edm::InputTag srcHepMC_;
      bool mixHepMC_;


      // the "fake" MC event from the embeded source
      //HepMC::GenEvent* genEvt_output;
      std::auto_ptr<HepMC::GenEvent> genEvent_;
      std::auto_ptr<GenEventInfoProduct> genEventInfo_;
      
      
      // How often does the embedded event pass the kinematic requirments (pt and eta)
      unsigned int numEvents_tried;
      unsigned int numEvents_passed;
     
      
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
EmbeddingProducer::EmbeddingProducer(const edm::ParameterSet& iConfig){   
  
  muonsCollection_ = consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("src"));
  mixHepMC_ = iConfig.getParameter<bool>("mixHepMc");
  if (mixHepMC_) srcHepMC_ = iConfig.getParameter<edm::InputTag>("hepMcSrc");
  
   produces<GenFilterInfo>("minVisPtFilter");
   produces<GenEventInfoProduct>("");
}


EmbeddingProducer::~EmbeddingProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
EmbeddingProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  reset_event_content();
  
   using namespace edm;
   Handle<std::vector<pat::Muon>> coll_muons;
   iEvent.getByToken(muonsCollection_ , coll_muons);
   
   unsigned key=0;  
   for (std::vector<pat::Muon>::const_iterator muon=  coll_muons->begin(); muon!= coll_muons->end();  ++muon,  ++key){ 
     std::cout<<"aaa"<<std::endl; 
     
  }
  std::cout<<"----------------------------------------------------"<<std::endl;
   
   
  add_to_event(iEvent);
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
EmbeddingProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EmbeddingProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
EmbeddingProducer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
EmbeddingProducer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
EmbeddingProducer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
EmbeddingProducer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EmbeddingProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}



// user functions 
void 
EmbeddingProducer::reset_event_content(){
  
  numEvents_tried  = 0;
  numEvents_passed = 0;
  genEvent_.reset(new HepMC::GenEvent);
  //genEvt_output = new HepMC::GenEvent();
  
}

void
EmbeddingProducer::add_to_event(edm::Event& iEvent){
  
    std::auto_ptr<GenFilterInfo> kinfilter(new GenFilterInfo(numEvents_tried, numEvents_passed));
    iEvent.put(kinfilter, std::string("minVisPtFilter"));
  
  
    std::auto_ptr<GenEventInfoProduct> generator(new GenEventInfoProduct());
    iEvent.put(generator, std::string(""));
}



















//define this as a plug-in
DEFINE_FWK_MODULE(EmbeddingProducer);
