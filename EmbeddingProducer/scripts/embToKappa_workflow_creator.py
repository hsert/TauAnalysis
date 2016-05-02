#! /usr/bin/env python

import os

class single_embToKappa_workflow():
	
	def __init__(self, generatorfileabspath):
		
		print "Initializing embedding to kappa workflow file.  Given absolute paths:"
		print "Generator file: ", generatorfileabspath
		
		# setting used paths
		self.cmssw_path = os.environ.get('CMSSW_BASE')
		if self.cmssw_path is None:
			raise EnvironmentError('Set CMSSW environment.')
		self.embedding_path = self.cmssw_path + '/src/TauAnalysis/EmbeddingProducer'
		self.template_path = self.embedding_path + '/templates'
		self.generator_path = self.embedding_path + '/python/ZTauTauGeneration'
		self.shellscriptworkflow_path = self.embedding_path + '/scripts/shellscripts'
		
		self.generatorfileabspath = generatorfileabspath
		
		# reading template
		self.template = ""
		try:
			filein = open(self.template_path + '/embToKappa_workflow_template.sh.txt', 'r')
			self.template = filein.read()
			filein.close()
		except IOError: print 'IOError: Generator template does not exist. Please define it as {TEMPLATE_PATH}'.format(TEMPLATE_PATH=self.template_path + '/embToKappa_workflow_template.sh.txt')
		
		# setting default values for template arguments
		self.randomserviceswitch = False
		self.globaltag = "76X_mcRun2_asymptotic_v12"
		self.generatorfile = os.path.relpath(self.generatorfileabspath, self.generator_path)
		self.vtxcorrection = ",TauAnalysis/EmbeddingProducer/customisers.customiseGeneratorVertexFromInput"
		self.correctvtx = False
		
		# setting default embedding to kappa workflow filename and folder
		self.fileoutfolder = self.shellscriptworkflow_path + '/test'
		self.fileoutname = self.fileoutfolder + '/embToKappa_workflow_test.sh'
	
	def set_embToKappa_workflow(self, randomserviceswitch=None, globaltag=None, correctvtx=None):
		
		print "Changing settings for embedding to kappa workflow file."
		
		self.globaltag = self.globaltag if globaltag is None else globaltag
		self.randomserviceswitch = self.randomserviceswitch if randomserviceswitch is None else randomserviceswitch
		self.correctvtx = self.correctvtx if correctvtx is None else correctvtx
		self.template = self.template.format(
			GLOBALTAG = self.globaltag,
			RANDOMSERVICESWITCH = "" if self.randomserviceswitch else "#",
			GENERATORFILE = self.generatorfile,
			VERTEXCORRECTION = self.vtxcorrection if self.correctvtx else ""
		)
	
	def save_embToKappa_workflow(self, fileoutfolder=None, fileoutname=None):
		
		# preparing embedding to kappa workflow filename and folder
		if not fileoutfolder is None:
			self.fileoutfolder = self.shellscriptworkflow_path + '/' + fileoutfolder
		if not fileoutname is None:
			self.fileoutname = self.fileoutfolder + '/' + fileoutname
			generatorfile = '_' + self.generatorfile.replace('/','').replace(fileoutfolder,'').replace("_cfi.py","")
			insertindex = self.fileoutname.find(".sh")
			self.fileoutname = self.fileoutname[:insertindex] + generatorfile + self.fileoutname[insertindex:]
		else:
			self.fileoutname = self.fileoutfolder + '/embToKappa_workflow_test.sh'
	
		# saving embedding to kappa workflow file
		if not os.path.exists(self.fileoutfolder):
			os.makedirs(self.fileoutfolder)
		fileout = open(self.fileoutname, 'w')
		fileout.write(self.template)
		print "Saving embedding to kappa workflow file as {FILEOUTNAME}".format(FILEOUTNAME=self.fileoutname)
		fileout.close()

		os.chmod(self.fileoutname, 0755)
		print "Enabling execution rights for {FILEOUTNAME}".format(FILEOUTNAME=self.fileoutname)
	
	def print_embToKappa_workflow_settings(self):
		
		print
		print "---------Current settings---------"
		print "Global tag: ", self.globaltag
		print "Used generator file: ", self.generatorfile
		print "Random service switch: ", self.randomserviceswitch
		print "Output folder: ", self.fileoutfolder
		print "Output file name: ", self.fileoutname
		print "----------------------------------"
		print

if __name__ == "__main__":
	
	from gen_creator import single_gen
	
	def perform_embToKappa_workflow_creation(generatorfileabspath, randomserviceswitch, globaltag, correctvtx, fileoutfolder, fileoutname):
		embToKappa_workflow = single_embToKappa_workflow(generatorfileabspath)
		embToKappa_workflow.set_embToKappa_workflow(randomserviceswitch=randomserviceswitch, globaltag=globaltag, correctvtx=correctvtx)
		embToKappa_workflow.save_embToKappa_workflow(fileoutfolder=fileoutfolder, fileoutname=fileoutname)
		embToKappa_workflow.print_embToKappa_workflow_settings()
		return embToKappa_workflow
	
	def perform_gen_creation(externaldecay, active_decaychannels, nattempts, muonembedding, fileoutfolder, fileoutname):
		gen = single_gen()
		gen.set_gen(externaldecay=externaldecay, active_decaychannels=active_decaychannels, nattempts=nattempts, muonembedding=muonembedding)
		gen.save_gen(fileoutfolder=fileoutfolder, fileoutname=fileoutname)
		gen.print_gen_settings()
		return gen
	
	import argparse
	
	class LoadFromFile (argparse.Action):
		def __call__ (self, parser, namespace, values, option_string = None):
			with values as f:
				parser.parse_args(f.read().replace('"','').split(), namespace)
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--loadfromfile', type=open, action=LoadFromFile, help='Load the options below from a .txt file.')
	
	parser.add_argument('--globaltag', default=None, help='Global tag of the input file and sample production.')
	parser.add_argument('--outputfolder', default=None, help='Name of the output folder used for all templates.')
	
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
	
	args = parser.parse_args()

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

