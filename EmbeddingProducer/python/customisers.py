#!/usr/bin/env python


### Various set of customise functions needed for embedding
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.Utilities import cleanUnscheduled


################################ Customizer for skimming ###########################
### There are four different parts. 
##First step is the SELECT (former SKIM) part, where we identfy the events which are good for Embedding. Need to store RAWRECO [RAW is needed for the MERG and RECO for the CLEAN step]
##Second step is the CLEAN input are PAT muons with RECO information. After this step only RAW plus some special collections needed for the MERG step must be saved
##Third step is the SIM. The input is the externalLHEProducer, which must be produced before (At the moment we do it parallel to the CLEAN step). Again only save RAW of the SELECT and only save what is need for the MERG step
##Last step is the MERG step. Which is the usally reconstruction, where the input produces are replaced by merg producer, which mix the SIM and CLEAN inputs.

## Some comments on this approach. All steps runs the RECO sequence until the end in the moment. It would be possible to stop after the all inputs which are needed for the MERG step are generated (which happens at a very early state of the reconstruction. But with this approach we are able to get the RECO (and PAT aka miniAOD) of all four step SELECT (orginal event), SIM, CLEAN and MERGED. Therefor one only needs to SAVE the corresponding output (in cmsDriver change output to RAW -> RAW,RECO,PAT and be modyfiy the keepSimulated() function, which drops most of the produced Collections at the moment)

#######################  Some basic functions ####################
## Helper Class, which summerizes in which step which Producer (Cleaner Merger), should be loaded. It is also usefull to define which collection should be stored for the next step
## E.g What is needed for MERGE must be produce in the CLEAN and SIM step 


class module_manipulate():
  def __init__(self, module_name, manipulator_name, steps = ["SELECT","CLEAN","SIM","MERGE"], instance=[""]):
    self.module_name = module_name
    self.manipulator_name = manipulator_name
    self.steps = steps
    self.instance = instance
    self.merger_name = manipulator_name+"Merger"
    self.cleaner_name = manipulator_name+"Cleaner"

    
to_bemanipulate = []

to_bemanipulate.append(module_manipulate(module_name = 'siPixelClusters', manipulator_name = "Pixel", steps = ["SELECT","CLEAN"] ))
to_bemanipulate.append(module_manipulate(module_name = 'siStripClusters', manipulator_name = "Strip", steps = ["SELECT","CLEAN"] ))
#to_bemanipulate.append(module_manipulate(module_name = 'generalTracks', manipulator_name = "generalTracks", steps = ["SIM", "MERGE"]))
#to_bemanipulate.append(module_manipulate(module_name = 'electronGsfTracks', manipulator_name = "electronGsfTracks", steps = ["SIM", "MERGE"]))


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



     
def keepMerged(process):
    ret_vstring = cms.untracked.vstring()
    ret_vstring.append("drop *_*_*_CLEAN")
    ret_vstring.append("drop *_*_*_SKIM") 
    ret_vstring.append("drop *_*_*_SELECT") 
    ret_vstring.append("drop *_*_*_LHEembeddingCLEAN") 
    ret_vstring.append("drop *_*_*_SIMembedding") 
    for akt_manimod in to_bemanipulate:
      if "CLEAN" in akt_manimod.steps:
	ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_"+process._Process__name) 
    return ret_vstring
  
def modify_outputModules(process, keep_drop_list = [], module_veto_list = [] ):
    outputModulesList = [key for key,value in process.outputModules.iteritems()]
    for outputModule in outputModulesList:
	if outputModule in module_veto_list:
	  continue
        outputModule = getattr(process, outputModule)
        for add_element in keep_drop_list:
	  outputModule.outputCommands.extend(add_element)    
    return process

  

################################ Customizer for Selecting ###########################

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
      if "CLEAN" in akt_manimod.steps:
	ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_SELECT") 
	ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_SKIM") 
   return ret_vstring



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
    return modify_outputModules(process,[keepSelected()])

################################ Customizer for cleaining ###########################
def keepCleaned():
   ret_vstring = cms.untracked.vstring()
   for akt_manimod in to_bemanipulate:
      if "MERGE" in akt_manimod.steps:
        ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_LHEembeddingCLEAN")
        ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_CLEAN")
   return ret_vstring



