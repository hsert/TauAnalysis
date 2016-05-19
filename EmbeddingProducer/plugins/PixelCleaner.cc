// -*- C++ -*-
//
// Package:    Cleaner/PixelCleaner
// Class:      PixelCleaner
// 
/**\class PixelCleaner PixelCleaner.cc Cleaner/PixelCleaner/plugins/PixelCleaner.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stefan Wayand
//         Created:  Fri, 15 Apr 2016 09:10:57 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "DataFormats/MuonReco/interface/Muon.h"

#include "DataFormats/CSCRecHit/interface/CSCRecHit2D.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/CSCRecHit/interface/CSCRecHit2DCollection.h"
#include "DataFormats/MuonReco/interface/Muon.h"

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"


#include "RecoLocalTracker/SiStripRecHitConverter/interface/SiStripRecHitConverterAlgorithm.h"
#include "DataFormats/Common/interface/ContainerMask.h"
#include "TrackingTools/PatternTools/interface/TrackCollectionTokens.h"


#include "DataFormats/TrackerRecHit2D/interface/SiPixelRecHit.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit1D.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit2D.h"
#include "DataFormats/TrackerRecHit2D/interface/ProjectedSiStripRecHit2D.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripMatchedRecHit2D.h"
#include <DataFormats/SiStripDetId/interface/SiStripDetId.h>


#include <iostream>
#include <map>
#include <string>
//
// class declaration
//

class PixelCleaner : public edm::stream::EDProducer<> {
   public:
      explicit PixelCleaner(const edm::ParameterSet&);
      ~PixelCleaner();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginStream(edm::StreamID) override;
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      virtual void endStream() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      using PixelMaskContainer = edm::ContainerMask<edmNew::DetSetVector<SiPixelCluster>>;
      
      
      const edm::EDGetTokenT<edm::View<reco::Muon> > mu_input_;
// const TrackCollectionTokens trajectories_;
      
      const edm::EDGetTokenT<edmNew::DetSetVector<SiPixelCluster> > pixelClusters_;
      
      
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
PixelCleaner::PixelCleaner(const edm::ParameterSet& iConfig) :
    mu_input_(consumes<edm::View<reco::Muon> >(iConfig.getParameter<edm::InputTag>("MuonCollection"))),
   // trajectories_(iConfig.getParameter<edm::InputTag>("trajectories"),consumesCollector()),
    pixelClusters_(consumes<edmNew::DetSetVector<SiPixelCluster> >(iConfig.getParameter<edm::InputTag>("pixelClusters"))) 
  {

    produces<SiPixelClusterCollectionNew>(); 
    


  
}


PixelCleaner::~PixelCleaner()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
PixelCleaner::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   
   edm::Handle< edm::View<reco::Muon> > muonHandle;
   iEvent.getByToken(mu_input_, muonHandle);
   edm::View<reco::Muon> muons = *muonHandle;
   
   
   edm::Handle<edmNew::DetSetVector<SiPixelCluster> > pixelClusters;
   iEvent.getByToken(pixelClusters_, pixelClusters);

   std::vector<bool> vetodPixels;

  vetodPixels.resize(pixelClusters->dataSize(), false);

  for (edm::View<reco::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {
      
    if(!iMuon->isGlobalMuon() ) continue;
  reco::Track *mutrack = new reco::Track(*(iMuon->globalTrack() ));

  //  reco::Track *mutrack = new reco::Track(*(iMuon->innerTrack() ));

        for (trackingRecHit_iterator hitIt = mutrack->recHitsBegin(); hitIt != mutrack->recHitsEnd(); ++hitIt) {
        const TrackingRecHit &murechit = **hitIt;     
            if(!(murechit).isValid()) continue;
	    bool is_tracker =false;

	    const std::type_info &hit_type = typeid(murechit);
            if (hit_type == typeid(SiPixelRecHit)) {is_tracker = true; }
            else if (hit_type == typeid(SiStripRecHit2D)) { is_tracker = true; }
            else if (hit_type == typeid(SiStripRecHit1D)) {is_tracker = true; }
            else if (hit_type == typeid(SiStripMatchedRecHit2D)) { is_tracker = true; } 
            else if (hit_type == typeid(ProjectedSiStripRecHit2D)) { is_tracker = true; }
	
    
	    if (is_tracker){
	    auto & thit = reinterpret_cast<BaseTrackerRecHit const&>(murechit);
            auto const & cluster = thit.firstClusterRef();
	    if (cluster.isPixel()) vetodPixels[cluster.key()]=true;
	    }
	    
        }
  }
  std::auto_ptr<edmNew::DetSetVector<SiPixelCluster> > output(new edmNew::DetSetVector<SiPixelCluster>());

    int idx = 0;
    for (SiPixelClusterCollectionNew::const_iterator clustSet = pixelClusters->begin(); clustSet!=pixelClusters->end(); ++clustSet) {
      DetId detIdObject( clustSet->detId() );
      edmNew::DetSetVector<SiPixelCluster>::FastFiller spc(*output, detIdObject);
      for(edmNew::DetSet<SiPixelCluster>::const_iterator clustIt = clustSet->begin(); clustIt!=clustSet->end();++clustIt) {
        idx++;  
        if (vetodPixels[idx-1]) continue;
        spc.push_back(*clustIt);
      }
    }
 // std::cout<<"Pixel Cluster:\t"<<output->dataSize()<<"\t"<<pixelClusters->dataSize()<<" "<<idx<<std::endl;
  iEvent.put(output);
  
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void
PixelCleaner::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void
PixelCleaner::endStream() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
PixelCleaner::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
PixelCleaner::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
PixelCleaner::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
PixelCleaner::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PixelCleaner::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PixelCleaner);
