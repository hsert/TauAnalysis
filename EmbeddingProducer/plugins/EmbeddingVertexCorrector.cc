// -*- C++ -*-
//
// Package:    TauAnalysis/EmbeddingProducer
// Class:      EmbeddingVertexCorrector
// 
/**\class EmbeddingVertexCorrector EmbeddingVertexCorrector.cc TauAnalysis/EmbeddingProducer/plugins/EmbeddingVertexCorrector.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Artur Akhmetshin
//         Created:  Sat, 23 Apr 2016 21:47:13 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "CLHEP/Units/GlobalSystemOfUnits.h"
#include "CLHEP/Units/GlobalPhysicalConstants.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/LorentzVectorFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

namespace HepMC {
   class FourVector ;
}

//
// class declaration
//

class EmbeddingVertexCorrector : public edm::stream::EDProducer<> {
   public:
      explicit EmbeddingVertexCorrector(const edm::ParameterSet&);
      ~EmbeddingVertexCorrector();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      //virtual void beginStream(edm::StreamID) override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      //virtual void endStream() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::InputTag sourceLabel;
      edm::InputTag vertexPositionLabel;
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
EmbeddingVertexCorrector::EmbeddingVertexCorrector(const edm::ParameterSet& iConfig)
{
   //register your products
/* Examples
   produces<ExampleData2>();

   //if do put with a label
   produces<ExampleData2>("label");
 
   //if you want to put into the Run
   produces<ExampleData2,InRun>();
*/
   produces<edm::HepMCProduct>();
   
   //now do what ever other initialization is needed
   sourceLabel = iConfig.getParameter<edm::InputTag>("src");
   consumes<edm::HepMCProduct>(sourceLabel);
   vertexPositionLabel = edm::InputTag("externalLHEProducer","vertexPosition");
   consumes<math::XYZTLorentzVectorD>(vertexPositionLabel);

}


EmbeddingVertexCorrector::~EmbeddingVertexCorrector()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
EmbeddingVertexCorrector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
/* This is an event example
   //Read 'ExampleData' from the Event
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);

   //Use the ExampleData to create an ExampleData2 which 
   // is put into the Event
   std::unique_ptr<ExampleData2> pOut(new ExampleData2(*pIn));
   iEvent.put(std::move(pOut));
*/

   // Retrieving generated Z to TauTau Event 
   Handle<edm::HepMCProduct> InputGenEvent;
   iEvent.getByLabel(sourceLabel, InputGenEvent);
   
   HepMC::GenEvent* genevent = new HepMC::GenEvent(*InputGenEvent->GetEvent());
   std::unique_ptr<edm::HepMCProduct> CorrectedGenEvent(new edm::HepMCProduct(genevent));
   
   int counter = 0;
   for ( HepMC::GenEvent::vertex_iterator vt=genevent->vertices_begin();
                                          vt!=genevent->vertices_end(); ++vt )
   {
   counter++;

   //std::cout << std::setprecision(10) << "Former vertex information in mm: " << std::endl;
   //std::cout << "Vertex " << counter << ": X = " << (*vt)->position().x() << std::endl;
   }
   //std::cout << "Number of vertices: " << counter << std::endl;
   //Retrieving vertex position from input and creating vertex shift
   Handle<math::XYZTLorentzVectorD> vertex_position;
   iEvent.getByLabel(vertexPositionLabel, vertex_position);
   
   HepMC::FourVector* vertex_shift = new HepMC::FourVector(vertex_position.product()->x()*cm, vertex_position.product()->y()*cm, vertex_position.product()->z()*cm); 
   //std::cout << "vertex shift in mm in X: " << vertex_shift->x() << std::endl;
   // Apply vertex shift to all production vertices of the event
   CorrectedGenEvent->applyVtxGen(vertex_shift);
   //HepMC::GenEvent* corgenevent = new HepMC::GenEvent(*CorrectedGenEvent->GetEvent());
   //std::cout << "Corrected  X for Vertex 1: " << (*corgenevent->vertices_begin())->position().x() << std::endl;
   
   iEvent.put(std::move(CorrectedGenEvent));
/* this is an EventSetup example
   //Read SetupData from the SetupRecord in the EventSetup
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
*/
 
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
/*
void
EmbeddingVertexCorrector::beginStream(edm::StreamID)
{
}
*/
// ------------ method called once each stream after processing all runs, lumis and events  ------------
/*
void
EmbeddingVertexCorrector::endStream() {
}
*/
// ------------ method called when starting to processes a run  ------------
/*
void
EmbeddingVertexCorrector::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
EmbeddingVertexCorrector::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
EmbeddingVertexCorrector::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
EmbeddingVertexCorrector::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
EmbeddingVertexCorrector::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(EmbeddingVertexCorrector);
