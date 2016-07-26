/** \class TrackMergeremb
 *
 * 
 * \author Stefan Wayand;
 *         Christian Veelken, LLR
 *
 * \version $Revision: 1.9 $
 *
 * $Id: TrackMergeremb.h,v 1.9 2013/03/23 09:12:51 veelken Exp $
 *
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"


#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackExtra.h"

#include "DataFormats/GsfTrackReco/interface/GsfTrackExtraFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"

#include "TrackingTools/PatternTools/interface/Trajectory.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "Geometry/Records/interface/TrackerTopologyRcd.h"

#include <string>
#include <iostream>
#include <map>



template <typename T1>
class TrackMergeremb : public edm::EDProducer 
{
 public:
  explicit TrackMergeremb(const edm::ParameterSet&);
  ~TrackMergeremb();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  
  typedef T1 TrackCollectionemb;
  
  void willproduce(std::string instance, std::string alias);
  void merg_and_put(edm::Event&, std::string ,  std::vector<edm::EDGetTokenT<TrackCollectionemb> > & );
  
  

  std::map<std::string,  std::vector<edm::EDGetTokenT<TrackCollectionemb > > > inputs_;
  

};

template <typename T1>
TrackMergeremb<T1>::TrackMergeremb(const edm::ParameterSet& iConfig)
{
  std::string alias( iConfig.getParameter<std::string>( "@module_label" ) );
  std::vector<edm::InputTag> inCollections =  iConfig.getParameter<std::vector<edm::InputTag> >("mergCollections");
  for (auto inCollection : inCollections){
     inputs_[inCollection.instance()].push_back(consumes<TrackCollectionemb >(inCollection) );
  }
  for (auto toproduce : inputs_){
     
      willproduce(toproduce.first,alias);

      
     
     
  }
 // produces<reco::GsfTrackExtraCollection>().setBranchAlias( alias_ + "GsfTrackExtras" );

 // produces<TrajGsfTrackAssociationCollection>();
 
 
}

template <typename T1>
TrackMergeremb<T1>::~TrackMergeremb()
{
// nothing to be done yet...  
}


template <typename T1>
void TrackMergeremb<T1>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   
  for (auto input_ : inputs_){
      
      merg_and_put(iEvent, input_.first, input_.second);
    //std::auto_ptr<TrackCollectionemb > output(new TrackCollectionemb());
    //std::auto_ptr<reco::TrackExtraCollection > output_ex(new reco::TrackExtraCollection());
    //std::auto_ptr<TrackingRecHitCollection > output_rh(new TrackingRecHitCollection());
    //std::auto_ptr<std::vector<Trajectory> > output_tr(new std::vector<Trajectory>());
    
    
    
   // std::vector<edm::Handle<MergeCollection> > inputCollections;
   // inputCollections.resize(input_.second.size());
   // for (unsigned id = 0; id<input_.second.size(); id++){
    //  iEvent.getByToken(input_.second[id], inputCollections[id]);
    // }
   // fill_output_obj(output,inputCollections);   
    //iEvent.put(output,input_.first);
    //iEvent.put(output_ex,input_.first);
    //iEvent.put(output_rh,input_.first);
    //iEvent.put(output_tr,input_.first);
  
  }
  
    

  
}
