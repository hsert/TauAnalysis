import FWCore.ParameterSet.Config as cms

MuonImput = cms.InputTag("selectedMuonsForEmbedding","","SKIM")


cleanedsiPixelClusters = cms.EDProducer('PixelCleaner',
    MuonCollection = MuonImput,
    oldCollection = cms.InputTag("siPixelClusters","","SKIM")
)

cleanedsiStripClusters = cms.EDProducer('StripCleaner',
    MuonCollection = MuonImput,
    oldCollection = cms.InputTag("siStripClusters","","SKIM"),
)

from TrackingTools.TrackAssociator.default_cfi import TrackAssociatorParameterBlock

TrackAssociatorParameterBlock.TrackAssociatorParameters.EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB","SKIM")
TrackAssociatorParameterBlock.TrackAssociatorParameters.EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE","SKIM")
##TrackAssociatorParameterBlock.TrackAssociatorParameters.ESRecHitCollectionLabel = cms.InputTag("ecalPreshowerRecHit","EcalRecHitsES","SKIM")
TrackAssociatorParameterBlock.TrackAssociatorParameters.HBHERecHitCollectionLabel = cms.InputTag("hbhereco","","SKIM")
TrackAssociatorParameterBlock.TrackAssociatorParameters.HORecHitCollectionLabel = cms.InputTag("horeco","","SKIM")


cleanedecalRecHit = cms.EDProducer("EcalRecHitCleaner",
    MuonCollection = MuonImput,
    TrackAssociatorParameters = TrackAssociatorParameterBlock.TrackAssociatorParameters,
    oldCollections = cms.VInputTag(cms.InputTag("ecalRecHit","EcalRecHitsEB","SKIM"),
    cms.InputTag("ecalRecHit","EcalRecHitsEE","SKIM"))
)

cleanedecalPreShowerRecHit = cms.EDProducer("EcalRecHitCleaner",
    MuonCollection = MuonImput,
    TrackAssociatorParameters = TrackAssociatorParameterBlock.TrackAssociatorParameters,
    oldCollections = cms.VInputTag(cms.InputTag("ecalPreshowerRecHit","EcalRecHitsES","SKIM"))
)
##ecalPreShowerRecHit.TrackAssociatorParameters.usePreshower = cms.bool(True) 

cleanedhbhereco = cms.EDProducer("HBHERecHitCleaner",
    MuonCollection = MuonImput,
    TrackAssociatorParameters = TrackAssociatorParameterBlock.TrackAssociatorParameters,
    oldCollections = cms.VInputTag(cms.InputTag("hbhereco","","SKIM"))
)

cleanedhoreco = cms.EDProducer("HORecHitCleaner",
    MuonCollection = MuonImput,
    TrackAssociatorParameters = TrackAssociatorParameterBlock.TrackAssociatorParameters,
    oldCollections = cms.VInputTag(cms.InputTag("horeco","","SKIM"))
)

cleaneddt1DRecHits = cms.EDProducer('DTCleaner',
    MuonCollection = MuonImput,
    oldCollection = cms.InputTag("dt1DRecHits","","SKIM"),
)

cleanedcsc2DRecHits = cms.EDProducer('CSCCleaner',
    MuonCollection = MuonImput,
    oldCollection  = cms.InputTag("csc2DRecHits","","SKIM"),
)

cleanedrpcRecHits = cms.EDProducer('RPCleaner',
    MuonCollection = MuonImput,
    oldCollection  = cms.InputTag("rpcRecHits","","SKIM"),
)

#externalLHEProducer = cms.EDProducer("EmbeddingLHEProducer",
#    src = MuonImput,
#    switchToMuonEmbedding = cms.bool(True),
#    mirroring = cms.bool(False),
#    studyFSRmode = cms.untracked.string("reco")
#)

makeCleaningProcedure = cms.Sequence(
    cleanedsiPixelClusters
    + cleanedsiStripClusters
    + cleanedecalRecHit
    + cleanedecalPreShowerRecHit
    + cleanedhbhereco
    + cleanedhoreco
    + cleaneddt1DRecHits
    + cleanedcsc2DRecHits
    + cleanedrpcRecHits
#    + externalLHEProducer
)
