# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: rereco --conditions 76X_dataRun2_v15 --filein file:skimmed.root --fileout file:reco_Run2105.root --step L1Reco,RECO --datatier RECO --era Run2_25ns --eventcontent RECO --no_exec -n -1 --data --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps --python_filename reco_step.py
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('SKIM',eras.Run2_25ns)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'/store/data/Run2015D/DoubleMuon/MINIAOD/16Dec2015-v1/10000/00039A2E-D7A7-E511-98EE-3417EBE64696.root'
),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('rereco nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RECO'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:skimmed.root'),
    outputCommands = cms.untracked.vstring("keep * ",
    ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("inputPathAndCleaning")),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v15', '')

# Path and EndPath definitions

# Selection of muons from input
process.load('TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff')
process.patMuonsAfterKinCuts.src = cms.InputTag("slimmedMuons")
process.patMuonsAfterID = process.patMuonsAfterLooseID.clone()

process.inputPathAndCleaning = cms.Path(process.makePatMuonsZmumuSelection)

process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)

# Schedule definition

process.schedule = cms.Schedule(
   process.inputPathAndCleaning,
   process.endjob_step,
   process.RECOoutput_step)
# customisation of the process.

# End of customisation functions

