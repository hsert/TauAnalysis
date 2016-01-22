// -*- C++ -*-
//
// Package:    test/EmbeddingLHEProducer
// Class:      EmbeddingLHEProducer
// 
/**\class EmbeddingLHEProducer EmbeddingLHEProducer.cc test/EmbeddingLHEProducer/plugins/EmbeddingLHEProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stefan Wayand
//         Created:  Wed, 13 Jan 2016 08:15:01 GMT
//
//


// system include files
#include <memory>
#include "TLorentzVector.h"
//#include "boost/bind.hpp"
//#include "boost/shared_ptr.hpp"
#include "boost/ptr_container/ptr_deque.hpp"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Muon.h"


#include "SimDataFormats/GeneratorProducts/interface/LesHouches.h"
#include "SimDataFormats/GeneratorProducts/interface/LHECommonBlocks.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEXMLStringProduct.h"

#include "GeneratorInterface/LHEInterface/interface/LHERunInfo.h"
#include "GeneratorInterface/LHEInterface/interface/LHEEvent.h"
#include "GeneratorInterface/LHEInterface/interface/LHEReader.h"



//
// class declaration
//





class EmbeddingLHEProducer : public edm::one::EDProducer<edm::BeginRunProducer,
                                                        edm::EndRunProducer> {
   public:
      explicit EmbeddingLHEProducer(const edm::ParameterSet&);
      ~EmbeddingLHEProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      
      virtual void beginRunProduce(edm::Run& run, edm::EventSetup const& es) override;
      virtual void endRunProduce(edm::Run&, edm::EventSetup const&) override;
     // virtual void beginRun(edm::Run const &, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      void fill_lhe_from_mumu(TLorentzVector &positiveLepton, TLorentzVector &negativeLepton, lhef::HEPEUP &outlhe);
      
      
      // ----------member data ---------------------------
      boost::shared_ptr<lhef::LHERunInfo>	runInfoLast;
      boost::shared_ptr<lhef::LHERunInfo>	runInfo;
      boost::shared_ptr<lhef::LHEEvent>	partonLevel;
      boost::ptr_deque<LHERunInfoProduct>	runInfoProducts;
      edm::EDGetTokenT<pat::MuonCollection> muonsCollection_;
      bool switchToTaus_;
      double leptonMass;
      
      
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
EmbeddingLHEProducer::EmbeddingLHEProducer(const edm::ParameterSet& iConfig)
{
   //register your products
   produces<LHEEventProduct>();
   produces<LHERunInfoProduct, edm::InRun>();
/* Examples
   produces<ExampleData2>();

   //if do put with a label
   produces<ExampleData2>("label");
 
   //if you want to put into the Run
   produces<ExampleData2,InRun>();
*/
   //now do what ever other initialization is needed
   muonsCollection_ = consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("src"));
   switchToTaus_ = iConfig.getParameter<bool>("switchToTaus");
   leptonMass = 1.77682 ? switchToTaus_ : 0.1056584;
}


EmbeddingLHEProducer::~EmbeddingLHEProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
EmbeddingLHEProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   
  // boost::shared_ptr<lhef::LHEEvent> partonLevel;
    // std::auto_ptr<LHEEventProduct> product(
//	       new LHEEventProduct(*partonLevel->getHEPEUP(),
//				   partonLevel->originalXWGTUP())
//	       );
   
   
//-13   1       col 1: 0        col 2: 0       f mom: 3        l mom: 3     -44.6966686     1.7242644       65.7211490      79.4987161      0.1056584   l time: 0.0000000  spin: 1.0000000
//13    1       col 1: 0        col 2: 0       f mom: 3        l mom: 3     44.6966686      -1.7242644      98.3669058      108.0593568     0.1056584   l time: 0.0000000  spin: -1.0000000  
   
    Handle<std::vector<pat::Muon>> coll_muons;
    iEvent.getByToken(muonsCollection_ , coll_muons);
    TLorentzVector positiveLepton, negativeLepton;
    bool mu_plus_found = false;
    bool mu_minus_found = false;

    lhef::HEPEUP hepeup;

    // Assuming Pt-Order
    for (std::vector<pat::Muon>::const_iterator muon=  coll_muons->begin(); muon!= coll_muons->end();  ++muon)
    {
      if (muon->charge() == 1 && !mu_plus_found)
      {
        positiveLepton.SetXYZM(muon->p4().px(),muon->p4().py(),muon->p4().pz(),leptonMass);
        mu_plus_found = true;
      }
      else if (muon->charge() == -1 && !mu_minus_found)
      {
        negativeLepton.SetXYZM(muon->p4().px(),muon->p4().py(),muon->p4().pz(),leptonMass);
        mu_minus_found = true;
      }
      else if (mu_minus_found && mu_plus_found) break;
    }
   
   fill_lhe_from_mumu(positiveLepton,negativeLepton,hepeup);
   
    
    double originalXWGTUP_=0.1;
     std::auto_ptr<LHEEventProduct> product(
	       new LHEEventProduct(hepeup,originalXWGTUP_)
	       );
     iEvent.put(product);

/* This is an event example
   //Read 'ExampleData' from the Event
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);

   //Use the ExampleData to create an ExampleData2 which 
   // is put into the Event
   std::unique_ptr<ExampleData2> pOut(new ExampleData2(*pIn));
   iEvent.put(std::move(pOut));
*/

/* this is an EventSetup example
   //Read SetupData from the SetupRecord in the EventSetup
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
*/
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
EmbeddingLHEProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
EmbeddingLHEProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------

