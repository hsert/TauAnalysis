#include "TauAnalysis/EmbeddingProducer/plugins/CollectionMerger.h"
#include "FWCore/Framework/interface/MakerMacros.h"


#include "DataFormats/SiPixelCluster/interface/SiPixelCluster.h"
#include "DataFormats/SiStripCluster/interface/SiStripCluster.h"

#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/Common/interface/SortedCollection.h"


#include "DataFormats/MuonDetId/interface/DTLayerId.h"
#include "DataFormats/DTRecHit/interface/DTSLRecCluster.h"
#include "DataFormats/DTRecHit/interface/DTRecHit1DPair.h"

#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "DataFormats/CSCRecHit/interface/CSCRecHit2D.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"
#include "DataFormats/RPCRecHit/interface/RPCRecHit.h"

#include "DataFormats/Common/interface/RangeMap.h"
#include "DataFormats/Common/interface/OwnVector.h"



typedef CollectionMerger<edmNew::DetSetVector<SiPixelCluster>, SiPixelCluster> PixelMerger;
typedef CollectionMerger<edmNew::DetSetVector<SiStripCluster>, SiStripCluster> StripMerger;

typedef CollectionMerger<edm::SortedCollection<EcalRecHit>, EcalRecHit> EcalRecHitMerger;
typedef CollectionMerger<edm::SortedCollection<HBHERecHit>, HBHERecHit> HBHERecHitMerger;
typedef CollectionMerger<edm::SortedCollection<HFRecHit>, HFRecHit> HFRecHitMerger;
typedef CollectionMerger<edm::SortedCollection<HORecHit>, HORecHit> HORecHitMerger;
typedef CollectionMerger<edm::SortedCollection<CastorRecHit>, CastorRecHit> CastorRecHitMerger;




typedef CollectionMerger<edm::RangeMap<DTLayerId, edm::OwnVector<DTRecHit1DPair> >, DTRecHit1DPair> DTRecHitMerger;
typedef CollectionMerger<edm::RangeMap<CSCDetId, edm::OwnVector<CSCRecHit2D> >, CSCRecHit2D> CSCRecHitMerger;
typedef CollectionMerger<edm::RangeMap<RPCDetId, edm::OwnVector<RPCRecHit> >, RPCRecHit> RPCRecHitMerger;



// -------- Here Tracker Merger -----------
template <typename T1, typename T2>
void  CollectionMerger<T1,T2>::fill_output_obj_tracker(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  std::map<uint32_t, std::vector<BaseHit> >   output_map;
  // First merge the collections with the help of the output map
  for (auto inputCollection : inputCollections){
   for ( typename MergeCollection::const_iterator clustSet = inputCollection->begin(); clustSet!= inputCollection->end(); ++clustSet ) {
      DetId detIdObject( clustSet->detId() );
      for (typename edmNew::DetSet<BaseHit>::const_iterator clustIt = clustSet->begin(); clustIt != clustSet->end(); ++clustIt ) { 	
        output_map[detIdObject.rawId()].push_back(*clustIt);	
       }
    } 
  }
  // Now save it into the standard CMSSW format, with the standard Filler
  for (typename std::map<uint32_t, std::vector<BaseHit> >::const_iterator outHits = output_map.begin(); outHits != output_map.end(); ++outHits ) {
     DetId detIdObject(outHits->first);
     typename MergeCollection::FastFiller spc(*output, detIdObject);
     for (auto Hit : outHits->second){ 
       spc.push_back(Hit);
     }     
   }  
}




template <typename T1, typename T2>
void  CollectionMerger<T1,T2>::fill_output_obj_calo(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
 std::map<uint32_t, BaseHit >   output_map;  
 // First merge the two collections again
 for (auto inputCollection : inputCollections){
  for ( typename MergeCollection::const_iterator recHit = inputCollection->begin(); recHit!= inputCollection->end(); ++recHit ) {
    if (recHit->energy() <= 0) continue;
    DetId detIdObject( recHit->detid().rawId() );
    T2 *akt_calo_obj = &output_map[detIdObject.rawId()];
    float new_energy = akt_calo_obj->energy() + recHit->energy();
    T2 newRecHit(*recHit);
    newRecHit.setEnergy(new_energy);
    *akt_calo_obj = newRecHit;
  } 
  // Now save it into the standard CMSSW format
    for (typename std::map<uint32_t, BaseHit >::const_iterator outHits = output_map.begin(); outHits != output_map.end(); ++outHits ) {
      output->push_back(outHits->second);
    }   
  }
  output->sort(); //Do a sort for this collection
}



