# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: TauAnalysis/MCEmbeddingTools/python/ZmumuStandaloneSelection_cff --filein=file:step2.root --fileout=skimmed.root --python_filename=skim.py --eventcontent=RECOSIM --conditions MCRUN2_74_V9A --step NONE --magField 38T_PostLS1 --customise TauAnalysis/MCEmbeddingTools/setDefaults.setDefaults --customise TauAnalysis/MCEmbeddingTools/ZmumuStandaloneSelectionAll --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --no_exec -n -1
import FWCore.ParameterSet.Config as cms

process = cms.Process('EMBS')

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





process.p = cms.Path()


#process.load('HLTrigger.HLTanalyzers.hltTrigReport_cfi')
#process.embedTrigReport = process.hltTrigReport.clone()
#process.p *= process.embedTrigReport

#process.MessageLogger = cms.Service("MessageLogger",
#                                    destinations   = cms.untracked.vstring('trigger_messages.txt'),
#                                    statistics     = cms.untracked.vstring('statistics1'),   
#                                    statistics1 = cms.untracked.PSet(threshold = cms.untracked.string('DEBUG')                                                                     ),
#                                    )


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:step2.root'),
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
    fileName = cms.untracked.string('skimmed.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Path and EndPath definitions
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.p,process.RECOSIMoutput_step)


# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V9A', '')


process.load("TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff")
#process.schedule.insert(0, process.producemumuSelection)
process.p *= process.producemumuSelection
process.RECOSIMoutput.outputCommands.extend(
    cms.untracked.vstring("keep *_goodMuonsFormumuSelection_*_*"))




# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

