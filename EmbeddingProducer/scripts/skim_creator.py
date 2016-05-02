#! /usr/bin/env python

import os

class single_skim():
	
	def __init__(self):
		
		print "Initializing skim file."
		
		# setting used paths
		self.cmssw_path = os.environ.get('CMSSW_BASE')
		if self.cmssw_path is None:
			raise EnvironmentError('Set CMSSW environment.')
		self.embedding_path = self.cmssw_path + '/src/TauAnalysis/EmbeddingProducer'
		self.template_path = self.embedding_path + '/templates'
		self.skimming_path = self.embedding_path + '/python/Skimming'

		# reading template
		self.template = ""
		try:
			filein = open(self.template_path + '/skim_template.py.txt', 'r')
			self.template = filein.read()
			filein.close()
		except IOError: print 'IOError: Skim template does not exist. Please define it as {TEMPLATE_PATH}'.format(TEMPLATE_PATH=self.template_path + '/skim_template.py.txt')
		
		# setting default template arguments
		self.inputfile = "file:/pnfs/desy.de/cms/tier2/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/004544CB-6DD8-E511-97E4-0026189438F6.root"
		self.globaltag = "76X_mcRun2_asymptotic_v12"
		self.fsrmode = "reco"
		self.muonembedding = False
		
		# setting default skim filename and folder
		self.fileoutfolder = self.skimming_path + '/test'
		self.fileoutname = self.fileoutfolder + '/skim_test.py'
		
		# setting default input format and possible formats
		self.miniaod = "from TauAnalysis.EmbeddingProducer.customisers import customiseMuonInputForMiniAOD\nprocess = customiseMuonInputForMiniAOD(process)"
		self.reco = "from TauAnalysis.EmbeddingProducer.customisers import customiseMuonInputForRECO\nprocess = customiseMuonInputForRECO(process)"
		self.inputformats = {"miniaod" : self.miniaod, "reco" : self.reco}
		self.formatname = "miniaod"
		
		
	def set_skim(self, inputfile=None, globaltag=None, fsrmode=None, muonembedding=None, formatname=None):
		
		print "Changing settings for skim file."
		
		self.inputfile = self.inputfile if inputfile is None else inputfile
		self.globaltag = self.globaltag if globaltag is None else globaltag
		self.fsrmode = self.fsrmode if fsrmode is None else fsrmode
		self.muonembedding = self.muonembedding if muonembedding is None else muonembedding
		
		if formatname not in self.inputformats:
			print "No known input format given. Using default (miniaod)."
			self.formatname = self.formatname
		else: self.formatname = formatname
		
		self.template = self.template.format(INPUTFILE = self.inputfile, GLOBALTAG = self.globaltag, FSRMODE = self.fsrmode, CUSTOMIZEINPUT = self.inputformats[self.formatname], MUONEMBEDDING = "True" if self.muonembedding else "False")
	
	def save_skim(self, fileoutname=None, fileoutfolder=None):
		
		# preparing skim filename and folder
		if not fileoutfolder is None:
			self.fileoutfolder = self.skimming_path + '/' + fileoutfolder
		if not fileoutname is None:
			self.fileoutname = self.fileoutfolder + '/' + fileoutname
		else:
			self.fileoutname = self.fileoutfolder + '/skim_test.py'
		if self.fsrmode != '':
			fsr = '_' + self.fsrmode
			insertindex = self.fileoutname.find(".py")
			self.fileoutname = self.fileoutname[:insertindex] + fsr + self.fileoutname[insertindex:]
	
		# saving skim file
		if not os.path.exists(self.fileoutfolder):
			os.makedirs(self.fileoutfolder)
		fileout = open(self.fileoutname, 'w')
		fileout.write(self.template)
		print "Saving skim file as {FILEOUTNAME}".format(FILEOUTNAME=self.fileoutname)
		fileout.close()
	
	def print_skim_settings(self):
		
		print
		print "---------Current settings---------"
		print "Input file: ", self.inputfile
		print "Format of the input file: ", self.formatname
		print "Global tag: ", self.globaltag
		print "Used FSR mode: ", self.fsrmode
		print "Switch for muon embedding: ", self.muonembedding
		print "Output folder: ", self.fileoutfolder
		print "Output file name: ", self.fileoutname
		print "----------------------------------"
		print

if __name__ == "__main__":
	
	def perform_skim_creation(fsrmode, formatname, inputfile, globaltag, muonembedding, fileoutfolder, fileoutname):
		skim = single_skim()
		skim.set_skim(fsrmode=fsrmode, formatname=formatname, inputfile=inputfile, globaltag=globaltag, muonembedding=muonembedding)
		skim.save_skim(fileoutfolder=fileoutfolder, fileoutname=fileoutname)
		skim.print_skim_settings()
		return skim
	
	import argparse
	
	class LoadFromFile (argparse.Action):
		def __call__ (self, parser, namespace, values, option_string = None):
			with values as f:
				parser.parse_args(f.read().replace('"','').split(), namespace)
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--loadfromfile', type=open, action=LoadFromFile, help='Load the options below from a .txt file.')
	
	parser.add_argument('--inputfile', default=None, help='Input file for ZToMuMu selection.')
	parser.add_argument('--format', default=None, help='Format of the input file. Possible values: "miniaod", "reco".')
	parser.add_argument('--globaltag', default=None, help='Global tag of the input file.')
	parser.add_argument('--fsrmodes', default=[], nargs = '+', help='Defines, whether final state radiation should be studied on generator level and if it is the case, which state of the muon should be taken. Possible values: "afterFSR", "beforeFSR", "reco". ')
	parser.add_argument('--muonembedding', default=None, action='store_true', help='Enables muon embedding.')
	parser.add_argument('--outputfolder', default=None, help='Name of the output folder.')
	parser.add_argument('--outputfilename', default=None, help='Name of the output file.')
	
	args = parser.parse_args()
	
	if len(args.fsrmodes) == 0: args.fsrmodes = [None]
	for fsrmode in args.fsrmodes:
		skim = perform_skim_creation(fsrmode=fsrmode, formatname = args.format, inputfile = args.inputfile, globaltag = args.globaltag, muonembedding = self.muonembedding, fileoutfolder = args.outputfolder, fileoutname = args.outputfilename)

