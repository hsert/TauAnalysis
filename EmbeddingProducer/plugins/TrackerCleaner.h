/** \class TrackerCleaner
 *
 * Merge collections of calorimeter recHits
 * for original Zmumu event and "embedded" simulated tau decay products
 * (detectors supported at the moment: EB/EE, HB/HE and HO)
 * 
 * \author Stefan Wayand;
 *         Christian Veelken, LLR
 *
 * \version $Revision: 1.9 $
 *
 * $Id: TrackerCleaner.h,v 1.9 2013/03/23 09:12:51 veelken Exp $
 *
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonEnergy.h"

#include "TrackingTools/TrackAssociator/interface/TrackAssociatorParameters.h"
#include "TrackingTools/TrackAssociator/interface/TrackDetectorAssociator.h"
#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"

#include "DataFormats/Common/interface/SortedCollection.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/Common/interface/DetSetVectorNew.h"
#include "DataFormats/TrackerRecHit2D/interface/BaseTrackerRecHit.h"
#include "DataFormats/TrackerRecHit2D/interface/OmniClusterRef.h"


//#include "TauAnalysis/MCEmbeddingTools/interface/embeddingAuxFunctions.h"
#include <string>
#include <iostream>
#include <map>

template <typename T>
struct TrackerCleaner_mixedRecHitInfoType
{
  uint32_t rawDetId_;
  
  double energy1_;
  bool isRecHit1_;
  const T* recHit1_;
  
  double energy2_;
  bool isRecHit2_;
  const T* recHit2_;
  
  double energySum_;
  bool isRecHitSum_;
};

template <typename T>
class TrackerCleaner : public edm::EDProducer 
{
 public:
  explicit TrackerCleaner(const edm::ParameterSet&);
  ~TrackerCleaner();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<edm::View<pat::Muon> > mu_input_;
  typedef edmNew::DetSetVector<T> TrackClusterCollection;
  
  const edm::EDGetTokenT<TrackClusterCollection > trackClusterClusters_;
  
  bool test_veto_rechit(const TrackingRecHit *murechit);


};

template <typename T>
TrackerCleaner<T>::TrackerCleaner(const edm::ParameterSet& iConfig) :
    mu_input_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("MuonCollection"))),
    trackClusterClusters_(consumes< TrackClusterCollection>(iConfig.getParameter<edm::InputTag>("oldCollection"))) 
{
    produces<TrackClusterCollection>();
  
}


template <typename T>
TrackerCleaner<T>::~TrackerCleaner()
{
// nothing to be done yet...  
}


template <typename T>
void TrackerCleaner<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  
   using namespace edm;
   
   edm::Handle< edm::View<pat::Muon> > muonHandle;
   iEvent.getByToken(mu_input_, muonHandle);
   edm::View<pat::Muon> muons = *muonHandle;
   
   
   edm::Handle<TrackClusterCollection > inputClusters;
   iEvent.getByToken(trackClusterClusters_, inputClusters);

   std::vector<bool> vetodClusters;

   vetodClusters.resize(inputClusters->dataSize(), false);

   for (edm::View<pat::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {   
    if(!iMuon->isGlobalMuon() ) continue;
    reco::Track *mutrack = new reco::Track(*(iMuon->globalTrack() ));
  //  reco::Track *mutrack = new reco::Track(*(iMuon->innerTrack() ));
    for (trackingRecHit_iterator hitIt = mutrack->recHitsBegin(); hitIt != mutrack->recHitsEnd(); ++hitIt) {
        const TrackingRecHit &murechit = **hitIt;     
        if(!(murechit).isValid()) continue;

	if (test_veto_rechit(&murechit)){
	  auto & thit = reinterpret_cast<BaseTrackerRecHit const&>(murechit);
          auto const & cluster = thit.firstClusterRef();
	  vetodClusters[cluster.key()]=true;
	}
	
	    
     }	
  }
  std::auto_ptr<TrackClusterCollection > output(new TrackClusterCollection());

    int idx = 0;
    for ( typename TrackClusterCollection::const_iterator clustSet = inputClusters->begin(); clustSet != inputClusters->end(); ++clustSet ) { 
  //  for (SiPixelClusterCollectionNew::const_iterator clustSet = pixelClusters->begin(); clustSet!=pixelClusters->end(); ++clustSet) {
      DetId detIdObject( clustSet->detId() );
      typename TrackClusterCollection::FastFiller spc(*output, detIdObject);
      for (typename edmNew::DetSet<T>::const_iterator clustIt = clustSet->begin(); clustIt != clustSet->end(); ++clustIt ) { 
      //for(edmNew::DetSet<SiPixelCluster>::const_iterator clustIt = clustSet->begin(); clustIt!=clustSet->end();++clustIt) {
        idx++;  
        if (vetodClusters[idx-1]) continue;
        spc.push_back(*clustIt);
      }
    }
  iEvent.put(output);
  
  
}