// -------- Here Muon Chamber Merger -----------
template <typename T1, typename T2>
void  CollectionMerger<T1,T2>::fill_output_obj_muonchamber(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  std::map<uint32_t, std::vector<BaseHit> >   output_map;
  // First merge the collections with the help of the output map
  for (auto inputCollection : inputCollections){
   for ( typename MergeCollection::const_iterator recHit = inputCollection->begin(); recHit!= inputCollection->end(); ++recHit ) {
      DetId detIdObject( recHit->geographicalId() );	
      output_map[detIdObject].push_back(*recHit);	
      }
  } 
  // Now save it into the standard CMSSW format, with the standard Filler
  for (typename std::map<uint32_t, std::vector<BaseHit> >::const_iterator outHits = output_map.begin(); outHits != output_map.end(); ++outHits ) {
        output->put((typename T1::id_iterator::value_type) outHits->first , outHits->second.begin(), outHits->second.end()); // The DTLayerId misses the automatic type cast 
   }  
}




// Here some overloaded functions, which are needed such that the right merger function is called for the indivudal Collections
template <typename T1, typename T2>
void  CollectionMerger<T1,T2>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  assert(0); // CV: make sure general function never gets called;
             //     always use template specializations
}

// Start with the Tracker collections
template <>
void  CollectionMerger<edmNew::DetSetVector<SiPixelCluster>, SiPixelCluster>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_tracker(output,inputCollections);
}


template <>
void  CollectionMerger<edmNew::DetSetVector<SiStripCluster>, SiStripCluster>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_tracker(output,inputCollections);
}


// Next are the Calo entries
template <>
void  CollectionMerger<edm::SortedCollection<EcalRecHit>,  EcalRecHit>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_calo(output,inputCollections);
}


template <>
void  CollectionMerger<edm::SortedCollection<HBHERecHit>, HBHERecHit>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_calo(output,inputCollections);
}

template <>
void  CollectionMerger<edm::SortedCollection<HFRecHit>, HFRecHit>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_calo(output,inputCollections);
}

template <>
void  CollectionMerger<edm::SortedCollection<HORecHit>, HORecHit>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_calo(output,inputCollections);
}

template <>
void  CollectionMerger<edm::SortedCollection<CastorRecHit>, CastorRecHit>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_calo(output,inputCollections);
}



// Here the Muon Chamber
template <>
void  CollectionMerger<edm::RangeMap<DTLayerId, edm::OwnVector<DTRecHit1DPair> >, DTRecHit1DPair >::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_muonchamber(output,inputCollections);
}

template <>
void  CollectionMerger<edm::RangeMap<CSCDetId, edm::OwnVector<CSCRecHit2D> >, CSCRecHit2D >::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_muonchamber(output,inputCollections);
}


template <>
void  CollectionMerger<edm::RangeMap<RPCDetId, edm::OwnVector<RPCRecHit> >, RPCRecHit>::fill_output_obj(std::auto_ptr<MergeCollection > & output, std::vector<edm::Handle<MergeCollection> > &inputCollections)
{
  fill_output_obj_muonchamber(output,inputCollections);
}




#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(PixelMerger);
DEFINE_FWK_MODULE(StripMerger);

DEFINE_FWK_MODULE(EcalRecHitMerger);
DEFINE_FWK_MODULE(HBHERecHitMerger);
DEFINE_FWK_MODULE(HFRecHitMerger);
DEFINE_FWK_MODULE(HORecHitMerger);
DEFINE_FWK_MODULE(CastorRecHitMerger);


DEFINE_FWK_MODULE(DTRecHitMerger);
DEFINE_FWK_MODULE(CSCRecHitMerger);
DEFINE_FWK_MODULE(RPCRecHitMerger);
