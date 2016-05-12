import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *


generator = cms.EDFilter("Pythia8HadronizerFilter",
  
  maxEventsToPrint = cms.untracked.int32(1),
  nAttempts = cms.uint32(1000),
  HepMCFilter = cms.PSet(
    filterName = cms.string('EmbeddingHepMCFilter'),
    filterParameters = cms.PSet(
      
      
      
      
      
      MuHadCut = cms.untracked.string("Mu.Pt > 17 && Mu.Eta < 2.1 && Had.Pt > 10 && Had.Eta < 2.3"),
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
                                'processParameters'
                                )
    )
)

ProductionFilterSequence = cms.Sequence(generator)




