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
#include "TrackingTools/PatternTools/interface/TrajTrackAssociation.h"
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
  
//  typedef T1 TrackCollectionemb;
  typedef std::vector<T1> TrackCollectionemb;
  
  typedef reco::TrackRef::key_type TrackRefKey;
  
  void willproduce(std::string instance, std::string alias);
  void merg_and_put(edm::Event&, std::string ,  std::vector<edm::EDGetTokenT<TrackCollectionemb> > & );
  bool copyTrajectories_;
  

  std::map<std::string,  std::vector<edm::EDGetTokenT<TrackCollectionemb > > > inputs_;
  std::map<std::string,  std::vector<edm::EDGetTokenT<std::vector<Trajectory> > > > inputs_tr_;
  std::map<std::string,  std::vector<edm::EDGetTokenT<TrajTrackAssociationCollection > > > inputs_ta_;

};

template <typename T1>
TrackMergeremb<T1>::TrackMergeremb(const edm::ParameterSet& iConfig):
   copyTrajectories_(iConfig.template getUntrackedParameter<bool>("copyTrajectories", false))
{
  std::string alias( iConfig.getParameter<std::string>( "@module_label" ) );
  std::vector<edm::InputTag> inCollections =  iConfig.getParameter<std::vector<edm::InputTag> >("mergCollections");
  for (auto inCollection : inCollections){
     inputs_[inCollection.instance()].push_back(consumes<TrackCollectionemb >(inCollection) );
     inputs_tr_[inCollection.instance()].push_back(mayConsume<std::vector<Trajectory> >(inCollection) );
     inputs_ta_[inCollection.instance()].push_back(mayConsume<TrajTrackAssociationCollection >(inCollection) );     
  }
  for (auto toproduce : inputs_){
     
    produces<reco::TrackCollection>(toproduce.first).setBranchAlias( alias + "Tracks" );
    produces<reco::TrackExtraCollection>(toproduce.first).setBranchAlias( alias + "TrackExtras" );
    produces<TrackingRecHitCollection>(toproduce.first).setBranchAlias( alias + "RecHits" );
    if (copyTrajectories_){
      produces< std::vector<Trajectory> >(toproduce.first).setBranchAlias( alias + "Trajectories" );
      produces< TrajTrackAssociationCollection >(toproduce.first).setBranchAlias( alias + "TrajectoryTrackAssociations" );
    }      
  }

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
      
     // merg_and_put(iEvent, input_.first, input_.second);
    
      std::unique_ptr<TrackCollectionemb> outTracks = std::unique_ptr<TrackCollectionemb>(new TrackCollectionemb);
      std::unique_ptr<reco::TrackExtraCollection> outTracks_ex = std::unique_ptr<reco::TrackExtraCollection>(new reco::TrackExtraCollection());
      std::unique_ptr<TrackingRecHitCollection> outTracks_rh = std::unique_ptr<TrackingRecHitCollection>(new TrackingRecHitCollection());
      
      auto rTracks = iEvent.getRefBeforePut<reco::TrackCollection>();
      auto rTrackExtras = iEvent.getRefBeforePut<reco::TrackExtraCollection>();
      
      
      std::unique_ptr< std::vector<Trajectory> > outTrack_tr;
      std::unique_ptr< TrajTrackAssociationCollection > outTrack_ta;
       edm::RefProd< std::vector<Trajectory> > rTraj;
      
     if (copyTrajectories_){
        outTrack_tr = std::unique_ptr< std::vector<Trajectory> >(new std::vector<Trajectory>());
        outTrack_ta = std::unique_ptr< TrajTrackAssociationCollection >(new TrajTrackAssociationCollection());
	rTraj = iEvent.getRefBeforePut< std::vector<Trajectory> >();
	
     }

      std::map<TrackRefKey, reco::TrackRef > goodTracks;
      TrackRefKey current = 0;
      auto rHits = iEvent.getRefBeforePut<TrackingRecHitCollection>();
      
      
      unsigned ncol=0;
      for (auto akt_collection : input_.second){
          edm::Handle<TrackCollectionemb> track_col_in;  
          iEvent.getByToken(akt_collection, track_col_in);
	
	  for (typename TrackCollectionemb::const_iterator it = track_col_in->begin(); it != track_col_in->end(); ++it, ++current) {
	    outTracks->push_back( T1( *it ) );
	    outTracks_ex->push_back( reco::TrackExtra( *it->extra() ) );
	    outTracks->back().setExtra( reco::TrackExtraRef( rTrackExtras, outTracks_ex->size() - 1) );
	    
	    goodTracks[current] = reco::TrackRef(rTracks, outTracks->size() - 1);
	  }
    	  
   	  if (copyTrajectories_){
    	  
	    edm::Handle< std::vector<Trajectory> > track_col_tr_in;
            edm::Handle< TrajTrackAssociationCollection > track_col_ta_in;
            iEvent.getByToken(inputs_tr_[input_.first][ncol],  track_col_tr_in);
	    iEvent.getByToken(inputs_ta_[input_.first][ncol],  track_col_ta_in);
  
	    for (size_t i = 0; i < track_col_tr_in->size(); ++i) {
	       edm::Ref< std::vector<Trajectory> > trajRef(track_col_tr_in, i);
               TrajTrackAssociationCollection::const_iterator match = track_col_ta_in->find(trajRef);
               if (match != track_col_ta_in->end()) {
                   const edm::Ref<reco::TrackCollection> &trkRef = match->val;
                   TrackRefKey oldKey = trkRef.key();
                   std::map<TrackRefKey, reco::TrackRef>::iterator getref = goodTracks.find(oldKey);
                   if (getref != goodTracks.end()) {
                      // do the clone
                       outTrack_tr->push_back( Trajectory(*trajRef) );
                       outTrack_ta->insert ( edm::Ref< std::vector<Trajectory> >(rTraj, outTrack_tr->size() - 1),getref->second );	    
		   } 
	         }
	     }
	  }
	  ncol++;        
      }// end merge 
    
    
      iEvent.put(std::move(outTracks),input_.first);
      iEvent.put(std::move(outTracks_ex),input_.first);
      iEvent.put(std::move(outTracks_rh),input_.first);
      if (copyTrajectories_){
       iEvent.put(std::move(outTrack_tr),input_.first);
       iEvent.put(std::move(outTrack_ta),input_.first);
      }

  }// end instance
  
    

  
}
