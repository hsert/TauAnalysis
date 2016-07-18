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

to_bemanipulate ={}
to_bemanipulate['siPixelClusters']=["Pixel",[""]]
to_bemanipulate['siPixelClustersPreSplitting']=["Pixel",[""]]
to_bemanipulate['siStripClusters']=["Strip",[""]]
to_bemanipulate['ecalRecHit']=["EcalRecHit",["EcalRecHitsEB","EcalRecHitsEE"]]
to_bemanipulate['ecalPreshowerRecHit']=["EcalRecHit",["EcalRecHitsES"]]

to_bemanipulate['hbheprereco']=["HBHERecHit",[""]]
to_bemanipulate['hbhereco']=["HBHERecHit",[""]]
to_bemanipulate['zdcreco']=["ZDCRecHit",[""]]



to_bemanipulate['horeco']=["HORecHit",[""]]
to_bemanipulate['hfreco']=["HFRecHit",[""]]
to_bemanipulate['castorreco']=["CastorRecHit",[""]]
to_bemanipulate['dt1DRecHits']=["DTRecHit",[""]]
to_bemanipulate['dt1DCosmicRecHits']=["DTRecHit",[""]]
to_bemanipulate['csc2DRecHits']=["CSCRecHit",[""]]
to_bemanipulate['rpcRecHits']=["RPCRecHit",[""]]







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
   for akt_name in to_bemanipulate:
#      ret_vstring.append("keep *_"+akt_name+"_*_SKIM") 
      ret_vstring.append("keep *_"+akt_name+"_*_SELECT") 
   return ret_vstring

def keepLHE(process):
    return cms.untracked.vstring("keep *_*_*_"+process._Process__name)


def keepSimulated():
    ret_vstring = cms.untracked.vstring()
    for akt_name in to_bemanipulate:
      akt_sim_name = "simulated"+akt_name
      ret_vstring.append("keep *_"+akt_sim_name+"_*_SIMembedding")
    ret_vstring.append("keep *_genParticles_*_SIMembedding") 
    ret_vstring.append("keep *_MeasurementTrackerEventPreSplitting_*_SIMembedding") 
    ret_vstring.append("keep *_ecalMultiFitUncalibRecHit_*_SIMembedding") 
    ret_vstring.append("keep *_siPixelDigis_*_SIMembedding") 
    ret_vstring.append("keep *_siStripDigis_*_SIMembedding") 
    #ret_vstring.append("keep *_siStripZeroSuppression_*_SIMembedding") 
    ret_vstring.append("keep *_ecalDigis_*_SIMembedding") 
    ret_vstring.append("keep *_hcalDigis_*_SIMembedding") 
    
    return ret_vstring

def keepCleaned():
   return cms.untracked.vstring(
                         "keep *_*_*_CLEAN",
                         "keep *_*_*_LHEembeddingCLEAN"          
                         )


  
