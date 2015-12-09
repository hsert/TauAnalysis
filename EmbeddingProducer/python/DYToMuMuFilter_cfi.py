import FWCore.ParameterSet.Config as cms


dYToMuMuFilter = cms.EDFilter("DYToMuMuFilter", 
                              inputTag = cms.InputTag("genParticles"))
