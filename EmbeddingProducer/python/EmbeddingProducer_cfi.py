import FWCore.ParameterSet.Config as cms


pregenerator = cms.EDProducer("EmbeddingProducer",
				   src = cms.InputTag("patMuonsAfterKinCuts"),
				   mixHepMc = cms.bool(False),
				   histFileName = cms.string("hist.root")
				  )
