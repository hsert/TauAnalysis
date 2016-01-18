import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.PAT_cff import *

from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi import patMuons
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import *


## Trigger requirements
doubleMuonTrigger = cms.EDFilter("TriggerResultsFilter",
    hltResults = cms.InputTag("TriggerResults","","HLT"),
    l1tResults = cms.InputTag(""),
    throw = cms.bool(False),
    triggerConditions = cms.vstring("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v* OR HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*")
)



## Muon selection
patMuonsEmbedding = patMuons.clone()
patMuonsEmbedding.addGenMatch = cms.bool(True)
patMuonsEmbedding.embedCaloMETMuonCorrs = cms.bool(False)
patMuonsEmbedding.embedTcMETMuonCorrs = cms.bool(False)


patMuonsAfterKinCuts = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag(
    "slimmedMuons"
    #"patMuonsEmbedding"
    ),
    cut = cms.string("pt > 8 && abs(eta) < 2.5"),
    filter = cms.bool(False)
)

ZmumuCandidates = cms.EDProducer("CandViewShallowCloneCombiner",
    checkCharge = cms.bool(True),
    # require one of the muons with pT > 17 GeV, and an invariant mass > 20 GeV
    cut = cms.string('charge = 0 & max(daughter(0).pt, daughter(1).pt) > 17 & mass > 20'),
    decay = cms.string("patMuonsAfterKinCuts@+ patMuonsAfterKinCuts@-")
)


ZmumuCandidatesFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("ZmumuCandidates"),
    minNumber = cms.uint32(0),
    filter = cms.bool(False)
)


## Sequence for Z->mumu selection
makePatMuonsZmumu = cms.Sequence(
#    doubleMuonTrigger
#    + makePatMuons
#    + patMuonsEmbedding
    patMuonsAfterKinCuts
    + ZmumuCandidates
#    + ZmumuCandidatesFilter
)