def keepMerged(process):
    ret_vstring = cms.untracked.vstring()
    for akt_name in to_bemanipulate:
      ret_vstring.append("keep *_"+akt_name+"_*_"+process._Process__name)
    ret_vstring.append("drop *_*_*_CLEAN")
    ret_vstring.append("drop *_*_*_SKIM") 
    ret_vstring.append("drop *_*_*_SELECT") 
    ret_vstring.append("drop *_*_*_HLT") 
    ret_vstring.append("drop *_*_*_LHC") 
    ret_vstring.append("drop *_*_*_LHEembeddingCLEAN") 
    ret_vstring.append("drop *_*_*_SIMembedding") 
    ret_vstring.append("keep *_rawDataCollector_*_SIMembedding") 
    #ret_vstring.append("keep *_MeasurementTrackerEventPreSplitting_*_SIMembedding") 
    #ret_vstring.append("keep *_MeasurementTrackerEvent_*_SIMembedding") 
    ret_vstring.append("keep *_genParticles_*_SIMembedding") 
    ret_vstring.append("keep *_ecalMultiFitUncalibRecHit_*_SIMembedding") 
    ret_vstring.append("keep *_siPixelDigis_*_SIMembedding") 
    ret_vstring.append("keep *_siStripDigis_*_SIMembedding") 
    ret_vstring.append("keep *_ecalDigis_*_SIMembedding") 
    ret_vstring.append("keep *_hcalDigis_*_SIMembedding") 
    
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
      
  #  process.RAWSIMoutput.outputCommands = cms.untracked.vstring("keep * ",
  #  "drop *_externalLHEProducer_vertexPosition*_CLEANING",
  #  "drop recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM",
   # "drop edmTriggerResults_TriggerResults_*_GEN"
    #)
    ## here correct the vertex collectoin
    process.load('TauAnalysis.EmbeddingProducer.EmbeddingVertexCorrector_cfi')
    process.VtxSmeared = process.VtxCorrectedToInput.clone()
    print "Correcting Vertex in genEvent to one from input. Replaced 'VtxSmeared' with the Corrector."
    
    
    process.merging = cms.Path()   
    for org_sim_name in to_bemanipulate:
      new_sim_name = "simulated"+org_sim_name
      cloned_module = getattr(process, org_sim_name).clone()
      setattr(process, new_sim_name, cloned_module)
      process.reconstruction_step *= getattr(process, new_sim_name)
     
    
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(keepSelected()) #Also store the Selected muons 
        outputModule.outputCommands.extend(keepCleaned())
	outputModule.outputCommands.extend(keepSimulated())
      #  outputModule.outputCommands.extend(cms.untracked.vstring("keep *"))
    
    return process

################################ Customizer for merging ###########################

def customiseMerging(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "MERGE"
 
    process.merging = cms.Path()   
    for mod_name in to_bemanipulate:
      mergCollections_in = cms.VInputTag()
      for instance in to_bemanipulate[mod_name][1]:
#	mergCollections_in.append(cms.InputTag("simulated"+mod_name,instance,""))
      	mergCollections_in.append(cms.InputTag("cleaned"+mod_name,instance,""))
      setattr(process, mod_name, cms.EDProducer(to_bemanipulate[mod_name][0]+"Merger",mergCollections = mergCollections_in))
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
  
    for mod_name in to_bemanipulate: 
      process.reconstruction_step.remove(getattr(process, mod_name))
    

    
    #process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag("siPixelDigis","","SIMembedding")
    #process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag("siStripDigis","","SIMembedding")
    
    #process.MeasurementTrackerEventPreSplitting.inactivePixelDetectorLabels = cms.VInputTag("siPixelDigis","","SIMembedding")
    #process.MeasurementTrackerEventPreSplitting.inactiveStripDetectorLabels = cms.VInputTag("siStripDigis","","SIMembedding")
    
    #process.MeasurementTrackerEvent.switchOffPixelsIfEmpty = cms.bool(False)
    #process.MeasurementTrackerEventPreSplitting.switchOffPixelsIfEmpty = cms.bool(False) 
  #  process.raw2digi_step.remove(process.siPixelDigis)
  #  process.raw2digi_step.remove(process.siStripDigis)
    
 #   process.reconstruction_step.remove(process.MeasurementTrackerEvent)
 #   process.reconstruction_step.remove(process.MeasurementTrackerEventPreSplitting)
    
#    process.reconstruction_step.remove(process.siPixelClusters)
#    process.reconstruction_step.remove(process.siStripClusters)
#    process.reconstruction_step.remove(process.ecalRecHit)
#    process.reconstruction_step.remove(process.ecalPreshowerRecHit)
#    process.reconstruction_step.remove(process.hbhereco)
#    process.reconstruction_step.remove(process.horeco)
#    process.reconstruction_step.remove(process.dt1DRecHits)
#    process.reconstruction_step.remove(process.csc2DRecHits)
#    process.reconstruction_step.remove(process.rpcRecHits)
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
        outputModule = getattr(process, outputModule)
        outputModule.outputCommands.extend(cms.untracked.vstring(
            "keep LHEEventProduct_*_*_CLEANING",
            "keep LHERunInfoProduct_*_*_CLEANING",
            "keep *_*_*_GEN"
        ))
    return process




