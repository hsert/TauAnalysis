import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *


generator = cms.EDFilter("Pythia8HadronizerFilter",
#  ExternalDecays = cms.PSet(
#    Tauola = cms.untracked.PSet(
#      TauolaPolar,
#      TauolaDefaultInputCards
#    ),
#    parameterSets = cms.vstring('Tauola')
#  ),
  maxEventsToPrint = cms.untracked.int32(1),
  nAttempts = cms.uint32(10000),
  HepMCFilter = cms.PSet(
    filterName = cms.string('EmbeddingHepMCFilter'),
    filterParameters = cms.PSet(
      ElElCut = cms.string("El1.Pt > 22 && El2.Pt > 10 && El1.Eta < 2.4 && El2.Eta < 2.4"),
      MuMuCut = cms.string("Mu1.Pt > 17 && Mu2.Pt > 8 && Mu1.Eta < 2.4 && Mu2.Eta < 2.4"),
      HadHadCut = cms.string("Had1.Pt > 40 && Had2.Pt > 40  && Had1.Eta < 2.1 && Had2.Eta < 2.1"),
      ElMuCut = cms.string("(El.Pt > 13 && El.Eta < 2.5 && Mu.Pt > 18 && Mu.Eta < 2.4) || (El.Pt > 18 && El.Eta < 2.5 && Mu.Pt > 10 && Mu.Eta < 2.4"),
      ElHadCut = cms.string("El.Pt > 24 && El.Eta < 2.1 && Had.Pt > 20 && Had.Eta < 2.3"),
      MuHadCut = cms.string("Mu.Pt > 19 && Mu.Eta < 2.1 && Had.Pt > 20 && Had.Eta < 2.3"),
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
        'Init:showChangedParticleData = off',
        '15:onMode = off',
        '15:onPosIfAny = 11',
        '15:onNegIfAny = -13'
    ),
    parameterSets = cms.vstring('pythia8CommonSettings',
                                'pythia8CUEP8M1Settings',
                                'processParameters',
                                )
    )
)

ProductionFilterSequence = cms.Sequence(generator)




