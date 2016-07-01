#!/usr/bin/env python


### Various set of customise functions needed for embedding
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.Utilities import cleanUnscheduled


################################ Customizer for skimming ###########################
### In the skimming one hast to run from RAW (over RECO) to MiniAOD 
### We need the save 
### RAW (Since in the end we want to run over this collection again) 
### RECO (maybe pick the muon + detinfo in futur)
### selectedMuonsForEmbedding which are PAT muons with special requierments

to_beclened = ['siPixelClusters','siStripClusters','ecalRecHit','ecalPreshowerRecHit','hbhereco','horeco','dt1DRecHits','csc2DRecHits','rpcRecHits']
to_besimulated  = to_beclened[:]
to_besimulated.extend(['castorreco','hfreco'])

def keepSelected():
   return cms.untracked.vstring(
             "keep *_patMuonsAfterID_*_SELECT",
             "keep *_slimmedMuons_*_SELECT",
             "keep *_selectedMuonsForEmbedding_*_SELECT",
             "keep recoVertexs_offlineSlimmedPrimaryVertices_*_SELECT",

	     ## in some old files this step was called SKIM. So keep this until they are outdated
             "keep *_patMuonsAfterID_*_SKIM",
             "keep *_slimmedMuons_*_SKIM",
             "keep *_selectedMuonsForEmbedding_*_SKIM",
             "keep recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM")

def keepCleaned():
   return cms.untracked.vstring(
			  "keep *_*_*_CLEAN",
			  "keep *_*_*_LHEembeddingCLEAN"	  
			  )
def keepSimulated():
    ret_vstring = cms.untracked.vstring()
    for akt_name in to_besimulated:
      akt_sim_name = "simulated"+akt_name
      ret_vstring.append("keep *_"+akt_sim_name+"_*_SIMembedding")
    return ret_vstring

def keepThisStep(process):
   return cms.untracked.vstring("keep *_*_*_"+process._Process__name)


################################ Customizer for Selecting ###########################


def customiseSelecting(process):
    process._Process__name = "SELECT"

    process.load('TauAnalysis.EmbeddingProducer.SelectingProcedure_cff')
    process.patMuonsAfterKinCuts.src = cms.InputTag("slimmedMuons","","SELECT")
    process.patMuonsAfterID = process.patMuonsAfterLooseID.clone()

    process.selecting = cms.Path(process.makePatMuonsZmumuSelection)
    process.schedule.insert(-1, process.selecting)
    
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("selecting"))
        outputModule.outputCommands.extend(keepSelected())    
    return process

################################ Customizer for cleaining ###########################
## input are some RECO collections (
## siPixelClusters,siStripClusters,ecalRecHit,ecalPreshowerRecHit,hbhereco,horeco,dt1DRecHits,csc2DRecHits,rpcRecHits)
## which will with clenaed collections

def customiseCleaning(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "CLEAN"
    process.load('TauAnalysis.EmbeddingProducer.CleaningProcedure_cff')
 
  ## the next three StandardSequences are needed for the track assicator, 
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
    process.load('Configuration.StandardSequences.Reconstruction_cff')
     
    process.cleaning = cms.Path(process.makeCleaningProcedure)
    process.schedule.insert(0,process.cleaning)
 
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(keepSelected()) #Also store the Selected muons 
        outputModule.outputCommands.extend(keepCleaned())
    return process
  
  
################################ Customizer for simulaton ###########################

def customiseLHE(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "LHEembedding"
    process.load('TauAnalysis.EmbeddingProducer.EmbeddingLHEProducer_cfi')
    process.lheproduction = cms.Path(process.makeexternalLHEProducer)
    process.schedule.insert(0,process.lheproduction)
    try:
      process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')## Filter out all empty lumis and runs (Otherwise pythia8 will crash)
    except:
      process.options = cms.untracked.PSet(emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis'))
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(keepSelected()) #Also store the Selected muons 
        outputModule.outputCommands.extend(keepThisStep(process))
    return process


def manipulate_reco_step(process):
    ###print "reduce the reco step to the minimum" ## not true in the moment
    ### At the moment keep the complett reco schedule, but in principle we could clean it up and only produce the "simulated*" once (and the module afterwards are unecessary.
    for akt_mod_name in to_besimulated:
      new_mod_name = "simulated"+akt_mod_name
      cloned_module = getattr(process, akt_mod_name).clone()
      setattr(process, new_mod_name, cloned_module)
      process.reconstruction_step *= getattr(process, new_mod_name)
    return process


def customiseGenerator(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "SIMembedding"
    try:
      process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
    except:
      process.options = cms.untracked.PSet(emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis'))
      
  #  process.RAWSIMoutput.outputCommands = cms.untracked.vstring("keep * ",
  #  "drop *_externalLHEProducer_vertexPosition*_CLEANING",
  #  "drop recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM",
   # "drop edmTriggerResults_TriggerResults_*_GEN"
    #)
    ## here correct the vertex collectoin
    process.load('TauAnalysis.EmbeddingProducer.EmbeddingVertexCorrector_cfi')
    process.VtxSmeared = process.VtxCorrectedToInput.clone()
    print "Correcting Vertex in genEvent to one from input. Replaced 'VtxSmeared' with the Corrector."
    
    process = manipulate_reco_step(process)
    
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(keepSelected()) #Also store the Selected muons 
        outputModule.outputCommands.extend(keepCleaned())
        outputModule.outputCommands.extend(keepSimulated())
      #  outputModule.outputCommands.extend(cms.untracked.vstring("keep *"))
    
    return process




################################ cross Customizers ###########################

def customiseLHEandCleaning(process):
    process._Process__name = "LHEembeddingCLEAN"
    process = customiseCleaning(process,False)
    process = customiseLHE(process,False)
    return process




def customiseReconstruction(process):
    process.reconstruction_step.remove(process.siPixelClusters)
    process.reconstruction_step.remove(process.siStripClusters)
    process.reconstruction_step.remove(process.ecalRecHit)
    process.reconstruction_step.remove(process.ecalPreshowerRecHit)
    process.reconstruction_step.remove(process.hbhereco)
    process.reconstruction_step.remove(process.horeco)
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




