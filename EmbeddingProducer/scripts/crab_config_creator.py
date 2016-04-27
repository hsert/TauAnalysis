#! /usr/bin/env python

import os
import stat

class single_crab_workflow():
	
	def __init__(self, skimfileabspath, generatorfileabspath):
		
		print "Initializing crab workflow file. Given absolute paths:"
		print "Skim file: ", skimfileabspath
		print "Generator file: ", generatorfileabspath
		# setting used paths and standard names
		self.cmssw_path = os.environ.get('CMSSW_BASE')
		if self.cmssw_path is None:
			raise EnvironmentError('Set CMSSW environment.')
		self.embedding_path = self.cmssw_path + '/src/TauAnalysis/EmbeddingProducer'
		self.template_path = self.embedding_path + '/templates'
		self.skimming_path = self.embedding_path + '/python/Skimming'
		self.generator_path = self.embedding_path + '/python/ZTauTauGeneration'
		
		self.stdjobfolderfilename = "ZTAUTAU_KAPPA_FROM_CMSSW_7_6_3_patch2_76X_"
		self.skimfileabspath = skimfileabspath
		self.generatorfileabspath = generatorfileabspath
		
		# reading templates
		self.shtemplate = ""
		try:
			shfilein = open(self.template_path + '/crab_workflow_template.sh.txt', 'r')
			self.shtemplate = shfilein.read()
			shfilein.close()
		except IOError: print 'IOError: Generator template does not exist. Please define it as {TEMPLATE_PATH}'.format(TEMPLATE_PATH=self.template_path + '/crab_workflow_template.sh.txt')
		
		self.pytemplate = ""
		try:
			pyfilein = open(self.template_path + '/crab_workflow_template.py.txt', 'r')
			self.pytemplate = pyfilein.read()
			pyfilein.close()
		except IOError: print 'IOError: Generator template does not exist. Please define it as {TEMPLATE_PATH}'.format(TEMPLATE_PATH=self.template_path + '/crab_workflow_template.py.txt')
		
		# setting default values for the switches in the templates
		self.randomserviceswitch = False
		self.cfiswitch = False
		self.testrunswitch = False
		
		# setting default skim filename and folder
		self.stdfilename = "crab_workflow_test"
		self.fileoutfolder = self.embedding_path + '/test'
		self.shfileoutname = self.fileoutfolder + '/' + self.stdfilename + '.sh'
		self.pyfileoutname = self.fileoutfolder + '/' + self.stdfilename + '.py'
		
		# setting default template arguments
		
		self.globaltag = "76X_mcRun2_asymptotic_v12"
		self.datasetpath = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM"
		self.jobfoldername = self.stdjobfolderfilename + "test"
		self.crabworkflowfilename = os.path.relpath(self.shfileoutname,self.fileoutfolder)
		self.skimfilepath = os.path.relpath(self.skimfileabspath,self.fileoutfolder)
		self.generatorfilepath = os.path.relpath(self.generatorfileabspath, self.generator_path)
	
	def set_crab_workflow(self,
		randomserviceswitch=None,
		cfiswitch=None,
		testrunswitch=None,
		fileoutfolder=None,
		fileoutname=None,
		globaltag=None,
		datasetpath=None,
		jobfoldernamepostfix=None
	):
		
		print "Changing settings for crab workflow file."
		self.randomserviceswitch = self.randomserviceswitch if randomserviceswitch is None else randomserviceswitch
		self.cfiswitch = self.cfiswitch if cfiswitch is None else cfiswitch
		self.testrunswitch = self.testrunswitch if testrunswitch is None else testrunswitch
		self.globaltag = self.globaltag if globaltag is None else globaltag
		self.datasetpath = self.datasetpath if datasetpath is None else datasetpath
		self.jobfoldername = self.jobfoldername if jobfoldernamepostfix is None else self.stdjobfolderfilename + jobfoldernamepostfix
		if not fileoutfolder is None:
			self.fileoutfolder = self.embedding_path + '/' + fileoutfolder
		self.skimfilepath = os.path.relpath(self.skimfileabspath,self.fileoutfolder)
		if not fileoutname is None:
			self.shfileoutname = self.fileoutfolder + '/' + fileoutname + '.sh'
			self.pyfileoutname = self.fileoutfolder + '/' + fileoutname + '.py'
		self.crabworkflowfilename = os.path.relpath(self.shfileoutname,self.fileoutfolder)
		
		self.shtemplate = self.shtemplate.format(
			CFISWITCH = "" if self.cfiswitch else "#",
			RANDOMSERVICESWITCH = "" if self.randomserviceswitch else "#",
			GLOBALTAG = self.globaltag,
			GENERATORFILEPATH = self.generatorfilepath
		)
		
		self.pytemplate = self.pytemplate.format(
			TESTRUNSWITCH = "" if self.testrunswitch else "#",
			JOBFOLDERNAME = self.jobfoldername,
			DATASETPATH = self.datasetpath,
			CRABWORKFLOWFILENAME = self.crabworkflowfilename,
			SKIMFILEPATH = self.skimfilepath
		)
	
	def save_crab_workflow(self):
		
		# saving crab workflow files
		if not os.path.exists(self.fileoutfolder):
			os.makedirs(self.fileoutfolder)
		
		shfileout = open(self.shfileoutname, 'w')
		shfileout.write(self.shtemplate)
		print "Saving crab workflow shell file as {FILEOUTNAME}".format(FILEOUTNAME=self.shfileoutname)
		shfileout.close()
		
		pyfileout = open(self.pyfileoutname, 'w')
		# or S_IXGRP or S_IXOTH
		pyfileout.write(self.pytemplate)
		print "Saving crab workflow python file as {FILEOUTNAME}".format(FILEOUTNAME=self.pyfileoutname)
		pyfileout.close()
		
		os.chmod(self.shfileoutname, 0755)
		print "Enabling execution rights for {FILEOUTNAME}".format(FILEOUTNAME=self.shfileoutname)
	
	def print_crab_workflow_settings(self):
		
		print
		print "---------Current settings---------"
		print "CFI switch: ", self.cfiswitch
		print "Random service switch: ", self.randomserviceswitch
		print "Test run switch: ", self.testrunswitch
		print "relative generator file path: ", self.generatorfilepath
		print "relative skim file path: ", self.skimfilepath
		print "DBS dataset path: ", self.datasetpath
		print "Job folder name: ", self.jobfoldername
		print "Global tag: ", self.globaltag
		print "Output folder: ", self.fileoutfolder
		print "Output file name of .sh file: ", self.shfileoutname
		print "Output file name of .py file: ", self.pyfileoutname
		print "----------------------------------"
		print

