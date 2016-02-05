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
      void fill_lhe_with_particle(TLorentzVector &particle, double spin, int motherindex, int pdgid, int status, lhef::HEPEUP &outlhe);
      
      void transform_mumu_to_tautau(TLorentzVector &positiveLepton, TLorentzVector &negativeLepton);
      void mirror(TLorentzVector &positiveLepton, TLorentzVector &negativeLepton);
      
      // ----------member data ---------------------------
      boost::shared_ptr<lhef::LHERunInfo>	runInfoLast;
      boost::shared_ptr<lhef::LHERunInfo>	runInfo;
      boost::shared_ptr<lhef::LHEEvent>	partonLevel;
      boost::ptr_deque<LHERunInfoProduct>	runInfoProducts;
      edm::EDGetTokenT<pat::MuonCollection> muonsCollection_;
      bool switchToMuonEmbedding_;
      bool mirroring_;
      const double tauMass_ = 1.77682;
      
      
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
   switchToMuonEmbedding_ = iConfig.getParameter<bool>("switchToMuonEmbedding");
   mirroring_ = iConfig.getParameter<bool>("mirroring");
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
        positiveLepton.SetPxPyPzE(muon->p4().px(),muon->p4().py(),muon->p4().pz(), muon->p4().e());
        mu_plus_found = true;
      }
      else if (muon->charge() == -1 && !mu_minus_found)
      {
        negativeLepton.SetPxPyPzE(muon->p4().px(),muon->p4().py(),muon->p4().pz(), muon->p4().e());
        mu_minus_found = true;
      }
      else if (mu_minus_found && mu_plus_found) break;
    }
    
    transform_mumu_to_tautau(positiveLepton,negativeLepton); // if MuonEmbedding, function does nothing.
    mirror(positiveLepton,negativeLepton); // if no mirroring, function does nothing.
    fill_lhe_from_mumu(positiveLepton,negativeLepton,hepeup);
    
    double originalXWGTUP_ = 0.1;
    std::auto_ptr<LHEEventProduct> product( new LHEEventProduct(hepeup,originalXWGTUP_) );
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
    // fill HEPRUP common block and store in edm::Run
    lhef::HEPRUP heprup;
    lhef::CommonBlocks::readHEPRUP(&heprup);

    // make sure we write a valid LHE header, Herwig6Hadronizer
    // will interpret it correctly and set up LHAPDF
    heprup.PDFGUP.first = 0;
    heprup.PDFGUP.second = 0;

    std::auto_ptr<LHERunInfoProduct> runInfo(new LHERunInfoProduct(heprup));
  
    run.put(runInfo);
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
EmbeddingLHEProducer::fill_lhe_from_mumu(TLorentzVector &positiveLepton, TLorentzVector &negativeLepton, lhef::HEPEUP &outlhe)
{
    TLorentzVector Z = positiveLepton + negativeLepton;
    int leptonPDGID = switchToMuonEmbedding_ ? 13 : 15;
    fill_lhe_with_particle(Z,9.0,0,23,2,outlhe);
    fill_lhe_with_particle(positiveLepton,1.0,1,-leptonPDGID,1,outlhe);
    fill_lhe_with_particle(negativeLepton,-1.0,1,leptonPDGID,1,outlhe);
    
    return;
}

void EmbeddingLHEProducer::fill_lhe_with_particle(TLorentzVector &particle, double spin, int motherindex, int pdgid, int status, lhef::HEPEUP &outlhe)
{
    // Pay attention to different index conventions:
    // 'particleindex' follows usual C++ index conventions starting at 0 for a list.
    // 'motherindex' follows the LHE index conventions: 0 is for 'not defined', so the listing starts at 1.
    // That means: LHE index 1 == C++ index 0.
    //std::cout << "old NUP: " << outlhe.NUP << std::endl;
    int particleindex = outlhe.NUP;
    outlhe.resize(outlhe.NUP+1);
    //std::cout << "new NUP: " << outlhe.NUP << std::endl;
    //std::cout << "particle index C++: " << particleindex << std::endl;
    
    outlhe.PUP[particleindex][0] = particle.Px();
    outlhe.PUP[particleindex][1] = particle.Py();
    outlhe.PUP[particleindex][2] = particle.Pz();
    outlhe.PUP[particleindex][3] = particle.E();
    outlhe.PUP[particleindex][4] = particle.M();
    outlhe.SPINUP[particleindex] = spin;
    outlhe.ICOLUP[particleindex].first = 0;
    outlhe.ICOLUP[particleindex].second = 0;
    
    outlhe.MOTHUP[particleindex].first = motherindex;
    outlhe.MOTHUP[particleindex].second = motherindex;
    outlhe.IDUP[particleindex] = pdgid;
    outlhe.ISTUP[particleindex] = status;
    
    return;
}




void EmbeddingLHEProducer::transform_mumu_to_tautau(TLorentzVector &positiveLepton, TLorentzVector &negativeLepton)
{
    // No corrections applied for muon embedding
    if (switchToMuonEmbedding_) return;

    TLorentzVector Z = positiveLepton + negativeLepton;

    TVector3 boost_from_Z_to_LAB = Z.BoostVector();
    TVector3 boost_from_LAB_to_Z = -Z.BoostVector();

    // Boosting the two leptons to Z restframe, then both are back to back. This means, same 3-momentum squared
    positiveLepton.Boost(boost_from_LAB_to_Z);
    negativeLepton.Boost(boost_from_LAB_to_Z);

    // Energy of tau = 0.5*Z-mass
    double tau_mass_squared = tauMass_*tauMass_;
    double tau_energy_squared = 0.25*Z.M2();
    double tau_3momentum_squared = tau_energy_squared - tau_mass_squared;
    if (tau_3momentum_squared < 0)
    {
        std::cout << "3-Momentum squared is negative" << std::endl;
        return;
    }
    
    //Computing scale, applying it on the 3-momenta and building new 4 momenta of the taus
    double scale = std::sqrt(tau_3momentum_squared/positiveLepton.Vect().Mag2());
    positiveLepton.SetPxPyPzE(scale*positiveLepton.Px(),scale*positiveLepton.Py(),scale*positiveLepton.Pz(),std::sqrt(tau_energy_squared));
    negativeLepton.SetPxPyPzE(scale*negativeLepton.Px(),scale*negativeLepton.Py(),scale*negativeLepton.Pz(),std::sqrt(tau_energy_squared));

    //Boosting the new taus back to LAB frame
    positiveLepton.Boost(boost_from_Z_to_LAB);
    negativeLepton.Boost(boost_from_Z_to_LAB);

    return;
}

void EmbeddingLHEProducer::mirror(TLorentzVector &positiveLepton, TLorentzVector &negativeLepton)
{
    if (!mirroring_) return;

    // By construction, the 3-momenta of mu-, mu+ and Z are in one plane. 
    // That means, one vector for perpendicular projection can be used for both leptons.
    TLorentzVector Z = positiveLepton + negativeLepton;

    TVector3 Z3 = Z.Vect();
    TVector3 positiveLepton3 = positiveLepton.Vect();
    TVector3 negativeLepton3 = negativeLepton.Vect();

    TVector3 p3_perp = positiveLepton3 - positiveLepton3.Dot(Z3)/Z3.Dot(Z3)*Z3;
    p3_perp = p3_perp.Unit();

    positiveLepton3 -= 2*positiveLepton3.Dot(p3_perp)*p3_perp;
    negativeLepton3 -= 2*negativeLepton3.Dot(p3_perp)*p3_perp;

    positiveLepton.SetVect(positiveLepton3);
    negativeLepton.SetVect(negativeLepton3);

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
