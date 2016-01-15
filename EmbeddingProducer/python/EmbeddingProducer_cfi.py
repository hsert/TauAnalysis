import FWCore.ParameterSet.Config as cms


pregenerator = cms.EDProducer("EmbeddingProducer",
				   src = cms.InputTag("patMuonsAfterKinCuts"),
				   vtxSrc = cms.InputTag(
				   "offlineSlimmedPrimaryVertices"
				   #"offlinePrimaryVertices"
				   ),
				   mixHepMc = cms.bool(False),
				   histFileName = cms.string("hist.root")
				  )
