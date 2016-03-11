# Used CMSSW version: 7_4_14
# Data format: miniaod
# Data type: MC

import sys
if not hasattr(sys, 'argv'):
	sys.argv = ["cmsRun", "runFrameworkMC.py"]

import os
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

### Configurations, that can be changed, are used as variables below.

## Inputs configuration
data = False
isEmbedded = False
globaltag = 'auto:run2_mc_25ns14e33_v4'
outputfilename = "kappaTuple.root"
maxevents = -1

## Needed for configuration of Kappa itself to be able to run it.
centerOfMassEnergy = int(13)
sample_generator = 'madgraph_tauola'
sample_dataset  = 'DYtoMuMu'
sample_process  = 'DYtoMuMu'
sample_scenario = 'DYtoMuMu'
sample_campaign = 'private'
kappaTag = 'KAPPA_2_1_0'

### Configuration

## Define Kappa process
process = cms.Process("KAPPA",eras.Run2_25ns)

## Setting up geometry and magnetic field
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")

## MessageLogger: suppress too much error output
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.default = cms.untracked.PSet(ERROR = cms.untracked.PSet(limit = cms.untracked.int32(5)))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

## technical Kappa configuration

# enable unscheduled mode
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True),
	allowUnscheduled = cms.untracked.bool(True) )

# maximal number of events
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(maxevents))

# global tag
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, globaltag, '')

# source
process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring('file:skimmed_to_reco.root'))

# setting up paths
process.p = cms.Path()
process.ep = cms.EndPath()

# event weight count producer
process.load("Kappa.CMSSW.EventWeightCountProducer_cff")
process.p *= process.nEventsTotal
process.p *= process.nNegEventsTotal

# KappaTuple
process.load('Kappa.Producers.KTuple_cff')
process.kappaTuple = cms.EDAnalyzer('KTuple', process.kappaTupleDefaultsBlock,outputFile = cms.string(outputfilename))
process.kappaTuple.active = cms.vstring()
process.kappaTuple.verbose    = cms.int32(0)
process.kappaTuple.profile    = cms.bool(True)
process.kappaTuple.active = cms.vstring('TreeInfo')
process.kappaTuple.TreeInfo.parameters = cms.PSet(
	dataset               = cms.string(str(sample_dataset)),
	generator             = cms.string(str(sample_generator)),
	productionProcess     = cms.string(str(sample_process)),
	globalTag             = cms.string(globaltag),
	scenario              = cms.string(str(sample_scenario)),
	campaign              = cms.string(str(sample_campaign)),
	kappaTag              = cms.string(kappaTag),
	isEmbedded            = cms.bool(isEmbedded),
	centerOfMassEnergy    = cms.int32(centerOfMassEnergy),
	isData                = cms.bool(data)
)

# Running whole Kappa and writing output
process.kappaOut = cms.Sequence(process.kappaTuple)
process.ep *= process.kappaOut

## general physical configuration

process.kappaTuple.Info.pileUpInfoSource = cms.InputTag("slimmedAddPileupInfo")

process.kappaTuple.active += cms.vstring('VertexSummary')
process.load("Kappa.Skimming.KVertices_cff")
process.goodOfflinePrimaryVertices.src = cms.InputTag('offlineSlimmedPrimaryVertices')
process.p *= (process.makeVertexes)
process.kappaTuple.VertexSummary.whitelist = cms.vstring('offlineSlimmedPrimaryVertices')
process.kappaTuple.VertexSummary.rename = cms.vstring('offlineSlimmedPrimaryVertices => goodOfflinePrimaryVerticesSummary')
process.kappaTuple.VertexSummary.goodOfflinePrimaryVerticesSummary = cms.PSet(src=cms.InputTag("offlineSlimmedPrimaryVertices"))

process.kappaTuple.active += cms.vstring('TriggerObjectStandalone')
process.kappaTuple.TriggerObjectStandalone.bits = cms.InputTag("TriggerResults","","HLTembedding")

