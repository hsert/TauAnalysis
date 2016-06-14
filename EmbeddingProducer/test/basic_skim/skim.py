# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: RECO -s RAW2DIGI,L1Reco,RECO,ALCA:TkAlZMuMu+MuAlCalIsolatedMu+MuAlOverlaps+MuAlZMuMu+DtCalib,EI,PAT,DQM:@standardDQM+@miniAODDQM --runUnscheduled --data --scenario pp --conditions 76X_dataRun2_v15 --eventcontent RECO,AOD,MINIAOD,DQM --datatier RECO,AOD,MINIAOD,DQMIO --customise Configuration/DataProcessing/RecoTLR.customiseDataRun2Common_25ns --filein DoubleMuonData2015RAW.root -n 100 --no_exec --python_filename=reco_Run2015D_DoubleMuon.py --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('SKIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.AlCaRecoStreams_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('DQMOffline.Configuration.DQMOffline_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(30)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:DoubleMuon2015DRAWPicked.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('SKIM nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAOD'),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('RAWskimmed.root'),
    outputCommands = process.MINIAODEventContent.outputCommands,
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("skimming")),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

process.MINIAODoutput.outputCommands.extend(cms.untracked.vstring(
	"keep *_*_*_LHC",
	"keep *_*_*_HLT",

	"drop *_*_*_SKIM",
	# muon collections considered for selection and LHE product
	"keep *_patMuonsAfterID_*_SKIM",
	"keep *_slimmedMuons_*_SKIM",
	"keep *_selectedMuonsForEmbedding_*_SKIM",

	# collections manipulated later by cleaning
	"keep *_siPixelClusters_*_SKIM",
	"keep *_siStripClusters_*_SKIM",
	"keep *_dt1DRecHits_*_SKIM",
	"keep *_csc2DRecHits_*_SKIM",
	"keep *_rpcRecHits_*_SKIM",
	
	# keep vertex collection for later LHEEventProduct creation
	"keep recoVertexs_offlineSlimmedPrimaryVertices_*_SKIM"
))

process.MINIAODoutput.outputCommands.extend(process.RecoMuonRECO.outputCommands)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v15', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.dqmoffline_step = cms.Path(process.DQMOffline)
process.dqmoffline_1_step = cms.Path(process.DQMOfflineMiniAOD)
process.MINIAODoutput_step = cms.EndPath(process.MINIAODoutput)

process.load('TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff')
process.patMuonsAfterKinCuts.src = cms.InputTag("slimmedMuons","","SKIM")
process.patMuonsAfterID = process.patMuonsAfterLooseID.clone()

process.skimming = cms.Path(process.makePatMuonsZmumuSelection)

# Schedule definition
process.schedule = cms.Schedule(
	process.raw2digi_step,
	process.L1Reco_step,
	process.reconstruction_step,
	process.pathALCARECOMuAlCalIsolatedMu,
	process.pathALCARECOTkAlZMuMu,
	process.pathALCARECOMuAlOverlaps,
	process.pathALCARECOMuAlZMuMu,
	process.pathALCARECODtCalib,
	process.eventinterpretaion_step,
	process.Flag_HBHENoiseFilter,
	process.Flag_HBHENoiseIsoFilter,
	process.Flag_CSCTightHaloFilter,
	process.Flag_CSCTightHaloTrkMuUnvetoFilter,
	process.Flag_CSCTightHalo2015Filter,
	process.Flag_HcalStripHaloFilter,
	process.Flag_hcalLaserEventFilter,
	process.Flag_EcalDeadCellTriggerPrimitiveFilter,
	process.Flag_EcalDeadCellBoundaryEnergyFilter,
	process.Flag_goodVertices,
	process.Flag_eeBadScFilter,
	process.Flag_ecalLaserCorrFilter,
	process.Flag_trkPOGFilters,
	process.Flag_chargedHadronTrackResolutionFilter,
	process.Flag_muonBadTrackFilter,
	process.Flag_trkPOG_manystripclus53X,
	process.Flag_trkPOG_toomanystripclus53X,
	process.Flag_trkPOG_logErrorTooManyClusters,
	process.Flag_METFilters,
	process.dqmoffline_step,
	process.dqmoffline_1_step,
	process.skimming,
	process.MINIAODoutput_step
)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.RecoTLR
from Configuration.DataProcessing.RecoTLR import customiseDataRun2Common_25ns 

#call to customisation function customiseDataRun2Common_25ns imported from Configuration.DataProcessing.RecoTLR
process = customiseDataRun2Common_25ns(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PAT_cff')
from FWCore.ParameterSet.Utilities import cleanUnscheduled
process=cleanUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllData 

#call to customisation function miniAOD_customizeAllData imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllData(process)

# End of customisation functions
