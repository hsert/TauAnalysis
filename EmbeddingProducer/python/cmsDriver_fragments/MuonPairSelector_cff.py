import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi import patMuons
patMuonsForembedding = patMuons.clone()
patMuonsForembedding.addGenMatch = cms.bool(False)
patMuonsForembedding.embedCaloMETMuonCorrs = cms.bool(False)
patMuonsForembedding.embedTcMETMuonCorrs = cms.bool(False)




from Configuration.StandardSequences.PATMC_cff import *

#process.load('Configuration.StandardSequences.PATMC_cff')
#process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
#process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
#process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

#pat muons 
mypatMuons = patMuons.clone()
mypatMuons.embedTrack = cms.bool(True)
mypatMuons.embedPFCandidate = cms.bool(True)
mypatMuons.embedPfEcalEnergy = cms.bool(True)
mypatMuons.embedCaloMETMuonCorrs = cms.bool(True)



goodMuonsFormumuSelection = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("mypatMuons"),
    cut = cms.string("pt > 8 && isPFMuon "),
)



producemumuSelection = cms.Sequence(
    makePatMuons
    + mypatMuons
    + goodMuonsFormumuSelection   
)







goodMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsForembedding"),
    cut = cms.string(
        'pt > 8 && abs(eta) < 2.5 && isGlobalMuon && isPFMuon'),
    filter = cms.bool(False)
)


patMuonstobereplaced = cms.EDProducer("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(True),
    # require one of the muons with pT > 17 GeV, and an invariant mass > 20 GeV
    cut = cms.string('charge = 0 & max(daughter(0).pt, daughter(1).pt) > 17 & mass > 20'),
    decay = cms.string("goodMuons@+ goodMuons@-")
)


patMuonstobereplacedFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("patMuonstobereplaced"),                             
    minNumber = cms.uint32(1),
    filter = cms.bool(True)
)


muonsForembeddingSelectionSequence = cms.Sequence(
    patMuonsForembedding
    + goodMuons
    + patMuonstobereplaced
)