if __name__ == "__main__":
	
	def perform_skim_creation(fsrmode, formatname, inputfile, globaltag, fileoutfolder, fileoutname):
		skim = single_skim()
		skim.set_skim(fsrmode=fsrmode, formatname=formatname, inputfile=inputfile, globaltag=globaltag)
		skim.save_skim(fileoutfolder=fileoutfolder, fileoutname=fileoutname)
		skim.print_skim_settings()
		return skim
	
	def perform_gen_creation(externaldecay, active_decaychannels, nattempts, muonembedding, fileoutfolder, fileoutname):
		gen = single_gen()
		gen.set_gen(externaldecay=externaldecay, active_decaychannels=active_decaychannels, nattempts=nattempts, muonembedding=muonembedding)
		gen.save_gen(fileoutfolder=fileoutfolder, fileoutname=fileoutname)
		gen.print_gen_settings()
		return gen
	
	def perform_crab_workflow_creation(
		skim,
		gen,
		cfiswitch,
		randomserviceswitch,
		testrunswitch,
		datasetpath,
		globaltag,
		fileoutfolder,
		fileoutname
	):
		
		crab_workflow = single_crab_workflow(skimfileabspath=skim.fileoutname, generatorfileabspath=gen.fileoutname)
		jobfoldernamepostfix = os.path.relpath(skim.fileoutname,skim.fileoutfolder).replace(".py","") + "_" + os.path.relpath(gen.fileoutname,gen.fileoutfolder).replace("_cfi.py","")
		fileoutname = crab_workflow.stdfilename + '_' + jobfoldernamepostfix if fileoutname is None else fileoutname + '_' + jobfoldernamepostfix 
		crab_workflow.set_crab_workflow(
			randomserviceswitch=randomserviceswitch,
			cfiswitch=cfiswitch,
			testrunswitch=testrunswitch,
			fileoutfolder=fileoutfolder,
			fileoutname=fileoutname,
			globaltag=globaltag,
			datasetpath=datasetpath,
			jobfoldernamepostfix=jobfoldernamepostfix
		)
		crab_workflow.save_crab_workflow()
		crab_workflow.print_crab_workflow_settings()

		return crab_workflow
	
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--globaltag', default=None, help='Global tag of the input file and sample production.')
	parser.add_argument('--outputfolder', default=None, help='Name of the output folder used for all templates.')

	skimgroup = parser.add_argument_group('skim options')
	skimgroup.add_argument('--inputfile', default=None, help='Input file for ZToMuMu selection.')
	skimgroup.add_argument('--format', default=None, help='Format of the input file. Possible values: "miniaod", "reco".')
	skimgroup.add_argument('--fsrmodes', default=[], nargs = '+', help='Defines, whether final state radiation should be studied on generator level and if it is the case, which state of the muon should be taken. Possible values: "afterFSR", "beforeFSR", "". ')
	skimgroup.add_argument('--skimoutputfilename', default=None, help='Name of the skim output file.')

	gengroup = parser.add_argument_group('generator options')
	gengroup.add_argument('--decaychannels', default=[], nargs = '+', help='Defines, which set of decay channels of the ditau system should simulated and tested. If multiple channels are in a set, then separate them by comma in the string. Possible values: "EE","MM","TT","EM","ET","MT","ALL".')
	gengroup.add_argument('--externaldecays', default=[], nargs = '+', help='Defines additional generators that should enabled within pythia8 hadronizer. Possible values: "photospp".')
	gengroup.add_argument('--nattempts', default=None, type=int, help="Number of attempts for the filter that is tested.")
	gengroup.add_argument('--muonembedding', default=None, action='store_true', help='Enables muon embedding.')
	gengroup.add_argument('--genoutputfilename', default=None, help='Name of the generator output file.')
	
	crabgroup = parser.add_argument_group('crab workflow options')
	crabgroup.add_argument('--cfiswitch', default=None, action='store_true', help='Decides, whether cfi crab fix in the .sh file should be used. Needed for jobs running on the grid.')
	crabgroup.add_argument('--randomserviceswitch', default=None, action='store_true', help='Decides, whether a random seed for generators should be used.')
	crabgroup.add_argument('--testrunswitch', default=None, action='store_true', help='Desides, whether a grid testrun for the crab config should be done.')
	crabgroup.add_argument('--craboutputfilename', default=None, help='Name of the crab workflow output files without their extensions ".py" and ".sh".')
	crabgroup.add_argument('--datasetpath', default=None, help='Name of the DBS dataset, that should be used for input on grid.')
	
	args = parser.parse_args()
	
	shellscriptcontent = ""
	shellscriptfilepath = ""
	
	from skim_creator import single_skim
	from gen_creator import single_gen
	if len(args.fsrmodes) == 0: args.fsrmodes = [None]
	for fsrmode in args.fsrmodes:
		skim = perform_skim_creation(fsrmode=fsrmode, formatname = args.format, inputfile = args.inputfile, globaltag = args.globaltag, fileoutfolder = args.outputfolder, fileoutname = args.skimoutputfilename)
		if len(args.decaychannels) == 0: args.decaychannels = [None]
		for dcs in args.decaychannels:
			if type(dcs) is str:
				if "ALL" in dcs: dcs = "EE,MM,TT,EM,ET,MT"
				dcs = dcs.split(",")
			if len(args.externaldecays) == 0: args.externaldecays = [None]
			for extd in args.externaldecays:
				gen = perform_gen_creation(
					externaldecay = extd,
					active_decaychannels = dcs,
					nattempts = args.nattempts,
					muonembedding = args.muonembedding,
					fileoutfolder = args.outputfolder,
					fileoutname = args.genoutputfilename
				)
				crab_workflow = perform_crab_workflow_creation(
					skim=skim,
					gen=gen,
					cfiswitch=args.cfiswitch,
					randomserviceswitch=args.randomserviceswitch,
					testrunswitch=args.testrunswitch,
					datasetpath=args.datasetpath,
					globaltag=args.globaltag,
					fileoutfolder=args.outputfolder,
					fileoutname=args.craboutputfilename
				)
				if shellscriptfilepath == "": shellscriptfilepath = crab_workflow.fileoutfolder + '/jobshellscript.sh'
				shellscriptcontent += "crab submit --proxy $X509_USER_PROXY {CRABWORKFLOW}\n".format(CRABWORKFLOW = crab_workflow.pyfileoutname)
	shellscript = open(shellscriptfilepath, 'w')
	shellscript.write(shellscriptcontent)
	shellscript.close()
	print "Saving job shell script as {FILEOUTNAME}".format(FILEOUTNAME=shellscriptfilepath)
	os.chmod(shellscriptfilepath, 0755)
	print "Enabling execution rights for {FILEOUTNAME}".format(FILEOUTNAME=shellscriptfilepath)
	print "Be sure, that CMSSW and crab3 are initialized correctly, VOMS proxy is set the $CMMSW_BASE/src folder is compiled with scram. This is required to run this shell script correctly."
	
