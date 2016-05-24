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
    input = cms.untracked.int32(20)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'root://cmsxrootd.gridka.de///store/data/Run2015D/DoubleMuon/RECO/16Dec2015-v1/10008/7E2D53A5-18A7-E511-BBF9-C4346BBF3E78.root'
#'file:cloned_Run2105.root'
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
    fileName = cms.untracked.string('file:cleaned.root'),
    #outputCommands = process.RECOEventContent.outputCommands,
    outputCommands = cms.untracked.vstring("keep * ",
    "drop *_siPixelClusters_*_RECO",
    "drop *_siStripClusters_*_RECO",
    "drop *_siStripClusters_*_RECO",
    "drop *_dt1DRecHits_*_RECO",
    "drop *_csc2DRecHits_*_RECO",
    "drop *_rpcRecHits_*_RECO",
    "drop *_*_*_CLEANING",
    "keep *_siPixelClusters_*_CLEANING",
    "keep *_siStripClusters_*_CLEANING",
    "keep *_siStripClusters_*_CLEANING",
    "keep *_dt1DRecHits_*_CLEANING",
    "keep *_csc2DRecHits_*_CLEANING",
    "keep *_rpcRecHits_*_CLEANING",
    ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("inputPathAndCleaning")),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v15', '')


#process.siStripClusters  = cms.EDProducer('MuonCleaner',
process.siPixelClusters = cms.EDProducer('PixelCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","CLEANING"),
        pixelClusters = cms.InputTag("siPixelClusters","","RECO")
)

process.siStripClusters = cms.EDProducer('StripCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","CLEANING"),
	stripClusters = cms.InputTag("siStripClusters","","RECO"),
)

process.dt1DRecHits = cms.EDProducer('DTCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","CLEANING"),
	oldCollection = cms.InputTag("dt1DRecHits","","RECO"),
)

process.csc2DRecHits = cms.EDProducer('CSCCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","CLEANING"),
	oldCollection  = cms.InputTag("csc2DRecHits","","RECO"),
)

process.rpcRecHits = cms.EDProducer('RPCleaner',
	MuonCollection = cms.InputTag("patMuonsAfterID","","CLEANING"),
	oldCollection  = cms.InputTag("rpcRecHits","","RECO"),
)


# Path and EndPath definitions

# Selection of muons from input
from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cff import patMuons, makePatMuons, muonMatch

patMuons.addGenMatch = cms.bool(False)
patMuons.embedGenMatch = False
patMuons.genParticleMatch = ''
patMuons.embedCaloMETMuonCorrs = cms.bool(False)
patMuons.embedTcMETMuonCorrs = cms.bool(False)
makePatMuons.remove(muonMatch)

process.load('TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff')
process.patMuonsAfterKinCuts.src = cms.InputTag("patMuons")
process.patMuonsAfterID = process.patMuonsAfterLooseID.clone()

process.inputPathAndCleaning = cms.Path(process.makePatMuonsZmumuSelection)
process.inputPathAndCleaning.replace(process.doubleMuonHLTTrigger, process.doubleMuonHLTTrigger + makePatMuons)
process.inputPathAndCleaning *= process.siPixelClusters
process.inputPathAndCleaning *= process.siStripClusters
process.inputPathAndCleaning *= process.dt1DRecHits
process.inputPathAndCleaning *= process.dt2DSegments
process.inputPathAndCleaning *= process.csc2DRecHits
process.inputPathAndCleaning *= process.rpcRecHits

process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)

# Schedule definition

process.schedule = cms.Schedule(
   process.inputPathAndCleaning,
   process.endjob_step,
   process.RECOoutput_step)
# customisation of the process.

# End of customisation functions

