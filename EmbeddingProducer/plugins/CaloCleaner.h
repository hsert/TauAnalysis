/** \class CaloCleaner
 *
 * Clean collections of calorimeter recHits
 * (detectors supported at the moment: EB/EE, HB/HE and HO)
 * 
 * \author Tomasz Maciej Frueboes;
 *         Christian Veelken, LLR
 *
 * \version $Revision: 1.9 $
 *
 * $Id: CaloCleaner.h,v 1.9 2013/03/23 09:12:51 veelken Exp $
 *
 *  Clean Up from STefan Wayand, KIT
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

//#include "TauAnalysis/MCEmbeddingTools/interface/embeddingAuxFunctions.h"
#include <string>
#include <iostream>
#include <map>

template <typename T>
class CaloCleaner : public edm::EDProducer 
{
 public:
  explicit CaloCleaner(const edm::ParameterSet&);
  ~CaloCleaner();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  typedef edm::SortedCollection<T> RecHitCollection;

  const edm::EDGetTokenT<edm::View<pat::Muon> > mu_input_;

  std::vector<edm::EDGetTokenT<RecHitCollection > > RecHitinputs_;
  std::vector< std::string> instances;
  
  TrackDetectorAssociator trackAssociator_;
  TrackAssociatorParameters parameters_;
  
  bool is_preshower_;
  void fill_correction_map(TrackDetMatchInfo *,  std::map<uint32_t, float> *);
  
};

template <typename T>
CaloCleaner<T>::CaloCleaner(const edm::ParameterSet& iConfig) :
    mu_input_(consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("MuonCollection")))
{ 
  std::vector<edm::InputTag> inCollections =  iConfig.getParameter<std::vector<edm::InputTag> >("oldCollections");
  for (auto inCollection : inCollections){
    RecHitinputs_.push_back(consumes<RecHitCollection >(inCollection));
    produces<RecHitCollection>(inCollection.instance()); 
    instances.push_back(inCollection.instance()); 
    
  }
   is_preshower_ =iConfig.getUntrackedParameter<bool>("is_preshower", false);
   edm::ParameterSet parameters = iConfig.getParameter<edm::ParameterSet>("TrackAssociatorParameters");
   edm::ConsumesCollector iC = consumesCollector();
   parameters_.loadParameters( parameters, iC );
   //trackAssociator_.useDefaultPropagator();
 
}

template <typename T>
CaloCleaner<T>::~CaloCleaner()
{
// nothing to be done yet...  
}


template <typename T>
void CaloCleaner<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::ESHandle<Propagator> propagator;
  iSetup.get<TrackingComponentsRecord>().get("SteppingHelixPropagatorAny", propagator);
  trackAssociator_.setPropagator(propagator.product());
  
  edm::Handle< edm::View<pat::Muon> > muonHandle;
  iEvent.getByToken(mu_input_, muonHandle);
  edm::View<pat::Muon> muons = *muonHandle;
  
  std::map<uint32_t, float>    correction_map;

  // Fill the correction map
  for (edm::View<pat::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {
    // get the basic informaiton like fill reco mouon does 
    //     RecoMuon/MuonIdentification/plugins/MuonIdProducer.cc
    const reco::Track* track = 0;
    if      ( iMuon->track().isNonnull() ) track = iMuon->track().get();
    else if ( iMuon->standAloneMuon().isNonnull() ) track = iMuon->standAloneMuon().get();
    else throw cms::Exception("FatalError") << "Failed to fill muon id information for a muon with undefined references to tracks";
    TrackDetMatchInfo info = trackAssociator_.associate(iEvent, iSetup, *track, parameters_,TrackDetectorAssociator::Any);
    fill_correction_map(&info,&correction_map);
  }
  
  // Copy the old collection
  unsigned id = 0;
  for (auto RecHitinput_ : RecHitinputs_){
    std::auto_ptr<RecHitCollection> recHitCollection_output(new RecHitCollection());   
    edm::Handle<RecHitCollection> recHitCollection;
    iEvent.getByToken(RecHitinput_, recHitCollection);    
    for ( typename RecHitCollection::const_iterator recHit = recHitCollection->begin(); recHit != recHitCollection->end(); ++recHit ) {
      if (correction_map[recHit->detid().rawId()] > 0){
	float new_energy =  recHit->energy() - correction_map[recHit->detid().rawId()];
	if (new_energy < 0) new_energy =0;
	T newRecHit (*recHit);
	newRecHit.setEnergy(new_energy);
	//if (new_energy>0) std::cout<< new_energy <<std::endl; to be tested 
	recHitCollection_output->push_back(newRecHit);
      }
      else{
	recHitCollection_output->push_back(*recHit);
      }  
    }
    // Save the new collection
    iEvent.put(recHitCollection_output,instances[id]);
    id++;   
  }

}
