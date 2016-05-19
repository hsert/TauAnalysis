# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: gen --filein /store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/004544CB-6DD8-E511-97E4-0026189438F6.root --fileout file:skimmed.root --conditions 76X_mcRun2_asymptotic_v12 --era Run2_25ns --step NONE --customise TauAnalysis/EmbeddingProducer/customisers.customiseSkimming,TauAnalysis/EmbeddingProducer/customisers.customiseMuonInputForMiniAOD --no_exec -n -1 --python_filename skim.py
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
    fileNames = cms.untracked.vstring('/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/004544CB-6DD8-E511-97E4-0026189438F6.root'),
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
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_mcRun2_asymptotic_v12', '')

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

