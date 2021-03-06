# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --filein file:RAWSIM.root --fileout RECOSIM.root --mc --eventcontent RECOSIM --runUnscheduled --datatier RECOSIM --conditions 76X_mcRun2_asymptotic_v12 --step RAW2DIGI,L1Reco,RECO --era Run2_25ns --python_filename recosim.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 8
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Run2_25ns)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(8)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:RAWSIM.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:8'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RECOSIM'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('RECOSIM.root'),
    outputCommands = cms.untracked.vstring("keep *"),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_mcRun2_asymptotic_v12', '')

process.reconstruction = cms.Sequence(
    process.bunchSpacingProducer
    + process.siPixelClustersPreSplitting
    + process.siPixelRecHitsPreSplitting
    + process.siStripZeroSuppression
    + process.siStripClusters
    + process.siStripMatchedRecHits
    + process.clusterSummaryProducer
    + process.dt1DRecHits
    + process.dt4DSegments
    + process.dt1DCosmicRecHits
    + process.dt4DCosmicSegments
    + process.csc2DRecHits
    + process.cscSegments
    + process.rpcRecHits
    + process.ecalMultiFitUncalibRecHit
    + process.ecalDetIdToBeRecovered
    + process.ecalRecHit
    + process.ecalCompactTrigPrim
    + process.ecalTPSkim
    + process.ecalPreshowerRecHit
    + process.hbheprereco
    + process.hfreco
    + process.horeco
    + process.zdcreco
    + process.castorreco
    + process.offlineBeamSpot
    + process.MeasurementTrackerEventPreSplitting
    + process.siPixelClusterShapeCachePreSplitting
    + process.ancientMuonSeed
    + process.standAloneMuons
    + process.refittedStandAloneMuons
    + process.displacedMuonSeeds
    + process.displacedStandAloneMuons
    + process.initialStepSeedLayersPreSplitting
    + process.initialStepSeedsPreSplitting
    + process.initialStepTrackCandidatesPreSplitting
    + process.initialStepTracksPreSplitting
    + process.firstStepPrimaryVerticesPreSplitting
    + process.initialStepTrackRefsForJetsPreSplitting
    + process.caloTowerForTrkPreSplitting
    + process.ak4CaloJetsForTrkPreSplitting
    + process.jetsForCoreTrackingPreSplitting
    + process.siPixelClusters
)

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.RECOSIMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

