#!/usr/bin/env python

### Various set of customise functions needed for embedding
import FWCore.ParameterSet.Config as cms

def customiseAllSteps(process):
    process._Process__name +="embedding"
    print "Processing step: ",process._Process__name
    return process



def customiseMuonInputID(process, muon_src=cms.InputTag("patMuons"), muon_id='loose'):

    process.load('TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff')

    process.patMuonsAfterKinCuts.src = muon_src
    print "Input muons are",muon_src

    process.inputPath = cms.Path(process.makePatMuonsZmumuSelection)

    process.inputPath *= process.externalLHEProducer

    if muon_id == 'loose':
        process.patMuonsAfterID = process.patMuonsAfterLooseID.clone()
    elif muon_id == 'medium':
        process.patMuonsAfterID = process.patMuonsAfterMediumID.clone()
    elif muon_id == 'tight':
        process.patMuonsAfterID = process.patMuonsAfterTightID.clone()
    
    print "Muon ID used: ",muon_id," which means: cut =",process.patMuonsAfterID.cut
    
    #Getting the first output module and impose, that only events, which come through the 'inputPath' are saved.
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    outputModule = getattr(process, outputModulesList[0])
    outputModule.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("inputPath"))
    outputModule.outputCommands.extend(
        cms.untracked.vstring("drop * ",
            "keep LHEEventProduct_*_*_*",
            "keep LHERunInfoProduct_*_*_*",
            "keep *_*_*_SKIM",
        )
    )
    process.schedule.insert(0, process.inputPath)
    
    return process

def customiseMuonInputForMiniAOD(process,muon_id='loose'):
    return customiseMuonInputID(process,cms.InputTag("slimmedMuons"),muon_id)

def customiseMuonInputForRECO(process,muon_id='loose'):

    from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cff import patMuons, makePatMuons, muonMatch
    
    patMuons.addGenMatch = cms.bool(False)
    patMuons.embedGenMatch = False
    patMuons.genParticleMatch = ''
    patMuons.embedCaloMETMuonCorrs = cms.bool(False)
    patMuons.embedTcMETMuonCorrs = cms.bool(False)
    
    makePatMuons.remove(muonMatch)
    process = customiseMuonInputID(process,cms.InputTag("patMuons"),muon_id)
    i_path = getattr(process,'inputPath')
    #Producing patMuons after doubleMuonHLTTrigger, which are used for further selection
    i_path.replace(process.doubleMuonHLTTrigger, process.doubleMuonHLTTrigger + makePatMuons)
    return process
