# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: TauAnalysis/EmbeddingProducer/python/ZTauTauGeneration/test/lhehadronizerpythia8_noextdecayer_MT_cfi.py --filein file:skimmed.root --fileout file:step1.root --conditions 80X_mcRun2_asymptotic_2016_v3 --era Run2_25ns --eventcontent FEVTDEBUG --relval 9000,50 --step GEN,SIM --datatier GEN-SIM --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps,TauAnalysis/EmbeddingProducer/customisers.customiseGeneratorVertexFromInput --beamspot Realistic50ns13TeVCollision --no_exec -n -1 --python_filename embedding.py
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('GEN',eras.Run2_25ns)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic50ns13TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring('file:cleaned.root'),
    inputCommands = cms.untracked.vstring('keep *'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('TauAnalysis/EmbeddingProducer/python/ZTauTauGeneration/test/lhehadronizerpythia8_noextdecayer_MT_cfi.py nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:generated_and_cleaned.root'),
    outputCommands = cms.untracked.vstring("keep * ",
    "drop *_externalLHEProducer_vertexPosition*_CLEANING",
    "drop recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM",
    "drop edmTriggerResults_TriggerResults__GEN"
    ),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v15', '')

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *
process.generator = cms.EDFilter("Pythia8HadronizerFilter",
  
  maxEventsToPrint = cms.untracked.int32(1),
  nAttempts = cms.uint32(1),
  HepMCFilter = cms.PSet(
    filterName = cms.string('EmbeddingHepMCFilter'),
    filterParameters = cms.PSet(
      MuMuCut = cms.untracked.string("Mu1.Pt > 15 && Mu2.Pt > 6 && Mu1.Eta < 2.4 && Mu2.Eta < 2.4"),
      switchToMuonEmbedding = cms.bool(True)
    )
  ),
  pythiaPylistVerbosity = cms.untracked.int32(0),
  filterEfficiency = cms.untracked.double(1.0),
  pythiaHepMCVerbosity = cms.untracked.bool(False),
  comEnergy = cms.double(13000.),
  crossSection = cms.untracked.double(1.0),
  PythiaParameters = cms.PSet(
    pythia8CommonSettingsBlock,
    pythia8CUEP8M1SettingsBlock,
    processParameters = cms.vstring(
        
        'JetMatching:merge = off',
        'Init:showChangedSettings = off', 
        'Init:showChangedParticleData = off'
    ),
    parameterSets = cms.vstring('pythia8CommonSettings',
                                'pythia8CUEP8M1Settings',
                                'processParameters'
                                )
    )
)

process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.FEVTDEBUGoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from TauAnalysis.EmbeddingProducer.customisers
from TauAnalysis.EmbeddingProducer.customisers import customiseAllSteps, customiseGeneratorVertexFromInput

#call to customisation function customiseGeneratorVertexFromInput imported from TauAnalysis.EmbeddingProducer.customisers
process = customiseGeneratorVertexFromInput(process)

# End of customisation functions

