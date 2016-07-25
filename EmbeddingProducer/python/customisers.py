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



class module_manipulate():
  def __init__(self, module_name, manipulator_name, steps = ["SELECT","CLEAN","SIM","MERGE"], instance=[""]):
    self.module_name = module_name
    self.manipulator_name = manipulator_name
    self.steps = steps
    self.steps = instance
    self.merger_name = manipulator_name+"Merger"

    

to_bemanipulate = []

to_bemanipulate.append(module_manipulate(module_name = 'siPixelClusters', manipulator_name = "Pixel", steps = ["SELECT","CLEAN"] ))
to_bemanipulate.append(module_manipulate(module_name = 'siStripClusters', manipulator_name = "Strip", steps = ["SELECT","CLEAN"] ))
to_bemanipulate.append(module_manipulate(module_name = 'generalTracks', manipulator_name = "generalTracks", steps = ["SIM", "MERGE"]))
to_bemanipulate.append(module_manipulate(module_name = 'electronGsfTracks', manipulator_name = "electronGsfTracks", steps = ["SIM", "MERGE"]))


to_bemanipulate.append(module_manipulate(module_name = 'ecalRecHit', manipulator_name = "EcalRecHit", instance= ["EcalRecHitsEB","EcalRecHitsEE"]))
to_bemanipulate.append(module_manipulate(module_name = 'ecalPreshowerRecHit', manipulator_name = "EcalRecHit", instance= ["EcalRecHitsES"]))

to_bemanipulate.append(module_manipulate(module_name = 'hbheprereco', manipulator_name = "HBHERecHit"))
to_bemanipulate.append(module_manipulate(module_name = 'hbhereco', manipulator_name = "HBHERecHit"))
to_bemanipulate.append(module_manipulate(module_name = 'zdcreco', manipulator_name = "ZDCRecHit"))

to_bemanipulate.append(module_manipulate(module_name = 'horeco', manipulator_name = "HORecHit"))
to_bemanipulate.append(module_manipulate(module_name = 'hfreco', manipulator_name = "HFRecHit"))
to_bemanipulate.append(module_manipulate(module_name = 'castorreco', manipulator_name = "CastorRecHit"))


to_bemanipulate.append(module_manipulate(module_name = 'dt1DRecHits', manipulator_name = "DTRecHit"))
to_bemanipulate.append(module_manipulate(module_name = 'dt1DCosmicRecHits', manipulator_name = "DTRecHit"))
to_bemanipulate.append(module_manipulate(module_name = 'csc2DRecHits', manipulator_name = "CSCRecHit"))
to_bemanipulate.append(module_manipulate(module_name = 'rpcRecHits', manipulator_name = "RPCRecHit"))



def keepSelected():
   ret_vstring = cms.untracked.vstring(
             "keep *_patMuonsAfterID_*_SELECT",
             "keep *_slimmedMuons_*_SELECT",
             "keep *_selectedMuonsForEmbedding_*_SELECT",
             "keep recoVertexs_offlineSlimmedPrimaryVertices_*_SELECT",

	     ## in some old files this step was called SKIM. So keep this until they are outdated
             "keep *_patMuonsAfterID_*_SKIM",
             "keep *_slimmedMuons_*_SKIM",
             "keep *_selectedMuonsForEmbedding_*_SKIM",
             "keep recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM")
   for akt_manimod in to_bemanipulate:
      if "SELECT" in akt_manimod.steps:
	ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_SELECT") 
   return ret_vstring

def keepLHE(process):
    return cms.untracked.vstring("keep *_*_*_"+process._Process__name)


def keepSimulated():
    ret_vstring = cms.untracked.vstring()
    for akt_manimod in to_bemanipulate:
      if "MERGE" in akt_manimod.steps:
	akt_sim_name = "simulated"+akt_manimod.module_name
        ret_vstring.append("keep *_"+akt_sim_name+"_*_SIMembedding")
    ret_vstring.append("keep *_genParticles_*_SIMembedding") 
    return ret_vstring

