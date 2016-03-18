echo "================= CMSRUN starting ===================="
cmsRun -j FrameworkJobReport.xml -p PSet.py

echo "================= creating softlink for cfipython ===================="

rm -rf $CMSSW_BASE/cfipython
ln $CMSSW_RELEASE_BASE/cfipython $CMSSW_BASE/cfipython -s

echo "================= INPUT SKIMMING finished ===================="

cmsDriver.py TauAnalysis/EmbeddingProducer/python/lhehadronizerpythia8tauolafilter_cfi.py  \
  --filein file:skimmed.root --fileout file:step1.root \
  --conditions 76X_mcRun2_asymptotic_v12 --era Run2_25ns \
  --relval 9000,50 \
  --step GEN,SIM --datatier GEN-SIM \
  --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps \
  --beamspot NominalCollision2015 --no_exec -n -1 \
  --python_filename embedding.py

#echo 'from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper' >> embedding.py
#echo 'randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)' >> embedding.py
#echo 'randSvc.populate()' >> embedding.py

cmsRun -p embedding.py

echo "================= EMBEDDING STEP finished ===================="

cmsDriver.py step2  --conditions 76X_mcRun2_asymptotic_v12 \
  --filein file:step1.root --fileout file:step2.root \
  --step DIGI,L1,DIGI2RAW,HLT:@relval25ns \
  --datatier GEN-SIM-DIGI-RAW-HLTDEBUG  \
  --era Run2_25ns --eventcontent FEVTDEBUGHLT \
  --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps \
  --no_exec -n -1 --python_filename step2.py

cmsRun -p step2.py
rm step1.root

echo "================= STEP2 finished ===================="

cmsDriver.py step3  --runUnscheduled  --conditions 76X_mcRun2_asymptotic_v12 \
  --filein file:step2.root --fileout file:skimmed_to_reco.root \
  --step RAW2DIGI,L1Reco,RECO,PAT \
  --datatier MINIAODSIM \
  --era Run2_25ns --eventcontent MINIAODSIM \
  --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps \
  --no_exec -n -1 --python_filename step3.py

echo 'process.CSCHaloData.HLTResultLabel = cms.InputTag("TriggerResults","","HLTembedding")' >> step3.py
echo 'process.patTrigger.processName = cms.string("HLTembedding")' >> step3.py

cmsRun -p step3.py
rm step2.root
echo "================= STEP3 finished ===================="

cp $CMSSW_BASE/python/TauAnalysis/EmbeddingProducer/kSkimming_run2_MC_miniaod_cfg_for_test.py kappa.py
cmsRun -p kappa.py
rm skimmed_to_reco.root
echo "================= KAPPASKIM finished ===================="
#ls -lrth
echo "================= CMSRUN finished ===================="
