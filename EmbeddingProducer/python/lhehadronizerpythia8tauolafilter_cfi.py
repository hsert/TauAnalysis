import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *


generator = cms.EDFilter("Pythia8HadronizerFilter",
  ExternalDecays = cms.PSet(
    Tauola = cms.untracked.PSet(
      TauolaNoPolar,
      InputCards = cms.PSet(
                pjak1 = cms.int32(1),
                pjak2 = cms.int32(2),
                mdtau = cms.int32(0)
                )
            ),
    parameterSets = cms.vstring('Tauola')
  ),
  maxEventsToPrint = cms.untracked.int32(1),
  nAttempts = cms.uint32(100),
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

ProductionFilterSequence = cms.Sequence(generator)




