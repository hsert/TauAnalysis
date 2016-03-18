import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *


generator = cms.EDFilter("Pythia8HadronizerFilter",
#  ExternalDecays = cms.PSet(
#    Tauola = cms.untracked.PSet(
#      TauolaPolar,
#      TauolaDefaultInputCards,
#        InputCards = cms.PSet(
#          pjak1 = cms.int32(1),
#          pjak2 = cms.int32(2),
#          mdtau = cms.int32(0)
#        ),
#        parameterSets = cms.vstring('setRadiation'),
#        setRadiation = cms.bool(False)
#    ),
#    parameterSets = cms.vstring('Tauola')
#  ),
  ExternalDecays = cms.PSet(
    Photospp = cms.untracked.PSet(
      parameterSets = cms.vstring('suppressAll','forceBremForBranch'),
      suppressAll = cms.bool(True),
      forceBremForBranch = cms.PSet(
        parameterSets = cms.vstring('TauPlus', 'TauMinus'),
        TauMinus = cms.vint32(0,15),
        TauPlus = cms.vint32(0,-15)
      ),
    ),
    parameterSets = cms.vstring('Photospp')
  ),
  maxEventsToPrint = cms.untracked.int32(1),
  nAttempts = cms.uint32(100),
  HepMCFilter = cms.PSet(
    filterName = cms.string('EmbeddingHepMCFilter'),
    filterParameters = cms.PSet(
#      ElElCut = cms.string("El1.Pt > 20 && El2.Pt > 8 && El1.Eta < 2.4 && El2.Eta < 2.4"),
#      MuMuCut = cms.string("Mu1.Pt > 15 && Mu2.Pt > 6 && Mu1.Eta < 2.4 && Mu2.Eta < 2.4"),

#      HadHadCut = cms.string("Had1.Pt > 30 && Had2.Pt > 30  && Had1.Eta < 2.1 && Had2.Eta < 2.1"),
      ElMuCut = cms.string("(El.Pt > 11 && El.Eta < 2.5 && Mu.Pt > 16 && Mu.Eta < 2.4) || (El.Pt > 16 && El.Eta < 2.5 && Mu.Pt > 8 && Mu.Eta < 2.4"),
#      ElHadCut = cms.string("El.Pt > 22 && El.Eta < 2.1 && Had.Pt > 10 && Had.Eta < 2.3"),
#      MuHadCut = cms.string("Mu.Pt > 17 && Mu.Eta < 2.1 && Had.Pt > 10 && Had.Eta < 2.3"),
      ElElCut = cms.string(""), HadHadCut = cms.string(""), ElHadCut = cms.string(""), MuHadCut = cms.string(""), MuMuCut = cms.string(""),
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
#        '15:onIfAny = 11 13',
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




