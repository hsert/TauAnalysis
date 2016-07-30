#include "TauAnalysis/EmbeddingProducer/plugins/TrackMergeremb.h"





typedef TrackMergeremb<reco::Track> generalTracksMerger;
//typedef TrackMergeremb<reco::GsfTrack> electronGsfTracksMerger;


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

}

template <>
void  TrackMergeremb<reco::TrackCollection>::merg_and_put(edm::Event& iEvent, std::string instance,  std::vector<edm::EDGetTokenT<TrackCollectionemb> > &to_merge )
{
    
    



    
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




//template <>
//void  TrackMergeremb<reco::GsfTrackCollection>::willproduce(std::string instance, std::string alias)
//{
   // produces<reco::TrackCollection>(instance).setBranchAlias( alias + "Tracks" );
  //  produces<reco::TrackExtraCollection>(instance).setBranchAlias( alias + "TrackExtras" );
  //  produces<TrackingRecHitCollection>(instance).setBranchAlias( alias + "RecHits" );
  //  produces< std::vector<Trajectory> >(instance).setBranchAlias( alias + "Trajectories" );
  //  produces< TrajTrackAssociationCollection >(instance).setBranchAlias( alias + "TrajectoryTrackAssociations" );
//}

//template <>
//void  TrackMergeremb<reco::GsfTrackCollection>::merg_and_put(edm::Event& iEvent, std::string instance,  std::vector<edm::EDGetTokenT<TrackCollectionemb> > &to_merge )
//{
    
//}



#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(generalTracksMerger);
//DEFINE_FWK_MODULE(electronGsfTracksMerger);
