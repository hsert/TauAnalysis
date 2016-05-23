# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: rereco --conditions 76X_dataRun2_v15 --filein file:skimmed.root --fileout file:reco_Run2105.root --step L1Reco,RECO --datatier RECO --era Run2_25ns --eventcontent RECO --no_exec -n -1 --data --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps --python_filename reco_step.py
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO2',eras.Run2_25ns)

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
#'file:/nfs/dust/cms/user/swayand/DO_MU_FILES/DO_MU_MANY_RECO.root'
'file:cloned_Run2105.root'
#'file:skimmed.root'
),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

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
    fileName = cms.untracked.string('file:reco_Run2105.root'),
    #outputCommands = process.RECOEventContent.outputCommands,
    outputCommands = cms.untracked.vstring("keep * ",
					    "drop *_*_*_RECO"
					      ),
    
    
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_dataRun2_v15', '')


#process.siStripClusters  = cms.EDProducer('MuonCleaner',
process.siPixelClusters = cms.EDProducer('PixelCleaner',
	MuonCollection = cms.InputTag("muons"),
        pixelClusters = cms.InputTag("siPixelClusters","","RECO")
)

process.siStripClusters = cms.EDProducer('StripCleaner',
	MuonCollection = cms.InputTag("muons"),
	stripClusters = cms.InputTag("siStripClusters","","RECO"),
)


process.dt1DRecHits = cms.EDProducer('DTCleaner',
	MuonCollection = cms.InputTag("muons","","RECO"),
	oldCollection = cms.InputTag("dt1DRecHits","","RECO"),
)

process.csc2DRecHits = cms.EDProducer('CSCCleaner',
	MuonCollection = cms.InputTag("muons","","RECO"),
	oldCollection  = cms.InputTag("csc2DRecHits","","RECO"),
)

process.rpcRecHits = cms.EDProducer('RPCleaner',
	MuonCollection = cms.InputTag("muons","","RECO"),
	oldCollection  = cms.InputTag("rpcRecHits","","RECO"),
)


# Path and EndPath definitions


process.L1Reco_step = cms.Path(process.L1Reco)

#process.siPixelClustersPreSplitting.src = cms.InputTag("siPixelDigis","","RECO")
process.cleaning = cms.Path(
			    process.siPixelClusters +
			    process.siStripClusters +
			    process.dt1DRecHits + process.dt2DSegments  +
			    process.csc2DRecHits +
			    process.rpcRecHits 
			    )

#process.cleaning = cms.Path(process.siPixelClusters*process.siStripClusters)


process.reconstruction_step = cms.Path(process.reconstruction_fromRECO)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)

# Schedule definition

#process.schedule = cms.Schedule(process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.RECOoutput_step)
process.schedule = cms.Schedule(process.cleaning,process.reconstruction_step,process.endjob_step,process.RECOoutput_step)
# customisation of the process.

# Automatic addition of the customisation function from TauAnalysis.EmbeddingProducer.customisers
from TauAnalysis.EmbeddingProducer.customisers import customiseAllSteps 

#call to customisation function customiseAllSteps imported from TauAnalysis.EmbeddingProducer.customisers
process = customiseAllSteps(process)

# End of customisation functions

