# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: TauAnalysis/EmbeddingProducer/python/lhehadronizerpythia8tauolafilter_cfi.py --filein file:skimmed.root --fileout file:step1.root --conditions auto:run2_mc --era Run2_25ns --eventcontent FEVTDEBUG --relval 9000,50 --step GEN,SIM --datatier GEN-SIM --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps --beamspot Realistic50ns13TeVCollision --no_exec -n -1
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('SIM',eras.Run2_25ns)

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
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring('file:skimmed.root'),
    inputCommands = cms.untracked.vstring('keep *', 
        'drop LHEXMLStringProduct_*_*_*'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('TauAnalysis/EmbeddingProducer/python/lhehadronizerpythia8tauolafilter_cfi.py nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:step1.root'),
    outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    ExternalDecays = cms.PSet(
        Tauola = cms.untracked.PSet(
            InputCards = cms.PSet(
                mdtau = cms.int32(0),
                pjak1 = cms.int32(1),
                pjak2 = cms.int32(2)
            ),
            UseTauolaPolarization = cms.bool(False)
        ),
        parameterSets = cms.vstring('Tauola')
    ),
    HepMCFilter = cms.PSet(
        filterName = cms.string('EmbeddingHepMCFilter'),
        filterParameters = cms.PSet(
            ElElCut = cms.string('El1.Pt > 22 && El2.Pt > 10'),
            ElHadCut = cms.string('El.Pt > 28 && Had.Pt > 25'),
            ElMuCut = cms.string('(El.Pt > 21 && Mu.Pt > 10) || (El.Pt > 10 && Mu.Pt > 21)'),
            HadHadCut = cms.string('Had1.Pt > 35 && Had2.Pt > 30'),
            MuHadCut = cms.string('Mu.Pt > 18 && Had.Pt > 25 && Mu.Eta < 2.1'),
            MuMuCut = cms.string('Mu1.Pt > 17 && Mu2.Pt > 8'),
            switchToMuonEmbedding = cms.bool(False)
        )
    ),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring('pythia8CommonSettings', 
            'pythia8CUEP8M1Settings', 
            'processParameters'),
        processParameters = cms.vstring('JetMatching:merge = off', 
            'Init:showChangedSettings = off', 
            'Init:showChangedParticleData = off'),
        pythia8CUEP8M1Settings = cms.vstring('Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:pT0Ref=2.4024', 
            'MultipartonInteractions:ecmPow=0.25208', 
            'MultipartonInteractions:expPow=1.6'),
        pythia8CommonSettings = cms.vstring('Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on')
    ),
    comEnergy = cms.double(13000.0),
    crossSection = cms.untracked.double(1.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(1),
    nAttempts = cms.uint32(10000),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0)
)


process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.FEVTDEBUGoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from TauAnalysis.EmbeddingProducer.customisers
from TauAnalysis.EmbeddingProducer.customisers import customiseAllSteps 

#call to customisation function customiseAllSteps imported from TauAnalysis.EmbeddingProducer.customisers
process = customiseAllSteps(process)

# End of customisation functions

