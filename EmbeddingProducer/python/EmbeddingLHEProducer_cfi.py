import FWCore.ParameterSet.Config as cms


externalLHEProducer = cms.EDProducer("EmbeddingLHEProducer",
    src = cms.InputTag("selectedMuonsForEmbedding","",""),
    switchToMuonEmbedding = cms.bool(True),
    mirroring = cms.bool(False),
    studyFSRmode = cms.untracked.string("reco")
)

makeexternalLHEProducer = cms.Sequence( externalLHEProducer)