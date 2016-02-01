#!/usr/bin/env python


### Various set of customise functions needed for embedding
import FWCore.ParameterSet.Config as cms


# Muon selection

def muonSelectionPath(process, ID = "loose"):
    from TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff import patMuonsAfterID
    path = cms.Path()
    if ID == "loose": patMuonsAfterID.cut = cms.string("isLooseMuon")
    elif ID == "medium": patMuonsAfterID.cut = cms.string("isMediumMuon")
    elif ID == "tight": patMuonsAfterID.cut = cut = cms.string(
        "isPFMuon && isGlobalMuon"
        " && muonID('GlobalMuonPromptTight')"
        " && numberOfMatchedStations > 1"
        " && innerTrack.hitPattern.trackerLayersWithMeasurement > 5"
        " && innerTrack.hitPattern.numberOfValidPixelHits > 0"
        " && dB < 0.2"
    )
    path *= (process.hltTriggerType * process.makePatMuonsZmumuBaseline * patMuonsAfterID 
                                    * process.makeZmumuCandidates * process.hltBoolEnd)
    return path

def customiseMuonInputID(process):
    
    process.muonsLooseID = muonSelectionPath(process, "loose")
    process.muonsLooseID *= process.externalLHEProducer
    process.schedule.insert(-1, process.muonsLooseID)
    
    process.muonsMediumID = muonSelectionPath(process, "medium")
    process.schedule.insert(-1, process.muonsMediumID)
    
    process.muonsTightID = muonSelectionPath(process, "tight")
    process.schedule.insert(-1, process.muonsTightID)
    
    return process

def customiseMuonInputForMiniAOD(process):
    process.inputPath = cms.Path()
    process.twoSlimmedMuonsFilter = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("slimmedMuons"),
        minNumber = cms.uint32(2),
        maxNumber = cms.uint32(999999),
        filter = cms.bool(True)
        )
    
    process.inputPath *= process.twoSlimmedMuonsFilter
    process.patMuonsAfterKinCuts.src = cms.InputTag("slimmedMuons")
    process.schedule.insert(0, process.inputPath)
    return customiseMuonInputID(process)

def customiseMuonInputForRECO(process):
    process.inputPath = cms.Path()

    from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cff import patMuons, makePatMuons, muonMatch
    
    patMuons.addGenMatch = cms.bool(False)
    patMuons.embedGenMatch = False
    patMuons.genParticleMatch = ''
    patMuons.embedCaloMETMuonCorrs = cms.bool(False)
    patMuons.embedTcMETMuonCorrs = cms.bool(False)
    
    makePatMuons.remove(muonMatch)
    process.inputPath *= makePatMuons
    
    process.twoPatMuonsFilter = cms.EDFilter("PATCandViewCountFilter",
       src = cms.InputTag("patMuons"),
       minNumber = cms.uint32(2),
       maxNumber = cms.uint32(999999),
       filter = cms.bool(True)
       )
    
    process.inputPath *= process.twoPatMuonsFilter
    process.patMuonsAfterKinCuts.src = cms.InputTag("patMuons")
    process.schedule.insert(0, process.inputPath)
    return customiseMuonInputID(process)

