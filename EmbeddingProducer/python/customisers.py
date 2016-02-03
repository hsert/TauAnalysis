#!/usr/bin/env python


### Various set of customise functions needed for embedding
import FWCore.ParameterSet.Config as cms


def customiseMuonInputID(process, muon_src=cms.InputTag("patMuons"), muon_id='loose'):

    process.load('TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff')

    process.patMuonsAfterKinCuts.src = muon_src
    print "Input mons are ",muon_src

    process.inputPath = cms.Path(process.makePatMuonsZmumuSelection)

    process.inputPath *= process.externalLHEProducer

    if muon_id == 'loose':
        process.patMuonsAfterID = process.patMuonsAfterLooseID.clone()
    elif muon_id == 'medium':
        process.patMuonsAfterID = process.patMuonsAfterMediumID.clone()
    elif muon_id == 'tight':
        process.patMuonsAfterID = process.patMuonsAfterTightID.clone()
    
    print "Muon ID used: ",muon_id," which means: cut=",process.patMuonsAfterID.cut
        
    outputmodule = process.schedule[-1]
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
    i_path.replace(process.doubleMuonHLTTrigger,process.doubleMuonHLTTrigger+process.makePatMuons)
    return process
