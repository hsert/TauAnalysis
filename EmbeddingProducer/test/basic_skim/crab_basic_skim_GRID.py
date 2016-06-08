from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

##-- Your name of the crab project
config.General.requestName = 'BASIC_SKIM_TEST_CMSSW_7_6_4_GRID'
config.General.workArea = 'crab_projects'

##-- Transfer root files as well as log files "cmsRun -j FrameworkJobReport.xml" (log file = FrameworkJobReport.xml)
config.General.transferOutputs = True
config.General.transferLogs = False

##-- We want to have the special dcms role (better fair share at german grid sites). 
config.User.voGroup = 'dcms'

##-- the scripts (Analysis means with EDM input) which are executed. psetName is the cmsRun config and scriptExe is a shell config which should include "cmsRun -j FrameworkJobReport.xml -p PSet.py" (PSet.py is the renamed config.JobType.psetName)
config.JobType.pluginName = 'Analysis'
config.JobType.sendPythonFolder = True
config.JobType.psetName = 'skim.py'
config.JobType.maxJobRuntimeMin = 2700
config.JobType.maxMemoryMB = 2500

##-- instead of taking the outputfile per hand use the result of pset.py and renamed it, which cheat on the test of is an EDM file test and allows to use publish the data 
config.JobType.disableAutomaticOutputCollection = True
config.JobType.outputFiles = ['RAWskimmed.root']

##-- The dataset you want to process:

config.Data.inputDataset = '/DoubleMuon/Run2015D-v1/RAW'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

##-- If you want to run test jobs set totalUnits to a small number and publication to false
#config.Data.totalUnits = 1
config.Data.publication = True

##-- the output strorage element
config.Site.storageSite = 'T2_DE_DESY'
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())

##-- Run in xrootd mode (which allows you to run the jobs on all possible sites) 
config.Data.ignoreLocality = True
config.Site.whitelist = ['T2_CH_CERN','T2_DE_DESY','T1_DE_KIT','T2_DE_RWTH','T2_UK_London_IC','T2_US_MIT']
