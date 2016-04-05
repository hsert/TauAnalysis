#! /usr/bin/env python

import os

class single_gen():
	
	def __init__(self):
		
		
		print "Initializing generator file."
		# setting used paths
		self.cmssw_path = os.environ.get('CMSSW_BASE')
		if self.cmssw_path is None:
			raise EnvironmentError('Set CMSSW environment.')
		self.embedding_path = self.cmssw_path + '/src/TauAnalysis/EmbeddingProducer'
		self.template_path = self.embedding_path + '/templates'
		self.generator_path = self.embedding_path + '/python/ZTauTauGeneration'

		# reading template
		self.template = ""
		try:
			filein = open(self.template_path + '/lhehadronizerpythia8_template.py.txt', 'r')
			self.template = filein.read()
			filein.close()
		except IOError: print 'IOError: Generator template does not exist. Please define it as {TEMPLATE_PATH}'.format(TEMPLATE_PATH=self.template_path + '/lhehadronizerpythia8_template.py.txt')
		
		# setting default template arguments
		self.nattempts = 1000
		self.muonembedding = False
		
		self.ElElCut = 'ElElCut = cms.untracked.string("El1.Pt > 20 && El2.Pt > 8 && El1.Eta < 2.4 && El2.Eta < 2.4"),'
		self.MuMuCut = 'MuMuCut = cms.untracked.string("Mu1.Pt > 15 && Mu2.Pt > 6 && Mu1.Eta < 2.4 && Mu2.Eta < 2.4"),'
		self.HadHadCut = 'HadHadCut = cms.untracked.string("Had1.Pt > 30 && Had2.Pt > 30  && Had1.Eta < 2.1 && Had2.Eta < 2.1"),'
		self.ElMuCut = 'ElMuCut = cms.untracked.string("(El.Pt > 11 && El.Eta < 2.5 && Mu.Pt > 16 && Mu.Eta < 2.4) || (El.Pt > 16 && El.Eta < 2.5 && Mu.Pt > 8 && Mu.Eta < 2.4)"),'
		self.ElHadCut = 'ElHadCut = cms.untracked.string("El.Pt > 22 && El.Eta < 2.1 && Had.Pt > 10 && Had.Eta < 2.3"),'
		self.MuHadCut = 'MuHadCut = cms.untracked.string("Mu.Pt > 17 && Mu.Eta < 2.1 && Had.Pt > 10 && Had.Eta < 2.3"),'
		self.decaychannels = {"EE" : [0, self.ElElCut], "MM" : [1, self.MuMuCut], "TT" : [2, self.HadHadCut], "EM" : [3, self.ElMuCut], "ET" : [4, self.ElHadCut], "MT" : [5, self.MuHadCut]}
		self.active_decaychannels = ["EM"]
		
		self.photospp = '''ExternalDecays = cms.PSet(
    Photospp = cms.untracked.PSet(
      parameterSets = cms.vstring('suppressAll', 'forceBremForBranch', 'setInfraredCutOff'),
      suppressAll = cms.bool(True),
      forceBremForBranch = cms.PSet(
        parameterSets = cms.vstring('TauPlus', 'TauMinus'),
        TauMinus = cms.vint32(0,15),
        TauPlus = cms.vint32(0,-15)
      ),
      suppressBremForDecay = cms.PSet(
        parameterSets = cms.vstring('Taumpipi0nu','Tauppipi0nu','Taumpipi0nugamma','Tauppipi0nugamma'),
        Taumpipi0nu = cms.vint32(3, 15, 16, 111, -211),
        Tauppipi0nu = cms.vint32(3, -15, -16, 111, 211),
        Taumpipi0nugamma = cms.vint32(4, 15, 16, 22, 111, -211),
        Tauppipi0nugamma = cms.vint32(4, -15, -16, 22, 111, 211)
      ),
      setInfraredCutOff = cms.double(0.01)
    ),
    parameterSets = cms.vstring('Photospp')
  ),'''
		self.externaldecays = {"photospp" : self.photospp, "" : ""}
		self.externaldecay = ""
		
		# setting default gen filename and folder
		self.fileoutfolder = self.generator_path + '/test'
		self.fileoutname = self.fileoutfolder + '/lhehadronizerpythia8_test.py'
	
	def set_gen(self, externaldecay=None, active_decaychannels=None, nattempts=None, muonembedding=None):
		
		print "Changing setting for generator file."
		pythiadecaymode = "'15:onMode = off',\n        '15:onIfAny = 11 13',"
		
		self.externaldecay = self.externaldecay if externaldecay is None else externaldecay
		self.active_decaychannels = self.active_decaychannels if active_decaychannels is None else active_decaychannels
		self.nattempts = self.nattempts if nattempts is None else nattempts
		self.muonembedding = self.muonembedding if muonembedding is None else muonembedding
		
		dc_list = ["","","","","",""]
		for dc in self.active_decaychannels:
			dc_list[self.decaychannels[dc][0]] = self.decaychannels[dc][1]
		
		self.template = self.template.format(
			dc_list,
			NATTEMPTS=self.nattempts,
			MUONEMBEDDING="True" if self.muonembedding else "False",
			EXTERNALDECAY=self.externaldecays[self.externaldecay],
			PYTHIADECAYMODE = pythiadecaymode if self.active_decaychannels == ["EM"] else ""
		)
	
	def save_gen(self, fileoutname=None, fileoutfolder=None):
		
		# preparing gen filename and folder
		if not fileoutfolder is None:
			self.fileoutfolder = self.generator_path + '/' + fileoutfolder
		if not fileoutname is None:
			self.fileoutname = self.fileoutfolder + '/' + fileoutname
		if self.externaldecay != '':
			externaldecay = '_' + self.externaldecay
			insertindex = self.fileoutname.find(".py")
			self.fileoutname = self.fileoutname[:insertindex] + externaldecay + self.fileoutname[insertindex:]
		for dc in self.active_decaychannels:
			insertindex = self.fileoutname.find(".py")
			self.fileoutname = self.fileoutname[:insertindex] + "_" + dc + self.fileoutname[insertindex:]
		insertindex = self.fileoutname.find(".py")
		self.fileoutname = self.fileoutname[:insertindex] + "_cfi" + self.fileoutname[insertindex:]
	
		# saving gen file
		if not os.path.exists(self.fileoutfolder):
			os.makedirs(self.fileoutfolder)
		fileout = open(self.fileoutname, 'w')
		fileout.write(self.template)
		print "Saving generator file as {FILEOUTNAME}".format(FILEOUTNAME=self.fileoutname)
		fileout.close()
	
	def print_gen_settings(self):
		
		print
		print "---------Current settings---------"
		print "Active decay channels: ", self.active_decaychannels
		print "Additional external decay generator: ", self.externaldecay
		print "Number of attempts for the filter: ", self.nattempts
		print "Switch for muon embedding: ", self.muonembedding
		print "Output folder: ", self.fileoutfolder
		print "Output file name: ", self.fileoutname
		print "----------------------------------"
		print

