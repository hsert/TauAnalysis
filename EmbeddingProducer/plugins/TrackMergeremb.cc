#include "TauAnalysis/EmbeddingProducer/plugins/TrackMergeremb.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"


typedef TrackMergeremb<reco::TrackCollection> generalTracksMerger;



// Here some overloaded functions, which are needed such that the right merger function is called for the indivudal Collections
//template <typename T1, typename T2>
//void  TrackMergeremb<T1,T2>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
//{
 // assert(0); // CV: make sure general function never gets called;
             //     always use template specializations
//}





#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(generalTracksMerger);

