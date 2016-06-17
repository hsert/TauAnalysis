#include "TauAnalysis/EmbeddingProducer/plugins/CaloCleaner.h"

#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/HcalRecHit/interface/HBHERecHit.h"
#include "DataFormats/HcalRecHit/interface/HFRecHit.h"
#include "DataFormats/HcalRecHit/interface/HORecHit.h"
#include "DataFormats/HcalRecHit/interface/ZDCRecHit.h"
#include "DataFormats/HcalRecHit/interface/CastorRecHit.h"

typedef CaloCleaner<EcalRecHit> EcalRecHitMixer;
typedef CaloCleaner<HBHERecHit> HBHERecHitMixer;
typedef CaloCleaner<HFRecHit> HFRecHitMixer;
typedef CaloCleaner<HORecHit> HORecHitMixer;
//typedef CaloCleaner<ZDCRecHit> ZDCRecHitMixer;
typedef CaloCleaner<CastorRecHit> CastorRecHitMixer;

//-------------------------------------------------------------------------------
// define 'buildRecHit' functions used for different types of recHits
//-------------------------------------------------------------------------------


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(EcalRecHitMixer);
DEFINE_FWK_MODULE(HBHERecHitMixer);
DEFINE_FWK_MODULE(HFRecHitMixer);
DEFINE_FWK_MODULE(HORecHitMixer);
//DEFINE_FWK_MODULE(ZDCRecHitMixer);
DEFINE_FWK_MODULE(CastorRecHitMixer);

 //   ecalInputs = cms.VInputTag(cms.InputTag("ecalRecHit","EcalRecHitsEB"), cms.InputTag("ecalRecHit","EcalRecHitsEE")),
 //   hbheInput = cms.InputTag("hbheprereco"),
 //   hfInput = cms.InputTag("hfreco"),
 //   hoInput = cms.InputTag("horeco")
// process.castorreco
