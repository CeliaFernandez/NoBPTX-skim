import FWCore.ParameterSet.Config as cms

# Produced reduced dataset containing only info needed to measure muon efficiency
# with cosmic rays in spark tool
#
# @ Celia Fernandez Madrazo (from Ian Tomalin code)


process = cms.Process("skim")

# Debug printout & summaries.
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.limit = cms.untracked.int32(50)
process.MessageLogger.cerr.default.limit = cms.untracked.int32(50)

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(True),
  # Set up multi-threaded run. Must be consistent with config.JobType.numCores in crab_cfg.py.
  #numberOfThreads=cms.untracked.uint32(8)
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag

# Select number of events to be processed
nEvents = 1000
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(nEvents) )

# Read events
isData = True # Always true by default (running on MC is useless)
if (isData):
  process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      [
        '/store/data/Run2018B/NoBPTX/AOD/12Nov2019_UL2018-v1/00000/0440AB21-7479-B042-A968-2DA3A72B894A.root'
      ]),
    secondaryFileNames = cms.untracked.vstring(),
    skipEvents = cms.untracked.uint32(0)
  )
  process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data')


# Filters to select cosmic events
process.load("Cosmic-Analysis.NoBPTX-skim.filters_cff")
process.filtersPath = cms.Path(process.cosmicFilters)

# Output reduced dataset.
process.output = cms.OutputModule("PoolOutputModule",
  fileName = cms.untracked.string('output.root'),
  SelectEvents = cms.untracked.PSet( 
    SelectEvents = cms.vstring('filtersPath') 
  ),
  outputCommands = cms.untracked.vstring(
    'keep L1GlobalTriggerReadoutRecord_gtDigis_*_*',       # Trigger info
    'keep triggerTriggerEvent_hltTriggerSummaryAOD_*_HLT',
    'keep edmTriggerResults_TriggerResults_*_HLT',
    'keep DcsStatus*_scalersRawToDigi_*_*',    # Needed to check Tracker HV status
    'keep recoMuons_muonsFromCosmics1Leg_*_*', # cosmics recoed as a single helix
    'keep recoTracks_cosmicMuons1Leg_*_*',     # Referenced by muonsFromCosmics1Leg
    'keep recoMuons_muonsFromCosmics_*_*',     # cosmics recoed as two helices
    'keep recoTracks_cosmicMuons_*_*',         # Referenced by muonsFromCosmics
    'keep recoTracks_generalTracks_*_*',       # Found in Tracker
    'keep *_genParticles_*_*',                 # Truth
    'keep edmHepMCProduct_generator_*_*',      # Contains cosmic production time.
    'keep recoMuons_muons*_*_*',               # pp-reco Muons
    'keep recoTracks_*Muons_*_*'               # non-standard pp-reco Muons (dGlobals)
  )
)

process.e = cms.EndPath(process.output)

