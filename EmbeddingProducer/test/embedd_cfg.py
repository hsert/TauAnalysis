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
    input = cms.untracked.int32(300)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/A8586143-EB6E-E511-8546-0025905B85B2.root'),
    secondaryFileNames = cms.untracked.vstring(),
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    inputCommands = cms.untracked.vstring('keep *', 
       'drop *_*_*_LHE',
       )
)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('embedding.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Path and EndPath definitions
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.p,process.RECOSIMoutput_step)


# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '74X_mcRun2_asymptotic_AllChannelsGood_v0', '')

process.RECOSIMoutput.outputCommands.extend(
    cms.untracked.vstring("drop * ",
                          "keep *_*_*_EMBS"
      ))


process.load("TauAnalysis.EmbeddingProducer.cmsDriver_fragments.DYToMuMuGenFilter_cff")
process.load("TauAnalysis.EmbeddingProducer.cmsDriver_fragments.MuonPairSelector_cff")

process.p *= (process.dYToMuMuGenFilter * process.makePatMuonsZmumu)

#process.generator = cms.EDFilter("Pythia8EmbeddingGun",
#				  PythiaParameters = cms.PSet(
#				      py8Settings = cms.vstring(''),
#				      parameterSets = cms.vstring('py8Settings')
#				    ),
#				      PGunParameters = cms.PSet(
#					ParticleID = cms.vint32(521),
 #                                       AddAntiParticle = cms.bool(False),
#                                        MinPhi = cms.double(-3.14159265359),
#                                        MaxPhi = cms.double(3.14159265359),
#                                        MinE = cms.double(100.0),
#                                        MaxE = cms.double(200.0),
#                                        MinEta = cms.double(0.0),
#                                        MaxEta = cms.double(2.4)
#				      ),
				  
			#	   src = cms.InputTag("goodMuonsFormumuSelection"),
			#	   mixHepMc = cms.bool(False)
#)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *


#process.load("GeneratorInterface/LHEInterface/ExternalLHEProducer_cfi")


process.externalLHEProducer = cms.EDProducer("EmbeddingLHEProducer",
				src = cms.InputTag("patMuonsAfterMediumID"),
				switchToMuonEmbedding = cms.bool(False),
				mirroring = cms.bool(False)
				)


process.p *= process.externalLHEProducer

from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *


pythia8CommonSettingsBlock.pythia8CommonSettings.extend(cms.untracked.vstring('Init:showChangedSettings = off', 'Init:showChangedParticleData = off', 'Next:numberCount = 0'))

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
#  ExternalDecays = cms.PSet(
#    Tauola = cms.untracked.PSet(
#      TauolaPolar,
#      TauolaDefaultInputCards
#    ),
#    parameterSets = cms.vstring('Tauola')
#  ),
  maxEventsToPrint = cms.untracked.int32(1),
  nAttempts = cms.uint32(10),
  HepMCFilter = cms.PSet(
    filterName = cms.string('EmbeddingHepMCFilter'),
    filterParameters = cms.PSet(
      ElElCut = cms.string("El1.Pt > 22 && El2.Pt > 10"),
      MuMuCut = cms.string("Mu1.Pt > 17 && Mu2.Pt > 8"),
      HadHadCut = cms.string("Had1.Pt > 35 && Had2.Pt > 30"),
      ElMuCut = cms.string("(El.Pt > 21 && Mu.Pt > 10) || (El.Pt > 10 && Mu.Pt > 21)"),
      ElHadCut = cms.string("El.Pt > 28 && Had.Pt > 25"),
      MuHadCut = cms.string("Mu.Pt > 18 && Had.Pt > 25 && Mu.Eta < 2.1"),
      switchToMuonEmbedding = cms.bool(False)
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
                                'processParameters',
    )
  )
)







process.p *=process.generator


# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
#from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
#process = addMonitoring(process)

# End of customisation functions

