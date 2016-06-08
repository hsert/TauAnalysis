# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: rereco --conditions 76X_dataRun2_v15 --filein file:skimmed.root --fileout file:reco_Run2105.root --step L1Reco,RECO --datatier RECO --era Run2_25ns --eventcontent RECO --no_exec -n -1 --data --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps --python_filename reco_step.py
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('CLEANING',eras.Run2_25ns)

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
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'file:/pnfs/desy.de/cms/tier2/store/user/aakhmets/grid-control/DoubleMuon_Run2015D-v1_RAW/BASIC_SKIM_TEST_CMSSW_7_6_4_AACHEN/1/RAWskimmed_0.root'
),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('CLEANING nevts:-1'),
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
	fileName = cms.untracked.string('file:cleaned.root'),
	outputCommands = cms.untracked.vstring("keep * ",
		"drop *_*_*_SKIM",

		"drop *_*_*_CLEANING",
		# LHE product collections for GEN step
		"keep LHEEventProduct_*_*_CLEANING",
		"keep LHERunInfoProduct_*_*_CLEANING",
		"keep *_externalLHEProducer_vertexPosition*_CLEANING",
		"keep recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM",
		
		# save collections manipulated by CLEANING only
		"keep *_siPixelClusters_*_CLEANING",
		"keep *_siStripClusters_*_CLEANING",
		"keep *_dt1DRecHits_*_CLEANING",
		"keep *_csc2DRecHits_*_CLEANING",
		"keep *_rpcRecHits_*_CLEANING",
	),
	splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v15', '')


#process.siStripClusters  = cms.EDProducer('MuonCleaner',
process.siPixelClusters = cms.EDProducer('PixelCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","SKIM"),
        pixelClusters = cms.InputTag("siPixelClusters","","SKIM")
)

process.siStripClusters = cms.EDProducer('StripCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","SKIM"),
	stripClusters = cms.InputTag("siStripClusters","","SKIM"),
)

process.dt1DRecHits = cms.EDProducer('DTCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","SKIM"),
	oldCollection = cms.InputTag("dt1DRecHits","","SKIM"),
)

process.csc2DRecHits = cms.EDProducer('CSCCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","SKIM"),
	oldCollection  = cms.InputTag("csc2DRecHits","","SKIM"),
)

process.rpcRecHits = cms.EDProducer('RPCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","SKIM"),
	oldCollection  = cms.InputTag("rpcRecHits","","SKIM"),
)


# Path and EndPath definitions

process.externalLHEProducer = cms.EDProducer("EmbeddingLHEProducer",
	src = cms.InputTag("patMuonsAfterID","","SKIM"),
	switchToMuonEmbedding = cms.bool(True),
	mirroring = cms.bool(False),
	studyFSRmode = cms.untracked.string("reco")
    )


# Selection of muons from input
process.cleaning = cms.Path(
	process.siPixelClusters
	+ process.siStripClusters
	+ process.dt1DRecHits
	+ process.dt2DSegments
	+ process.csc2DRecHits
	+ process.rpcRecHits
	+ process.externalLHEProducer
)

process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)

# Schedule definition

process.schedule = cms.Schedule(
   process.cleaning,
   process.endjob_step,
   process.RECOoutput_step)
# customisation of the process.

# End of customisation functions

