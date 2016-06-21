#include "TauAnalysis/EmbeddingProducer/plugins/CaloCleaner.h"

#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/HcalRecHit/interface/HBHERecHit.h"
#include "DataFormats/HcalRecHit/interface/HFRecHit.h"
#include "DataFormats/HcalRecHit/interface/HORecHit.h"
#include "DataFormats/HcalRecHit/interface/ZDCRecHit.h"
#include "DataFormats/HcalRecHit/interface/CastorRecHit.h"

typedef CaloCleaner<EcalRecHit> EcalRecHitCleaner;
typedef CaloCleaner<HBHERecHit> HBHERecHitCleaner;
typedef CaloCleaner<HFRecHit> HFRecHitCleaner;
typedef CaloCleaner<HORecHit> HORecHitCleaner;
//typedef CaloCleaner<ZDCRecHit> ZDCRecHitCleaner;
typedef CaloCleaner<CastorRecHit> CastorRecHitCleaner;

//-------------------------------------------------------------------------------
// define 'buildRecHit' functions used for different types of recHits
//-------------------------------------------------------------------------------
  


template <typename T>
void  CaloCleaner<T>::fill_correction_map(TrackDetMatchInfo *,  std::map<uint32_t, float> *)
{
  assert(0); // CV: make sure general function never gets called;
             //     always use template specializations
}

template <>
void  CaloCleaner<EcalRecHit>::fill_correction_map(TrackDetMatchInfo * info,  std::map<uint32_t, float> * cor_map)
{
  if (is_preshower_){
     for ( std::vector<DetId>::const_iterator detId = info->crossedPreshowerIds.begin(); detId != info->crossedPreshowerIds.end(); ++detId ) {
       (*cor_map) [detId->rawId()] = 9999999; // just remove all energy (Below 0 is not possible)  
      }
    } 
  else {
    for(std::vector<const EcalRecHit*>::const_iterator hit=info->crossedEcalRecHits.begin(); hit!=info->crossedEcalRecHits.end(); hit++){
      //    (*cor_map) [(*hit)->detid().rawId()] +=(*hit)->energy();
      (*cor_map) [(*hit)->detid().rawId()] =(*hit)->energy(); // should be more correct ;)
    }
  }
}


template <>
void  CaloCleaner<HBHERecHit>::fill_correction_map(TrackDetMatchInfo * info,  std::map<uint32_t, float> * cor_map)
{
  for(std::vector<const HBHERecHit*>::const_iterator hit = info->crossedHcalRecHits.begin(); hit != info->crossedHcalRecHits.end(); hit++) {
    (*cor_map) [(*hit)->detid().rawId()] =(*hit)->energy(); // should be more correct ;)
  }
}


template <>
void  CaloCleaner<HORecHit>::fill_correction_map(TrackDetMatchInfo * info,  std::map<uint32_t, float> * cor_map)
{
  for(std::vector<const HORecHit*>::const_iterator hit = info->crossedHORecHits.begin(); hit != info->crossedHORecHits.end(); hit++) {
    (*cor_map) [(*hit)->detid().rawId()] =(*hit)->energy(); // should be more correct ;)
  }
}






#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(EcalRecHitCleaner);
DEFINE_FWK_MODULE(HBHERecHitCleaner);
DEFINE_FWK_MODULE(HORecHitCleaner);
// no  need for cleaning outside of tracker
//DEFINE_FWK_MODULE(HFRecHitCleaner);
//DEFINE_FWK_MODULE(CastorRecHitCleaner);
////DEFINE_FWK_MODULE(ZDCRecHitCleaner);

