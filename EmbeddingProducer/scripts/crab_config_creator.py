#! /usr/bin/env python

import os

class single_crab_config():
	
	def __init__(self, skimfileabspath, shellscriptworkflowfileabspath):
		
		print "Initializing crab config file. Given absolute paths:"
		print "Skim file: ", skimfileabspath
		print "Workflow shell script file: ", shellscriptworkflowfileabspath
		
		# setting used paths and standard names
		self.cmssw_path = os.environ.get('CMSSW_BASE')
		if self.cmssw_path is None:
			raise EnvironmentError('Set CMSSW environment.')
		self.embedding_path = self.cmssw_path + '/src/TauAnalysis/EmbeddingProducer'
		self.template_path = self.embedding_path + '/templates'
		self.skimming_path = self.embedding_path + '/python/Skimming'
		self.shellscriptworkflow_path = self.embedding_path + '/scripts/shellscripts'
		
		self.stdjobfolderfilename = "ZTAUTAU_KAPPA_FROM_CMSSW_7_6_3_patch2_76X_"
		self.stdfilename = "crab_config.py"
		self.skimfileabspath = skimfileabspath
		self.shellscriptworkflowfileabspath = shellscriptworkflowfileabspath
		
		# reading templates
		self.template = ""
		try:
			filein = open(self.template_path + '/crab_config_template.py.txt', 'r')
			self.template = filein.read()
			filein.close()
		except IOError: print 'IOError: Generator template does not exist. Please define it as {TEMPLATE_PATH}'.format(TEMPLATE_PATH=self.template_path + '/crab_config_template.py.txt')
		
		# setting default skim filename and folder
		self.fileoutfolder = self.embedding_path + '/test'
		self.fileoutname = self.fileoutfolder + '/' + 'crab_config_test.py'
		
		# setting default template arguments
		self.version = ""
		self.testrunswitch = False
		self.datasetpath = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM"
		self.jobfoldername = self.stdjobfolderfilename + "test"
		self.shellscriptworkflowfilepath = os.path.relpath(self.shellscriptworkflowfileabspath,self.fileoutfolder)
		self.skimfilepath = os.path.relpath(self.skimfileabspath,self.fileoutfolder)
	
	def set_crab_config(self,
		version=None,
		testrunswitch=None,
		datasetpath=None,
		fileoutfolder=None,
		fileoutname=None,
		jobfoldernamepostfix=None
	):
		
		print "Changing settings for crab workflow file."
		
		self.version = self.version if version is None else '_'+ version
		self.testrunswitch = self.testrunswitch if testrunswitch is None else testrunswitch
		self.datasetpath = self.datasetpath if datasetpath is None else datasetpath
		self.jobfoldername = self.jobfoldername if jobfoldernamepostfix is None else self.stdjobfolderfilename + jobfoldernamepostfix
		if not fileoutfolder is None:
			self.fileoutfolder = self.embedding_path + '/' + fileoutfolder
		self.skimfilepath = os.path.relpath(self.skimfileabspath,self.fileoutfolder)
		if not fileoutname is None:
			self.fileoutname = self.fileoutfolder + '/' + fileoutname
		else:
			self.fileoutname = self.fileoutfolder + '/' + 'crab_config_test.py'
		self.shellscriptworkflowfilepath = os.path.relpath(self.shellscriptworkflowfileabspath,self.fileoutfolder)
		
		self.template = self.template.format(
			VERSION = self.version,
			TESTRUNSWITCH = "" if self.testrunswitch else "#",
			JOBFOLDERNAME = self.jobfoldername,
			DATASETPATH = self.datasetpath,
			SHELLSCRIPTWORKFLOWFILEPATH = self.shellscriptworkflowfilepath,
			SKIMFILEPATH = self.skimfilepath
		)
	
	def save_crab_config(self):
		
		# saving crab workflow files
		if not os.path.exists(self.fileoutfolder):
			os.makedirs(self.fileoutfolder)
		
		fileout = open(self.fileoutname, 'w')
		fileout.write(self.template)
		print "Saving crab config file as {FILEOUTNAME}".format(FILEOUTNAME=self.fileoutname)
		fileout.close()
	
	def print_crab_config_settings(self):
		
		print
		print "---------Current settings---------"
		print "version: ", self.version
		print "Test run switch: ", self.testrunswitch
		print "relative workflow file path: ", self.shellscriptworkflowfilepath
		print "relative skim file path: ", self.skimfilepath
		print "DBS dataset path: ", self.datasetpath
		print "Job folder name: ", self.jobfoldername
		print "Output folder: ", self.fileoutfolder
		print "Output file name of crab config file: ", self.fileoutname
		print "----------------------------------"
		print

