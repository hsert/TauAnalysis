# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: TauAnalysis/MCEmbeddingTools/python/ZmumuStandaloneSelection_cff --filein=file:step2.root --fileout=skimmed.root --python_filename=skim.py --eventcontent=RECOSIM --conditions MCRUN2_74_V9A --step NONE --magField 38T_PostLS1 --customise TauAnalysis/MCEmbeddingTools/setDefaults.setDefaults --customise TauAnalysis/MCEmbeddingTools/ZmumuStandaloneSelectionAll --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --no_exec -n -1
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process('EMBS',eras.Run2_25ns)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


#process.load('HLTrigger.HLTanalyzers.hltTrigReport_cfi')
#process.embedTrigReport = process.hltTrigReport.clone()
#process.p *= process.embedTrigReport

#process.MessageLogger = cms.Service("MessageLogger",
#                                    destinations   = cms.untracked.vstring('trigger_messages.txt'),
#                                    statistics     = cms.untracked.vstring('statistics1'),   
#                                    statistics1 = cms.untracked.PSet(threshold = cms.untracked.string('DEBUG')                                                                     ),
#                                    )


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(300)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    #'file:/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/A8586143-EB6E-E511-8546-0025905B85B2.root',
    'file:/pnfs/desy.de/cms/tier2/store/data/Run2015D/DoubleMuon/RECO/16Dec2015-v1/10000/2A27197B-2CA7-E511-9C08-A0369F7FC0BC.root'
    #"file:step2.root"
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('skimmed_both.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)
    
process.RECOSIMoutput.outputCommands.extend(
    cms.untracked.vstring("drop * ",
			  "keep LHEEventProduct_*_*_*",
			  "keep LHERunInfoProduct_*_*_*",
                          "keep *_*_*_EMBS",
                         # "keep *_*_*_LHE"
      ))

# Path and EndPath definitions

#Path declaration, the proper definition is done in the customise functions
process.muonsLooseID = cms.Path()
process.muonsMediumID = cms.Path()
process.muonsTightID = cms.Path()

#Needed as formalism to define paths as trigger paths 
process.hltTriggerType = cms.EDFilter("HLTTriggerTypeFilter",
    SelectedTriggerType = cms.int32(1)
)

process.load("TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff")

process.hltBoolEnd = cms.EDFilter( "HLTBool",
        result = cms.bool( True )
    )

process.externalLHEProducer = cms.EDProducer("EmbeddingLHEProducer",
				src = cms.InputTag("patMuonsAfterID","","EMBS"),
				switchToMuonEmbedding = cms.bool(False),
				mirroring = cms.bool(False)
				)


process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.RECOSIMoutput_step)


# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '74X_mcRun2_asymptotic_AllChannelsGood_v0', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_hlt_25ns14e33_v4', '')

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

from TauAnalysis.EmbeddingProducer.customisers import customiseMuonInputForMiniAOD, customiseMuonInputForRECO

#process = customiseMuonInputForMiniAOD(process)
process = customiseMuonInputForRECO(process)

# End of customisation functions