void
EmbeddingLHEProducer::beginRunProduce(edm::Run &run, edm::EventSetup const&)
{
 // std::cout<<"aaa"<<std::endl;
  
     // fill HEPRUP common block and store in edm::Run
    lhef::HEPRUP heprup;
    lhef::CommonBlocks::readHEPRUP(&heprup);

  // make sure we write a valid LHE header, Herwig6Hadronizer
  // will interpret it correctly and set up LHAPDF
   heprup.PDFGUP.first = 0;
   heprup.PDFGUP.second = 0;

    std::auto_ptr<LHERunInfoProduct> runInfo(new LHERunInfoProduct(heprup));
  
   run.put(runInfo);
 
 // std::cout<<"vvv"<<std::endl;
  
}


 


void 
EmbeddingLHEProducer::endRunProduce(edm::Run& run, edm::EventSetup const& es)
{

  if (!runInfoProducts.empty()) {
    std::auto_ptr<LHERunInfoProduct> product(runInfoProducts.pop_front().release());
    run.put(product);
  }

}

void 
EmbeddingLHEProducer::fill_lhe_from_mumu(TLorentzVector &positiveLepton, TLorentzVector &negativeLepton, lhef::HEPEUP &outlhe){
  
    TLorentzVector Z_vec =  positiveLepton+negativeLepton;
    outlhe.resize(3);
    
//    double pz2 = -0.5*(Z_vec.E()-Z_vec.P());
 

    
    outlhe.IDUP[0]=23;
    outlhe.ISTUP[0]=2;
    outlhe.ICOLUP[0].first=0;
    outlhe.ICOLUP[0].second=0;
    outlhe.MOTHUP[0].first=0;
    outlhe.MOTHUP[0].second=0;
    outlhe.PUP[0][0]=Z_vec.Px();
    outlhe.PUP[0][1]=Z_vec.Py();
    outlhe.PUP[0][2]=Z_vec.Pz();
    outlhe.PUP[0][3]=Z_vec.E();
    outlhe.PUP[0][4]=Z_vec.M();
    outlhe.SPINUP[0]=9.0;
    
    
    outlhe.IDUP[1]=-15;
    outlhe.ISTUP[1]=1;
    outlhe.ICOLUP[1].first=0;
    outlhe.ICOLUP[1].second=0;
    outlhe.MOTHUP[1].first=1;
    outlhe.MOTHUP[1].second=1;
    outlhe.PUP[1][0]=positiveLepton.Px();
    outlhe.PUP[1][1]=positiveLepton.Py();
    outlhe.PUP[1][2]=positiveLepton.Pz();
    outlhe.PUP[1][3]=positiveLepton.E();
    outlhe.PUP[1][4]=positiveLepton.M();
    outlhe.SPINUP[1]=1.0;
    
    
    outlhe.IDUP[2]=15;
    outlhe.ISTUP[2]=1;
    outlhe.ICOLUP[2].first=0;
    outlhe.ICOLUP[2].second=0;
    outlhe.MOTHUP[2].first=1;
    outlhe.MOTHUP[2].second=1;
    outlhe.PUP[2][0]=negativeLepton.Px();
    outlhe.PUP[2][1]=negativeLepton.Py();
    outlhe.PUP[2][2]=negativeLepton.Pz();
    outlhe.PUP[2][3]=negativeLepton.E();
    outlhe.PUP[2][4]=negativeLepton.M();
    outlhe.SPINUP[2]=-1.0;
    
   // hepeup.IDUP[1]=-13;
    
// 2   -1      col 1: 501      col 2: 0        f mom: 0        l mom: 0    0.0000000       0.0000000       175.8230639     175.8230639     0.0000000  l time: 0.0000000   spin: -1.0000000
//-2   -1      col 1: 0        col 2: 501      f mom: 0        l mom: 0     0.0000000       0.0000000       -11.7350091     11.7350091      0.0000000   l time: 0.0000000  spin: 1.0000000
//23    2       col 1: 0        col 2: 0       f mom: 1        l mom: 2     0.0000000       0.0000000       164.0880548     187.5580730     90.8467996  l time: 0.0000000  spin: 9.0000000
//-13   1       col 1: 0        col 2: 0       f mom: 3        l mom: 3     -44.6966686     1.7242644       65.7211490      79.4987161      0.1056584   l time: 0.0000000  spin: 1.0000000
//13    1       col 1: 0        col 2: 0       f mom: 3        l mom: 3     44.6966686      -1.7242644      98.3669058      108.0593568     0.1056584   l time: 0.0000000  spin: -1.0000000  
    

   


//    -3      -1      col 1: 0        col 2: 501      0.0000000       0.0000000       23.2430806      23.2430806      0.0000000
//3       -1      col 1: 501      col 2: 0        0.0000000       0.0000000       -88.2875737     88.2875737      0.0000000
//23      2       col 1: 0        col 2: 0        0.0000000       0.0000000       -65.0444930     111.5306543     90.5996731
//-13     1       col 1: 0        col 2: 0        -36.2418089     1.5554354       0.8786733       36.2859660      0.1056584
//13      1       col 1: 0        col 2: 0        36.2418089      -1.5554354      -65.9231664     75.2446883      0.1056584

    
  
  
  
  
  
 return; 
} 




// ------------ method called when ending the processing of a run  ------------
/*
void
EmbeddingLHEProducer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
EmbeddingLHEProducer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
EmbeddingLHEProducer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EmbeddingLHEProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(EmbeddingLHEProducer);
