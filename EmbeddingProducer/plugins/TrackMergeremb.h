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
#include "DataFormats/TrajectorySeed/interface/TrajectorySeedCollection.h"
#include "TrackingTools/GsfTracking/interface/TrajGsfTrackAssociation.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"




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
  bool saveTrajectories_;
  

  std::map<std::string,  std::vector<edm::EDGetTokenT<TrackCollectionemb > > > inputs_;
  std::map<std::string,  std::vector<edm::EDGetTokenT<std::vector<Trajectory> > > > inputs_tr_;
  std::map<std::string,  std::vector<edm::EDGetTokenT<TrajGsfTrackAssociationCollection > > > inputs_ta_;

};

template <typename T1>
TrackMergeremb<T1>::TrackMergeremb(const edm::ParameterSet& iConfig):
   saveTrajectories_(iConfig.template getUntrackedParameter<bool>("saveTrajectories", false))
{
  std::string alias( iConfig.getParameter<std::string>( "@module_label" ) );
  std::vector<edm::InputTag> inCollections =  iConfig.getParameter<std::vector<edm::InputTag> >("mergCollections");
  for (auto inCollection : inCollections){
     inputs_[inCollection.instance()].push_back(consumes<TrackCollectionemb >(inCollection) );
     if (saveTrajectories_){
       inputs_tr_[inCollection.instance()].push_back(mayConsume<std::vector<Trajectory> >(inCollection) );
     }
     else{
        inputs_ta_[inCollection.instance()].push_back(mayConsume<TrajGsfTrackAssociationCollection >(inCollection) );
     }
     //inputs_tr_[inCollection.instance()].push_back(mayConsume<std::vector<Trajectory> >(inCollection) );
  //   inputs_ta_[inCollection.instance()].push_back(mayConsume<TrajTrackAssociationCollection >(inCollection) );     
  }
  for (auto toproduce : inputs_){
     
    produces<reco::TrackCollection>(toproduce.first).setBranchAlias( alias + "Tracks" );
    produces<reco::TrackExtraCollection>(toproduce.first).setBranchAlias( alias + "TrackExtras" );
    produces<TrackingRecHitCollection>(toproduce.first).setBranchAlias( alias + "RecHits" );
    produces<reco::GsfTrackCollection>(toproduce.first).setBranchAlias( alias + "GsfTrack" );
    produces< std::vector<Trajectory> >(toproduce.first).setBranchAlias( alias + "Trajectories" );
    produces< TrajGsfTrackAssociationCollection >(toproduce.first).setBranchAlias( alias + "TrajectoryTrackAssociations" );
     
  //  }      
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
      
      std::unique_ptr<TrackCollectionemb> outTracks = std::unique_ptr<TrackCollectionemb>(new TrackCollectionemb);
      std::unique_ptr<reco::GsfTrackCollection> outTracks_gsf = std::unique_ptr<reco::GsfTrackCollection>(new reco::GsfTrackCollection);
      
      std::unique_ptr<reco::TrackExtraCollection> outTracks_ex = std::unique_ptr<reco::TrackExtraCollection>(new reco::TrackExtraCollection());
      std::unique_ptr<TrackingRecHitCollection> outTracks_rh = std::unique_ptr<TrackingRecHitCollection>(new TrackingRecHitCollection());
      
      auto rTracks = iEvent.getRefBeforePut<reco::TrackCollection>();
      auto rTrackExtras = iEvent.getRefBeforePut<reco::TrackExtraCollection>();
      
      std::unique_ptr< std::vector<Trajectory> > outTrack_tr =  std::unique_ptr< std::vector<Trajectory> >(new std::vector<Trajectory>());

      //TrackRefKey current = 0;
      auto rHits = iEvent.getRefBeforePut<TrackingRecHitCollection>();
      
      
      unsigned ncol=0;
      for (auto akt_collection : input_.second){
          edm::Handle<TrackCollectionemb> track_col_in;  
          iEvent.getByToken(akt_collection, track_col_in);
	  

          
          edm::Handle<std::vector<Trajectory> >   traj_input;        
	  if (saveTrajectories_)  iEvent.getByToken(inputs_tr_[input_.first][ncol],  traj_input);
          
          
          // edm::Handle< edm::View<TrajectorySeedCollection> > track_col_trseed_in;
	 //  edm::Handle< edm::View<TrajectorySeed> > track_col_trseed_in;
	  
	  size_t sedref_it = 0;
	  for (typename TrackCollectionemb::const_iterator it = track_col_in->begin(); it != track_col_in->end(); ++it, ++sedref_it) {
	    outTracks->push_back( T1( *it ) );
            
            //outTracks_gsf->push_back( dynamic_cast<const reco::GsfTrack>( &*it) );
            outTracks_gsf->push_back( reco::GsfTrack() );
            if (saveTrajectories_) outTrack_tr->push_back( (*traj_input)[sedref_it]);
            
	    outTracks_ex->push_back( reco::TrackExtra( *it->extra() ) );
	    outTracks->back().setExtra( reco::TrackExtraRef( rTrackExtras, outTracks_ex->size() - 1) );	    	    
	  }
	    
	   
	  ncol++;        
      }// end merge 
    
      auto rTracks_ = iEvent.put(std::move(outTracks),input_.first);
      auto rTracks_gsf_ = iEvent.put(std::move(outTracks_gsf),input_.first);
      
     // iEvent.put(std::move(outTracks),input_.first);
      iEvent.put(std::move(outTracks_ex),input_.first);
      iEvent.put(std::move(outTracks_rh),input_.first);
      if (saveTrajectories_){
	
      edm::OrphanHandle<std::vector<Trajectory> > rTrajs =  iEvent.put(std::move(outTrack_tr),input_.first);
       std::unique_ptr< TrajGsfTrackAssociationCollection > outTrack_ta =  std::unique_ptr< TrajGsfTrackAssociationCollection >(new TrajGsfTrackAssociationCollection(rTrajs, rTracks_gsf_));
      
       for ( unsigned index = 0; index<rTrajs->size(); ++index ) { 
	        //std::cout<<"bbbb"<<std::endl;
	      edm::Ref<std::vector<reco::GsfTrack> >    tkRef(rTracks_gsf_, index);
	      edm::Ref<std::vector<Trajectory> > trajRef( rTrajs, index );
	      
	              //std::cout<<"jjjjj"<<std::endl;
	      outTrack_ta->insert(trajRef,tkRef);
       }
      
       iEvent.put(std::move(outTrack_ta),input_.first);
      
      }

  }// end instance
  
    
  
  
}