if __name__ == "__main__":
	
	from skim_creator import single_skim
	from gen_creator import single_gen
	from embToKappa_workflow_creator import single_embToKappa_workflow
	
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
	
	def perform_embToKappa_workflow_creation(generatorfileabspath, randomserviceswitch, globaltag, correctvtx, fileoutfolder, fileoutname):
		embToKappa_workflow = single_embToKappa_workflow(generatorfileabspath)
		embToKappa_workflow.set_embToKappa_workflow(randomserviceswitch=randomserviceswitch, globaltag=globaltag, correctvtx=correctvtx)
		embToKappa_workflow.save_embToKappa_workflow(fileoutfolder=fileoutfolder, fileoutname=fileoutname)
		embToKappa_workflow.print_embToKappa_workflow_settings()
		return embToKappa_workflow
	
	def perform_crab_config_creation(
		skim,
		gen,
		shellscript,
		version,
		testrunswitch,
		datasetpath,
		fileoutfolder,
		fileoutname
	):
		
		crab_config= single_crab_config(skimfileabspath=skim.fileoutname, shellscriptworkflowfileabspath=shellscript.fileoutname)
		jobfoldernamepostfix = os.path.relpath(skim.fileoutname,skim.fileoutfolder).replace(".py","") + "_" + os.path.relpath(gen.fileoutname,gen.fileoutfolder).replace("_cfi.py","")
		fileoutname = crab_config.stdfilename.replace(".py","") + '_' + jobfoldernamepostfix + ".py" if fileoutname is None else fileoutname.replace(".py","") + '_' + jobfoldernamepostfix + ".py"
		crab_config.set_crab_config(
			version=version,
			testrunswitch=testrunswitch,
			fileoutfolder=fileoutfolder,
			fileoutname=fileoutname,
			datasetpath=datasetpath,
			jobfoldernamepostfix=jobfoldernamepostfix
		)
		crab_config.save_crab_config()
		crab_config.print_crab_config_settings()

		return crab_config
	
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

	workflowgroup = parser.add_argument_group('embedding to kappa workflow options')
	workflowgroup.add_argument('--wfoutputfilename',default=None, help='Name of the embedding to kapppa workflow output file.')
	workflowgroup.add_argument('--randomserviceswitch', default=None, action='store_true', help='Decides, whether a random seed for generators should be used.')
	workflowgroup.add_argument('--correctvtx', default=None, action='store_true', help="Decides, whether vertex in the simulated event should be corrected.")

	crabgroup = parser.add_argument_group('crab config options')
	crabgroup.add_argument('--version', default=None, help='Version of the working area.')
	crabgroup.add_argument('--testrunswitch', default=None, action='store_true', help='Desides, whether a grid testrun for the crab config should be done.')
	crabgroup.add_argument('--craboutputfilename', default=None, help='Name of the crab workflow output files.')
	crabgroup.add_argument('--datasetpath', default=None, help='Name of the DBS dataset, that should be used for input on grid.')
	
	args = parser.parse_args()
	
	shellscriptcontent = ""
	shellscriptfilepath = ""
	
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
				embToKappa_workflow = perform_embToKappa_workflow_creation(
					generatorfileabspath = gen.fileoutname,
					randomserviceswitch=args.randomserviceswitch,
					globaltag=args.globaltag,
					correctvtx = args.correctvtx,
					fileoutfolder=args.outputfolder,
					fileoutname=args.wfoutputfilename
				)
				
				template_path = os.environ.get('CMSSW_BASE') + '/src/TauAnalysis/EmbeddingProducer/templates/crab_workflow_fragment.txt'
				crab_workflow_fragment = open(template_path, 'r')
				workflow_file = open(embToKappa_workflow.fileoutname, 'r')
				wf_for_crab = crab_workflow_fragment.read()+workflow_file.read()
				crab_workflow_fragment.close(),workflow_file.close()
				workflow_file = open(embToKappa_workflow.fileoutname, 'w')
				workflow_file.write(wf_for_crab)
				workflow_file.close()
				
				crab_config = perform_crab_config_creation(
					skim=skim,
					gen=gen,
					shellscript=embToKappa_workflow,
					version=args.version,
					testrunswitch=args.testrunswitch,
					datasetpath=args.datasetpath,
					fileoutfolder=args.outputfolder,
					fileoutname=args.craboutputfilename
				)
				if shellscriptfilepath == "": shellscriptfilepath = crab_config.fileoutfolder + '/jobshellscript.sh'
				shellscriptcontent += "crab submit --proxy $X509_USER_PROXY {CRABWORKFLOW}\n".format(CRABWORKFLOW = crab_config.fileoutname)
	shellscript = open(shellscriptfilepath, 'w')
	shellscript.write(shellscriptcontent)
	shellscript.close()
	print "Saving job shell script as {FILEOUTNAME}".format(FILEOUTNAME=shellscriptfilepath)
	os.chmod(shellscriptfilepath, 0755)
	print "Enabling execution rights for {FILEOUTNAME}".format(FILEOUTNAME=shellscriptfilepath)
	print "Be sure, that CMSSW and crab3 are initialized correctly, VOMS proxy is set the $CMMSW_BASE/src folder is compiled with scram. This is required to run this shell script correctly."
	