if __name__ == "__main__":
	
	def perform_gen_creation(externaldecay, active_decaychannels, nattempts, muonembedding, fileoutfolder, fileoutname):
		gen = single_gen()
		gen.set_gen(externaldecay=externaldecay, active_decaychannels=active_decaychannels, nattempts=nattempts, muonembedding=muonembedding)
		gen.save_gen(fileoutfolder=fileoutfolder, fileoutname=fileoutname)
		gen.print_gen_settings()
		return gen
	
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--decaychannels', default=[], nargs = '+', help='Defines, which set of decay channels of the ditau system should simulated and tested. If multiple channels are in a set, then separate them by comma in the string. Possible values: "EE","MM","TT","EM","ET","MT","ALL".')
	parser.add_argument('--externaldecays', default=[], nargs = '+', help='Defines additional generators that should enabled within pythia8 hadronizer. Possible values: "photospp".')
	parser.add_argument('--nattempts', default=None, type=int, help="Number of attempts for the filter that is tested.")
	parser.add_argument('--muonembedding', default=None, action='store_true', help='Enables muon embedding.')
	parser.add_argument('--outputfolder', default=None, help='Name of the output folder.')
	parser.add_argument('--outputfilename', default=None, help='Name of the output file.')
	
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
				fileoutname = args.outputfilename
			)