process.kappaTuple.active += cms.vstring('BeamSpot')
process.kappaTuple.BeamSpot.offlineBeamSpot = cms.PSet(src = cms.InputTag("offlineBeamSpot"))

process.kappaTuple.active+= cms.vstring('GenInfo')
process.kappaTuple.active+= cms.vstring('GenParticles')
process.kappaTuple.active+= cms.vstring('GenTaus')

process.kappaTuple.GenParticles.genParticles.src = cms.InputTag("prunedGenParticles")
process.kappaTuple.GenTaus.genTaus.src = cms.InputTag("prunedGenParticles")

## Trigger

from Kappa.Skimming.hlt_run2 import hltBlacklist, hltWhitelist
process.kappaTuple.Info.hltWhitelist = hltWhitelist
process.kappaTuple.Info.hltBlacklist = hltBlacklist

## PFCandidates

process.kappaTuple.active += cms.vstring('packedPFCandidates')
process.kappaTuple.packedPFCandidates.packedPFCandidates = cms.PSet(src = cms.InputTag("packedPFCandidates"))

## Muons

process.load("Kappa.Skimming.KMuons_miniAOD_cff")
process.kappaTuple.Muons.muons.src = cms.InputTag("slimmedMuons")
process.kappaTuple.Muons.muons.vertexcollection = cms.InputTag("offlineSlimmedPrimaryVertices")
process.kappaTuple.Muons.muons.srcMuonIsolationPF = cms.InputTag("")
process.kappaTuple.Muons.use03ConeForPfIso = cms.bool(True)
process.kappaTuple.active += cms.vstring('Muons')
process.kappaTuple.Muons.minPt = cms.double(8.0)
process.p *= (process.makeKappaMuons)

## Electrons

process.kappaTuple.active += cms.vstring('Electrons')
process.load("Kappa.Skimming.KElectrons_miniAOD_cff")
process.kappaTuple.Electrons.electrons.src = cms.InputTag("slimmedElectrons")
process.kappaTuple.Electrons.electrons.vertexcollection = cms.InputTag("offlineSlimmedPrimaryVertices")
process.kappaTuple.Electrons.electrons.rhoIsoInputTag = cms.InputTag("slimmedJets", "rho")
process.kappaTuple.Electrons.electrons.allConversions = cms.InputTag("reducedEgamma", "reducedConversions")
from Kappa.Skimming.KElectrons_miniAOD_cff import setupElectrons
process.kappaTuple.Electrons.srcIds = cms.string("standalone");
process.kappaTuple.Electrons.ids = cms.vstring(
	"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto",
	"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose",
	"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium",
	"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight",
	"electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"
)
setupElectrons(process)
process.p *= (process.makeKappaElectrons)

## Taus

process.kappaTuple.active += cms.vstring('PatTaus')
process.kappaTuple.PatTaus.taus.preselectOnDiscriminators = cms.vstring()
process.kappaTuple.PatTaus.taus.binaryDiscrWhitelist = cms.vstring(
	"decayModeFinding",
	"decayModeFindingNewDMs",
	"byLooseCombinedIsolationDeltaBetaCorr3Hits",
	"byMediumCombinedIsolationDeltaBetaCorr3Hits",
	"byTightCombinedIsolationDeltaBetaCorr3Hits",
	"byCombinedIsolationDeltaBetaCorrRaw3Hits",
	"chargedIsoPtSum",
	"neutralIsoPtSum",
	"puCorrPtSum",
	"footprintCorrection",
	"photonPtSumOutsideSignalCone",
	"byLooseIsolationMVArun2v1DBoldDMwLT",
	"byMediumIsolationMVArun2v1DBoldDMwLT",
	"byTightIsolationMVArun2v1DBoldDMwLT",
	"byVTightIsolationMVArun2v1DBoldDMwLT",
	"byLooseIsolationMVArun2v1DBnewDMwLT",
	"byMediumIsolationMVArun2v1DBnewDMwLT",
	"byTightIsolationMVArun2v1DBnewDMwLT",
	"byVTightIsolationMVArun2v1DBnewDMwLT",
	"againstMuonLoose3",
	"againstMuonTight3",
	"againstElectronVLooseMVA6",
	"againstElectronLooseMVA6",
	"againstElectronMediumMVA6",
	"againstElectronTightMVA6",
	"byLooseCombinedIsolationDeltaBetaCorr3HitsdR03",
	"byMediumCombinedIsolationDeltaBetaCorr3HitsdR03",
	"byTightCombinedIsolationDeltaBetaCorr3HitsdR03",
	"byLooseIsolationMVArun2v1DBdR03oldDMwLT",
	"byMediumIsolationMVArun2v1DBdR03oldDMwLT",
	"byTightIsolationMVArun2v1DBdR03oldDMwLT",
	"byVTightIsolationMVArun2v1DBdR03oldDMwLT"
)
process.kappaTuple.PatTaus.taus.floatDiscrWhitelist = process.kappaTuple.PatTaus.taus.binaryDiscrWhitelist

