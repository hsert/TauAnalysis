#include "TauAnalysis/EmbeddingProducer/plugins/TrackMergeremb.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/GsfTrackReco/interface/GsfTrackExtraFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "TrackingTools/PatternTools/interface/Trajectory.h"
#include "TrackingTools/PatternTools/interface/TrajTrackAssociation.h"



typedef TrackMergeremb<reco::TrackCollection> generalTracksMerger;
typedef TrackMergeremb<reco::GsfTrackCollection> electronGsfTracksMerger;


// Here some overloaded functions, which are needed such that the right merger function is called for the indivudal Collections
template <typename T1>
void  TrackMergeremb<T1>::willproduce(std::string instance, std::string alias)
{
  assert(0); // CV: make sure general function never gets called;
             //     always use template specializations
}

template <typename T1>
void  TrackMergeremb<T1>::merg_and_put(edm::Event&, std::string instance,  std::vector<edm::EDGetTokenT<TrackCollectionemb> > &to_merge)
{
  assert(0); // CV: make sure general function never gets called;
             //     always use template specializations
}

template <>
void  TrackMergeremb<reco::TrackCollection>::willproduce(std::string instance, std::string alias)
{
    produces<reco::TrackCollection>(instance).setBranchAlias( alias + "Tracks" );
    produces<reco::TrackExtraCollection>(instance).setBranchAlias( alias + "TrackExtras" );
    produces<TrackingRecHitCollection>(instance).setBranchAlias( alias + "RecHits" );
    produces< std::vector<Trajectory> >(instance).setBranchAlias( alias + "Trajectories" );
    produces< TrajTrackAssociationCollection >(instance).setBranchAlias( alias + "TrajectoryTrackAssociations" );
}

template <>
void  TrackMergeremb<reco::TrackCollection>::merg_and_put(edm::Event& iEvent, std::string instance,  std::vector<edm::EDGetTokenT<TrackCollectionemb> > &to_merge )
{
    
    
  std::unique_ptr<reco::TrackCollection> outTracks = std::unique_ptr<reco::TrackCollection>(new reco::TrackCollection());
  std::unique_ptr<reco::TrackExtraCollection> outTracks_ex = std::unique_ptr<reco::TrackExtraCollection>(new reco::TrackExtraCollection());
  std::unique_ptr<TrackingRecHitCollection> outTracks_rh = std::unique_ptr<TrackingRecHitCollection>(new TrackingRecHitCollection());
  std::unique_ptr< std::vector<Trajectory> > outTrack_tr = std::unique_ptr< std::vector<Trajectory> >(new std::vector<Trajectory>());
  std::unique_ptr< TrajTrackAssociationCollection > outTrack_ta = std::unique_ptr< TrajTrackAssociationCollection >(new TrajTrackAssociationCollection());
    
    for (auto akt_collection : to_merge){
        edm::Handle<reco::TrackCollection> track_col_in;  
        iEvent.getByToken(akt_collection, track_col_in);
        
        edm::Handle< std::vector<Trajectory> > hTraj;
        edm::Handle< TrajTrackAssociationCollection > hTTAss;
          evt.getByToken(hTTAssToken_, hTTAss);
evt.getByToken(hTrajToken_, hTraj);
        
        
        
    }
    
    
    iEvent.put(std::move(outTracks));
    iEvent.put(std::move(outTracks_ex));
    iEvent.put(std::move(outTracks_rh));
    iEvent.put(std::move(outTrack_tr));
    iEvent.put(std::move(outTrack_ta));


    
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




template <>
void  TrackMergeremb<reco::GsfTrackCollection>::willproduce(std::string instance, std::string alias)
{
    produces<reco::TrackCollection>(instance).setBranchAlias( alias + "Tracks" );
    produces<reco::TrackExtraCollection>(instance).setBranchAlias( alias + "TrackExtras" );
    produces<TrackingRecHitCollection>(instance).setBranchAlias( alias + "RecHits" );
    produces< std::vector<Trajectory> >(instance).setBranchAlias( alias + "Trajectories" );
    produces< TrajTrackAssociationCollection >(instance).setBranchAlias( alias + "TrajectoryTrackAssociations" );
}

template <>
void  TrackMergeremb<reco::GsfTrackCollection>::merg_and_put(edm::Event& iEvent, std::string instance,  std::vector<edm::EDGetTokenT<TrackCollectionemb> > &to_merge )
{
    
}



#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(generalTracksMerger);
DEFINE_FWK_MODULE(electronGsfTracksMerger);
