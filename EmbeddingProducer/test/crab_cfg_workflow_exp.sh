echo "================= CMSRUN starting ===================="
cmsRun -j FrameworkJobReport.xml -p PSet.py

echo "================= creating softlink for cfipython ===================="

rm -rf $CMSSW_BASE/cfipython
ln $CMSSW_RELEASE_BASE/cfipython $CMSSW_BASE/cfipython -s

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

echo "================= moving local PatUtils ===================="

mkdir $CMSSW_BASE/python/PhysicsTools/moved/
mv $CMSSW_BASE/python/PhysicsTools/PatUtils/ $CMSSW_BASE/python/PhysicsTools/moved/ -f

echo "================= creating softlink for PatUtils ===================="
ln $CMSSW_RELEASE_BASE/python/PhysicsTools/PatUtils/ $CMSSW_BASE/python/PhysicsTools/PatUtils -s

cmsDriver.py step3  --runUnscheduled  --conditions auto:run2_mc_25ns14e33_v4 \
  --filein file:step2.root --fileout file:skimmed_to_reco.root \
  --step RAW2DIGI,L1Reco,RECO,EI,PAT \
  --datatier MINIAODSIM \
  --era Run2_25ns --eventcontent MINIAODSIM \
  --customise TauAnalysis/EmbeddingProducer/customisers.customiseAllSteps \
  --no_exec -n -1 --python_filename step3.py

echo 'process.CSCHaloData.HLTResultLabel = cms.InputTag("TriggerResults","","HLTembedding")' >> step3.py
echo 'process.patTrigger.processName = cms.string("HLTembedding")' >> step3.py

cmsRun -p step3.py
rm step2.root
echo "================= STEP3 finished ===================="

echo "================= removing softlink for PatUtils ===================="
rm $CMSSW_BASE/python/PhysicsTools/PatUtils

echo "================= moving local PatUtils back ===================="
mv $CMSSW_BASE/python/PhysicsTools/moved/PatUtils/ $CMSSW_BASE/python/PhysicsTools/ -f
rm $CMSSW_BASE/python/PhysicsTools/moved/ -rf

cp $CMSSW_BASE/python/TauAnalysis/EmbeddingProducer/kSkimming_run2_MC_miniaod_cfg_for_test.py kappa.py
cmsRun -p kappa.py
rm skimmed_to_reco.root
echo "================= KAPPASKIM finished ===================="
ls -lrth
echo "================= CMSRUN finished ===================="
