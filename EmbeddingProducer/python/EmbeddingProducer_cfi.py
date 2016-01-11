import FWCore.ParameterSet.Config as cms


pregenerator = cms.EDProducer("EmbeddingProducer",
				   src = cms.InputTag("goodMuonsFormumuSelection"),
				   mixHepMc = cms.bool(False)
				  )