def keepCleaned():
   ret_vstring = cms.untracked.vstring()
   for akt_manimod in to_bemanipulate:
      if "MERGE" in akt_manimod.steps:
	akt_clean_name = "cleaned"+akt_manimod.module_name
        ret_vstring.append("keep *_"+akt_clean_name+"_*_LHEembeddingCLEAN")
        ret_vstring.append("keep *_"+akt_clean_name+"_*_CLEAN")
   return ret_vstring
   


  
def keepMerged(process):
    ret_vstring = cms.untracked.vstring()
    for akt_manimod in to_bemanipulate:
      if "MERGE" in akt_manimod.steps:
	ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_"+process._Process__name) 
    ret_vstring.append("drop *_*_*_CLEAN")
    ret_vstring.append("drop *_*_*_SKIM") 
    ret_vstring.append("drop *_*_*_SELECT") 
    ret_vstring.append("drop *_*_*_LHEembeddingCLEAN") 
    ret_vstring.append("drop *_*_*_SIMembedding") 
    ret_vstring.append("drop *_*_*_GENembedding") 
    
    return ret_vstring

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
    
    ## Also add a copy of castor reco and hf reco. There is no need for a cleaning, but for the merging step they are needed

    
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
        outputModule.outputCommands.extend(keepLHE(process))
    return process
  

def customiseGenerator(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "SIMembedding"
    try:
      process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
    except:
      process.options = cms.untracked.PSet(emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis'))
      
    #)
    ## here correct the vertex collectoin
    process.load('TauAnalysis.EmbeddingProducer.EmbeddingVertexCorrector_cfi')
    process.VtxSmeared = process.VtxCorrectedToInput.clone()
    print "Correcting Vertex in genEvent to one from input. Replaced 'VtxSmeared' with the Corrector."
    
    ## This module runs the complete GEN-SIM-RECO step. Thefore just clone this collections
    process.merging = cms.Path()   
    for akt_manimod in to_bemanipulate:
      if "SIM" in akt_manimod.steps:
	new_sim_name = "simulated"+akt_manimod.module_name
	cloned_module = getattr(process, akt_manimod.module_name).clone()
	setattr(process, new_sim_name, cloned_module)
	process.reconstruction_step *= getattr(process, new_sim_name)
    
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(keepSelected()) #Also store the Selected muons 
        outputModule.outputCommands.extend(keepCleaned())
	outputModule.outputCommands.extend(keepSimulated())
	

    
    return process

################################ Customizer for merging ###########################

def customiseMerging(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "MERGE"
 
    process.merging = cms.Path()   
    for akt_manimod in to_bemanipulate:
      if "CLEAN" in akt_manimod.steps: 
	mergCollections_in = cms.VInputTag()   
        for instance in akt_manimod.instance:
	  if "MERGE" in akt_manimod.steps: 
	    mergCollections_in.append(cms.InputTag("simulated"+akt_manimod.module_name,instance,"")) ## Only merge simulated and cleaned for collection where the merging happens on the same level as cleaning (Calo and Muon Chambers). 
      	  mergCollections_in.append(cms.InputTag("cleaned"+akt_manimod.module_name,instance,"")) ## For Tracker this means its just a clone of the cleaned collections
        setattr(process, mod_name, cms.EDProducer(akt_manimod.merger_name,mergCollections = mergCollections_in))
        process.merging *= getattr(process, mod_name)
    process.schedule.insert(-1, process.merging)
    
    
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(keepMerged(process)) #Also store the Selected muons 
 
    return process



################################ cross Customizers ###########################

def customiseLHEandCleaning(process):
    process._Process__name = "LHEembeddingCLEAN"
    process = customiseCleaning(process,False)
    process = customiseLHE(process,False)
    return process




def customiseReconstruction(process):
    try:
      process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
    except:
      process.options = cms.untracked.PSet(emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis'))
      
  #  for akt_manimod in to_bemanipulate:
  #    if "CLEAN" in akt_manimod.steps:
  #      process.reconstruction_step.remove(getattr(process, akt_manimod.module_name))
        
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(cms.untracked.vstring(
            "keep LHEEventProduct_*_*_CLEANING",
            "keep LHERunInfoProduct_*_*_CLEANING",
            "keep *_*_*_GEN"
        ))
    return process




