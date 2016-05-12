# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: gen --filein root://dcache-cms-xrootd.desy.de:1094//store/mc/RunIISpring16MiniAODv1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/20000/0017320C-7BFC-E511-9B2D-0CC47A4C8E34.root --fileout file:skimmed.root --conditions 80X_mcRun2_asymptotic_2016_v3 --era Run2_25ns --step NONE --customise TauAnalysis/EmbeddingProducer/customisers.customiseSkimming,TauAnalysis/EmbeddingProducer/customisers.customiseMuonInputForMiniAOD --no_exec -n -1 --python_filename skim.py
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('NONE',eras.Run2_25ns)

# import of standard configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://dcache-cms-xrootd.desy.de:1094//store/mc/RunIISpring16MiniAODv1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/20000/0017320C-7BFC-E511-9B2D-0CC47A4C8E34.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('gen nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:skimmed.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_v3', '')

# Path and EndPath definitions
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.RECOSIMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from TauAnalysis.EmbeddingProducer.customisers
from TauAnalysis.EmbeddingProducer.customisers import customiseSkimming,customiseMuonInputForMiniAOD 

#call to customisation function customiseSkimming imported from TauAnalysis.EmbeddingProducer.customisers
process = customiseSkimming(process)

#call to customisation function customiseMuonInputForMiniAOD imported from TauAnalysis.EmbeddingProducer.customisers
process = customiseMuonInputForMiniAOD(process)

# End of customisation functions

