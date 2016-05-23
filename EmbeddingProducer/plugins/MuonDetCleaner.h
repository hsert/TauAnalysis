/** \class MuonDetCleaner
 *
 * Clean collections of hits in muon detectors (CSC, DT and RPC)
 * for original Zmumu event and "embedded" simulated tau decay products
 * 
 * \author Christian Veelken, LLR
 *
 * \version $Revision: 1.2 $
 *
 * $Id: MuonDetCleaner.h,v 1.2 2012/12/13 09:52:06 veelken Exp $
 *
 * Clean Up from STefan Wayand, KIT
 * 
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/Common/interface/RangeMap.h"
#include "DataFormats/Common/interface/OwnVector.h"

#include "TauAnalysis/MCEmbeddingTools/interface/embeddingAuxFunctions.h"



#include <string>
#include <vector>
#include <map>

template <typename T1, typename T2>
class MuonDetCleaner : public edm::EDProducer 
{
 public:
  explicit MuonDetCleaner(const edm::ParameterSet&);
  ~MuonDetCleaner();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  typedef edm::RangeMap<T1, edm::OwnVector<T2> > RecHitCollection;

  typedef std::map<uint32_t, int> detIdToIntMap;

  void addRecHits(std::map<T1, std::vector<T2> >&, const RecHitCollection&, bool, const detIdToIntMap&, const detIdToIntMap&, int&);
  void fillVetoHits(const TrackingRecHit& , std::vector<uint32_t>* );
  
  uint32_t getRawDetId(const T2&);
  bool checkrecHit(const TrackingRecHit&);
  
  

  const edm::EDGetTokenT<edm::View<reco::Muon> > mu_input_;
  const edm::EDGetTokenT<RecHitCollection > RecHitinput_;
  
  
  
};

template <typename T1, typename T2>
MuonDetCleaner<T1,T2>::MuonDetCleaner(const edm::ParameterSet& iConfig):
    mu_input_(consumes<edm::View<reco::Muon> >(iConfig.getParameter<edm::InputTag>("MuonCollection"))),
    RecHitinput_(consumes< RecHitCollection>(iConfig.getParameter<edm::InputTag>("oldCollection"))) 
{
    produces<RecHitCollection>();
    
}

template <typename T1, typename T2>
MuonDetCleaner<T1,T2>::~MuonDetCleaner()
{
// nothing to be done yet...  
}

template <typename T1, typename T2>
void MuonDetCleaner<T1,T2>::produce(edm::Event& iEvent, const edm::EventSetup& es)
{
   std::map<T1, std::vector<T2> > recHits_output; // This data format is easyer to handle
   //std::auto_ptr<detIdToIntMap> vetoHits(new detIdToIntMap());
   std::vector<uint32_t> vetoHits;
  
  // First fill the veto RecHits colletion with the Hits from the input muons
   edm::Handle< edm::View<reco::Muon> > muonHandle;
   iEvent.getByToken(mu_input_, muonHandle);
   edm::View<reco::Muon> muons = *muonHandle;
   for (edm::View<reco::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {
     if(!iMuon->isGlobalMuon() ) continue;
     reco::Track *mutrack = new reco::Track(*(iMuon->outerTrack() ));
     //reco::Track *mutrack = new reco::Track(*(muon.globalTrack() ));
       for (trackingRecHit_iterator hitIt = mutrack->recHitsBegin(); hitIt != mutrack->recHitsEnd(); ++hitIt) {
        const TrackingRecHit &murechit = **hitIt; // Base class for all rechits 
        if(!(murechit).isValid()) continue;
        if (!checkrecHit(murechit)) continue;   // Check if the hit belongs to a specifc detector section   
        fillVetoHits(murechit,&vetoHits); // Go back to the very basic rechits 
       }
   }

   
   // Second read in the RecHit Colltection which is to be replaced, without the vetoRecHits
    typedef edm::Handle<RecHitCollection> RecHitCollectionHandle;
    RecHitCollectionHandle RecHitinput;
    iEvent.getByToken(RecHitinput_, RecHitinput);
    for ( typename RecHitCollection::const_iterator recHit = RecHitinput->begin(); recHit != RecHitinput->end(); ++recHit ) { // loop over the basic rec hit collection (DT CSC or RPC)
	if (find(vetoHits.begin(),vetoHits.end(),getRawDetId(*recHit)) != vetoHits.end()) continue; // If the hit is not in the  	
	T1 detId(getRawDetId(*recHit));
	recHits_output[detId].push_back(*recHit);	
    }
  
    
    
    // Last step savet the output in the CMSSW Data Format
    std::auto_ptr<RecHitCollection> output(new RecHitCollection());
    for ( typename std::map<T1, std::vector<T2> >::const_iterator recHit = recHits_output.begin(); recHit != recHits_output.end(); ++recHit ) {
      output->put(recHit->first, recHit->second.begin(), recHit->second.end());
    }
    output->post_insert();

    iEvent.put(output);
}


template <typename T1, typename T2>
void MuonDetCleaner<T1,T2>::fillVetoHits(const TrackingRecHit& rh, std::vector<uint32_t>* HitsList)
{
    std::vector<const TrackingRecHit*> rh_components = rh.recHits();
    if ( rh_components.size() == 0 ) {
      HitsList->push_back(rh.rawId());
    } 
    else {
      for ( std::vector<const TrackingRecHit*>::const_iterator rh_component = rh_components.begin(); rh_component != rh_components.end(); ++rh_component ) {
	fillVetoHits(**rh_component, HitsList);
      }
    }
}









