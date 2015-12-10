import FWCore.ParameterSet.Config as cms



from TauAnalysis.EmbeddingProducer.DYToMuMuGenFilter_cfi import *



genmuonFilterSequence= cms.Sequence(
    dYToMuMuGenFilter
    ) 
