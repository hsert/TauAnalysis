echo "================= CMSRUN starting ===================="
cmsRun -j FrameworkJobReport.xml -p PSet.py

mv skimmed_to_reco skimmed.root

echo "================= INPUT SKIMMING finished ===================="

cmsDriver.py TauAnalysis/EmbeddingProducer/python/lhehadronizerpythia8tauolafilter_cfi.py  \
  --filein file:skimmed.root --fileout file:step1.root \
  --conditions auto:run2_mc --era Run2_25ns \
  --eventcontent FEVTDEBUG --relval 9000,50 \
  --step GEN,SIM --datatier GEN-SIM \
  --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps \
  --beamspot Realistic50ns13TeVCollision --no_exec -n -1 \
  --python_filename embedding.py

cmsRun -p embedding.py
rm skimmed.root

echo "================= EMBEDDING STEP finished ===================="

cmsDriver.py step2  --conditions auto:run2_mc_25ns14e33_v4 \
  --filein file:step1.root --fileout file:step2.root \
  --step DIGI:pdigi_valid,L1,DIGI2RAW,HLT:@relval25ns \
  --datatier GEN-SIM-DIGI-RAW-HLTDEBUG  \
  --era Run2_25ns --eventcontent FEVTDEBUGHLT \
  --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps \
  --no_exec -n -1 --python_filename step2.py

cmsRun -p step2.py
rm step1.root

echo "================= STEP2 finished ===================="

cmsDriver.py step3  --runUnscheduled  --conditions auto:run2_mc_25ns14e33_v4 \
  --filein file:step2.root --fileout file:skimmed_to_reco.root \
  --step RAW2DIGI,L1Reco,RECO,EI,PAT \
  --datatier GEN-SIM-RECO,MINIAODSIM \
  --era Run2_25ns --eventcontent RECOSIM,MINIAODSIM \
  --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps \
  --no_exec -n -1 --python_filename step3.py

echo 'process.CSCHaloData.HLTResultLabel = cms.InputTag("TriggerResults","","HLTembedding")' >> step3.py
echo 'process.patTrigger.processName = cms.string("HLTembedding")' >> step3.py

cmsRun -p step3.py
rm step2.root
echo "================= STEP3 finished ===================="


echo "================= CMSRUN finished ===================="
