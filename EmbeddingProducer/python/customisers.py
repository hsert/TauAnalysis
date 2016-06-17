#!/usr/bin/env python


### Various set of customise functions needed for embedding
import FWCore.ParameterSet.Config as cms

def customiseSkimming(process):
    process._Process__name = "SKIM"
    process.RECOoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("skimming"))
    process.RECOoutput.outputCommands.extend(cms.untracked.vstring(

        # muon collections considered for selection and LHE product
        "keep *_patMuonsAfterID_*_SKIM",
        "keep *_slimmedMuons_*_SKIM",
        "keep *_selectedMuonsForEmbedding_*_SKIM",

        # keep vertex collection for later LHEEventProduct creation
        "keep recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM"

    ))
    process.load('TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff')
    process.patMuonsAfterKinCuts.src = cms.InputTag("slimmedMuons","","SKIM")
    process.patMuonsAfterID = process.patMuonsAfterLooseID.clone()

    process.skimming = cms.Path(process.makePatMuonsZmumuSelection)
    process.schedule.insert(-1, process.skimming)
    return process

def customiseCleaning(process):
    process._Process__name = "CLEANING"
    process.load('TauAnalysis.EmbeddingProducer.cmsDriver_fragments.CleaningProcedure_cff')
    process.cleaning = cms.Path(process.makeCleaningProcedure)
    process.schedule.insert(0,process.cleaning)
    process.RECOoutput.outputCommands = cms.untracked.vstring("keep * ",
        "drop *_*_*_SKIM",
        "drop *_*_*_CLEANING",

        # LHE product collections for GEN step
        "keep LHEEventProduct_*_*_CLEANING",
        "keep LHERunInfoProduct_*_*_CLEANING",
        "keep *_externalLHEProducer_vertexPosition*_CLEANING",
        "keep recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM"
    )
    return process

def customiseGenerator(process):
    process.RECOSIMoutput.outputCommands = cms.untracked.vstring("keep * ",
    "drop *_externalLHEProducer_vertexPosition*_CLEANING",
    "drop recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM",
    "drop edmTriggerResults_TriggerResults_*_GEN"
    )
    return process

def customiseReconstruction(process):
    process.reconstruction_step.remove(process.siPixelClusters)
    process.reconstruction_step.remove(process.siStripClusters)
    process.reconstruction_step.remove(process.dt1DRecHits)
    process.reconstruction_step.remove(process.csc2DRecHits)
    process.reconstruction_step.remove(process.rpcRecHits)
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(cms.untracked.vstring(
            "keep LHEEventProduct_*_*_CLEANING",
            "keep LHERunInfoProduct_*_*_CLEANING",
            "keep *_*_*_GEN"
        ))
    return process


def customiseKeepCleaningCollections(process):
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(cms.untracked.vstring(

            # keep original RAW data for further steps
            "keep *_*_*_LHC",
            "keep *_*_*_HLT",

            # keep collections manipulated in cleaning step
            "keep *_siPixelClusters_*_"+process._Process__name,
            "keep *_siStripClusters_*_"+process._Process__name,
            "keep *_dt1DRecHits_*_"+process._Process__name,
            "keep *_csc2DRecHits_*_"+process._Process__name,
            "keep *_rpcRecHits_*_"+process._Process__name,

            "keep *_castorreco_*_"+process._Process__name,
            "keep *_hfreco_*_"+process._Process__name,
            "keep *_ecalPreshowerRecHit_*_"+process._Process__name,
            "keep *_ecalRecHit_*_"+process._Process__name,
            "keep *_hbhereco_*_"+process._Process__name,
            "keep *_horeco_*_"+process._Process__name
        ))
    return process

def customiseAllSteps(process):
    process._Process__name +="embedding"
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    outputModule = getattr(process, outputModulesList[0])
    outputModule.outputCommands.extend(cms.untracked.vstring("keep recoVertexs_offlineSlimmedPrimaryVertices__PAT",
    "keep edmHepMCProduct_*_*_"+process._Process__name
    ))
    print "Processing step: ",process._Process__name
    return process

def customiseDropInputRECO(process):
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    outputModule = getattr(process, outputModulesList[0])
    outputModule.outputCommands.extend(cms.untracked.vstring("drop *_*_*_RECO",
    "keep HcalNoiseSummary_hcalnoise_*_*",
    "keep ClusterSummary_clusterSummaryProducer_*_*",
    "keep L1GlobalTriggerReadoutRecord_gtDigis_*_*"
    ))
    return process
def customiseGeneratorVertexFromInput(process):

    from TauAnalysis.EmbeddingProducer.cmsDriver_fragments.VertexCorrector_cff import VtxCorrectedToInput
    process.VtxSmeared = VtxCorrectedToInput.clone()
    print "Correcting Vertex in genEvent to one from input. Replaced 'VtxSmeared' with the Corrector."
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
    outputModule.outputCommands.extend(cms.untracked.vstring("drop * ",
			 "keep LHEEventProduct_*_*_"+process._Process__name,
			 "keep LHERunInfoProduct_*_*_"+process._Process__name,
			 "keep *_externalLHEProducer_vertexPosition*_"+process._Process__name,
			 "keep recoVertexs_offlineSlimmedPrimaryVertices__PAT"
      ))


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