def customiseCleaning(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "CLEAN"
    ## Needed for the Calo Cleaner, could also be put into a function wich fix the input parameters
    from TrackingTools.TrackAssociator.default_cfi import TrackAssociatorParameterBlock
    TrackAssociatorParameterBlock.TrackAssociatorParameters.CSCSegmentCollectionLabel = cms.InputTag("cscSegments","","SELECT")
    TrackAssociatorParameterBlock.TrackAssociatorParameters.CaloTowerCollectionLabel = cms.InputTag("towerMaker","","SELECT")
    TrackAssociatorParameterBlock.TrackAssociatorParameters.DTRecSegment4DCollectionLabel = cms.InputTag("dt4DSegments","","SELECT")
    TrackAssociatorParameterBlock.TrackAssociatorParameters.EBRecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB","SELECT")
    TrackAssociatorParameterBlock.TrackAssociatorParameters.EERecHitCollectionLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE","SELECT")
    TrackAssociatorParameterBlock.TrackAssociatorParameters.HBHERecHitCollectionLabel = cms.InputTag("hbhereco","","SELECT")
    TrackAssociatorParameterBlock.TrackAssociatorParameters.HORecHitCollectionLabel = cms.InputTag("horeco","","SELECT")

    
    MuonImput = cms.InputTag("selectedMuonsForEmbedding","","")  ## This are the muon
    for akt_manimod in to_bemanipulate:
      if "CLEAN" in akt_manimod.steps:
        oldCollections_in = cms.VInputTag()   
        for instance in akt_manimod.instance:
	    oldCollections_in.append(cms.InputTag(akt_manimod.module_name,instance,"SELECT"))
        setattr(process, akt_manimod.module_name, cms.EDProducer(akt_manimod.cleaner_name,
                                                                 MuonCollection = MuonImput,
                                                                 TrackAssociatorParameters = TrackAssociatorParameterBlock.TrackAssociatorParameters,
                                                                 oldCollection = oldCollections_in))
    process.ecalPreshowerRecHit.TrackAssociatorParameters.usePreshower = cms.bool(True)    
    return modify_outputModules(process,[keepSelected(),keepCleaned()])
        
  
################################ Customizer for simulaton ###########################
def keepLHE():
    ret_vstring = cms.untracked.vstring()
    ret_vstring.append("keep *_externalLHEProducer_*_LHE")
    ret_vstring.append("keep *_externalLHEProducer_*_LHEembeddingCLEAN")
    return ret_vstring


def keepSimulated():
    ret_vstring = cms.untracked.vstring()
    ret_vstring.append("drop *_*_*_SIMembedding") 
    for akt_manimod in to_bemanipulate:
      if "MERGE" in akt_manimod.steps:
        ret_vstring.append("keep *_"+akt_manimod.module_name+"_*_SIMembedding")
    ret_vstring.append("keep *_genParticles_*_SIMembedding") 
    return ret_vstring




def customiseLHE(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "LHEembedding"
    process.load('TauAnalysis.EmbeddingProducer.EmbeddingLHEProducer_cfi')
    process.lheproduction = cms.Path(process.makeexternalLHEProducer)
    process.schedule.insert(0,process.lheproduction)

    return modify_outputModules(process,[keepSelected(),keepLHE()])
  

def customiseGenerator(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "SIMembedding"      
    #)
    ## here correct the vertex collectoin
    process.load('TauAnalysis.EmbeddingProducer.EmbeddingVertexCorrector_cfi')
    process.VtxSmeared = process.VtxCorrectedToInput.clone()
    print "Correcting Vertex in genEvent to one from input. Replaced 'VtxSmeared' with the Corrector."
    
    process.mix.digitizers.ecal.doESNoise = cms.bool(False)
    process.mix.digitizers.ecal.doENoise = cms.bool(False)
    process.mix.digitizers.hcal.doNoise = cms.bool(False)
    process.mix.digitizers.hcal.doThermalNoise = cms.bool(False)

  #  process.mix.digitizers.pixel.AddNoisyPixels = cms.bool(False)    
  #  process.mix.digitizers.pixel.AddNoise = cms.bool(False)    
    return modify_outputModules(process,[keepSelected(),keepCleaned(),keepSimulated()])
    

################################ Customizer for merging ###########################

def customiseMerging(process, changeProcessname=True):
    if changeProcessname:
      process._Process__name = "MERGE"
            
    for akt_manimod in to_bemanipulate:
      if "MERGE" in akt_manimod.steps:
        mergCollections_in = cms.VInputTag()   
        for instance in akt_manimod.instance:
          mergCollections_in.append(cms.InputTag(akt_manimod.module_name,instance,"SIMembedding"))
          mergCollections_in.append(cms.InputTag(akt_manimod.module_name,instance,"LHEembeddingCLEAN")) ##  Mayb make some process history magic which finds out if it was CLEAN or LHEembeddingCLEAN step
        setattr(process, akt_manimod.module_name, cms.EDProducer(akt_manimod.merger_name,mergCollections = mergCollections_in))

    return process

#    outputModulesList = [key for key,value in process.outputModules.iteritems()]
#    for outputModule in outputModulesList:
#        outputModule = getattr(process, outputModule)
#        outputModule.outputCommands.extend(cms.untracked.vstring(
#            "keep LHEEventProduct_*_*_CLEANING",
#            "keep LHERunInfoProduct_*_*_CLEANING",
#            "keep *_*_*_GEN"


################################ cross Customizers ###########################

def customiseLHEandCleaning(process):
    process._Process__name = "LHEembeddingCLEAN"
    process = customiseCleaning(process,False)
    process = customiseLHE(process,False)
    return process

################################ additionla Customizer ###########################

def customisoptions(process):
    try:
      process.options.emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis')
    except:
      process.options = cms.untracked.PSet(emptyRunLumiMode = cms.untracked.string('doNotHandleEmptyRunsAndLumis'))
    return process