## Jets

process.kappaTuple.active += cms.vstring('PileupDensity')
process.kappaTuple.PileupDensity.pileupDensity = cms.PSet(src=cms.InputTag("fixedGridRhoFastjetAll"))
process.kappaTuple.PileupDensity.whitelist = cms.vstring("fixedGridRhoFastjetAll")
process.kappaTuple.PileupDensity.rename = cms.vstring("fixedGridRhoFastjetAll => pileupDensity")

process.kappaTuple.active += cms.vstring('PatJets')
process.kappaTuple.PatJets.ak4PF = cms.PSet(src=cms.InputTag("slimmedJets"))

## MET

#process.load("Kappa.Skimming.KMET_run2_cff")
#from Kappa.Skimming.KMET_run2_cff import configureMVAMetForMiniAOD
#configureMVAMetForMiniAOD(process)

## Standard MET and GenMet from pat::MET
#process.kappaTuple.active += cms.vstring('PatMET')
#process.kappaTuple.PatMET.met = cms.PSet(src=cms.InputTag("slimmedMETs"))
#process.kappaTuple.PatMET.metPuppi = cms.PSet(src=cms.InputTag("slimmedMETsPuppi"))

## Write MVA MET to KMETs. To check what happens on AOD
#process.kappaTuple.active += cms.vstring('PatMETs')
#process.kappaTuple.PatMETs.metMVAEM = cms.PSet(src=cms.InputTag("metMVAEM"))
#process.kappaTuple.PatMETs.metMVAET = cms.PSet(src=cms.InputTag("metMVAET"))
#process.kappaTuple.PatMETs.metMVAMT = cms.PSet(src=cms.InputTag("metMVAMT"))
#process.kappaTuple.PatMETs.metMVATT = cms.PSet(src=cms.InputTag("metMVATT"))
#process.load('JetMETCorrections.Configuration.JetCorrectionServices_cff')
#process.p *= (process.makeKappaMET)

## TauGenJets

process.load('PhysicsTools/JetMCAlgos/TauGenJets_cfi')
process.load('PhysicsTools/JetMCAlgos/TauGenJetsDecayModeSelectorAllHadrons_cfi')
process.tauGenJets.GenParticles = cms.InputTag("prunedGenParticles")
process.p *= (process.tauGenJets + process.tauGenJetsSelectorAllHadrons)
process.kappaTuple.GenJets.whitelist = cms.vstring("tauGenJets")
process.kappaTuple.GenJets.tauGenJets = cms.PSet(src=cms.InputTag("tauGenJets"))
process.kappaTuple.active += cms.vstring('GenJets')

## Filter Summary

process.nEventsTotal.isMC = cms.bool(True)
process.nNegEventsTotal.isMC = cms.bool(True)
process.nEventsFiltered.isMC = cms.bool(True)
process.nNegEventsFiltered.isMC = cms.bool(True)

process.p *= process.nEventsFiltered
process.p *= process.nNegEventsFiltered
process.kappaTuple.active += cms.vstring('FilterSummary')

