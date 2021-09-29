import FWCore.ParameterSet.Config as cms

# Select only events where magnetic field had specified value.
# Uses Alignment/CommonAlignment/plugins/MagneticFieldFilter.cc
MagneticFieldFilter = cms.EDFilter("MagneticFieldFilter",
                                    magneticField = cms.untracked.int32(38) # in kGauss to nearest integer
                                   )

# Select only events when pixel & strip tracker high voltage is on.
# Uses DQM/TrackerCommon/plugins/DetectorStateFilter.cc
pixelHVonFilter = cms.EDFilter("DetectorStateFilter",
                                DebugOn      = cms.untracked.bool(False),
                                DetectorType = cms.untracked.string("pixel")
                               )
stripHVonFilter = cms.EDFilter("DetectorStateFilter",
                                DebugOn      = cms.untracked.bool(False),
                                DetectorType = cms.untracked.string("sistrip")
                               )
trackerHVonFilter = cms.Sequence(pixelHVonFilter * stripHVonFilter)

# Select only events where strip tracker electronics is in deconvolution mode.
# Uses Alignment/CommonAlignment/plugins/APVModeFilter.cc
APVModeFilter = cms.EDFilter("APVModeFilter",
                              apvMode = cms.untracked.string("deco")
                             )

# Select only events passing certain triggers.
# The throw option causes the job to throw a fatal error if the desired trigger is not present in the menu of all runs.
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
triggerSelection = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["*"], throw = cms.bool(False))

# Event filters
cosmicFilters = cms.Sequence(MagneticFieldFilter * trackerHVonFilter * APVModeFilter * triggerSelection)                         
