################
# this cfg file runs 
# - track reconstruction (RECOBEFMIX step)
# - production of TrackingParticles used for truth matching of reconstructed tracks (in DIGI:pdigi_valid)
# - tracking particle validation as performed in the official validation (in VALIDATION STEP)
# - track validation as performed in the offical validation (in VALIDATION step)
# - track seed validation
#
# it is based on the configuration file generated by the following cmsDriver command
# cmsDriver.py test --conditions auto:run2_mc --fast -n 10 --eventcontent DQM --relval 100000,1000 -s RECOBEFMIX,DIGI:pdigi_valid,VALIDATION --datatier DQMIO --beamspot NominalCollision2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1 --no_exec --filein file:YOUR_FILE.root
#
# the modification with respect to the as such generated config file are indicated with BEGIN/END MODIFICATION
################

import FWCore.ParameterSet.Config as cms

process = cms.Process('VALIDATION')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('FastSimulation.Configuration.Geometries_MC_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('FastSimulation.Configuration.Reconstruction_BefMix_cff')
process.load('FastSimulation.Configuration.Digi_cff')
process.load('FastSimulation.Configuration.Validation_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring('file:GENSIM.root'),
    inputCommands = cms.untracked.vstring('keep *', 
        'drop *_genParticles_*_*', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('test nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('TrackRecoAndValidation_inDQM.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.mix.digitizers = cms.PSet(process.theDigitizersValid)
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# Path and EndPath definitions
process.reconstruction_befmix_step = cms.Path(process.reconstruction_befmix)
process.digitisation_step = cms.Path(process.pdigi_valid)
process.prevalidation_step = cms.Path(process.prevalidation)
process.validation_step = cms.EndPath(process.validation)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.reconstruction_befmix_step,process.digitisation_step,process.prevalidation_step,process.validation_step,process.DQMoutput_step)

# customisation of the process.

# Automatic addition of the customisation function from FastSimulation.Configuration.MixingModule_Full2Fast
from FastSimulation.Configuration.MixingModule_Full2Fast import prepareDigiRecoMixing 

#call to customisation function prepareDigiRecoMixing imported from FastSimulation.Configuration.MixingModule_Full2Fast
process = prepareDigiRecoMixing(process)

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions

# BEGIN MODIFICATIONS
# load tracker seed validator
process.load('Validation.RecoTrack.TrackerSeedValidator_cfi')
process.trackerSeedValidator.TTRHBuilder = "WithoutRefit"
process.trackerSeedValidator.associators = cms.vstring('trackAssociatorByHitsRecoDenom')
process.trackerSeedValidator.label = cms.VInputTag(
    cms.InputTag("initialStepSeeds"),
    cms.InputTag("detachedTripletStepSeeds"),
    cms.InputTag("lowPtTripletStepSeeds"),
    cms.InputTag("pixelPairStepSeeds"),
    cms.InputTag("mixedTripletStepSeeds"),
    cms.InputTag("pixelLessStepSeeds"),
    cms.InputTag("tobTecStepSeeds"))
# redefine validation paths
process.prevalidation = cms.Sequence(process.tracksValidationSelectors)
process.validation = cms.Sequence(process.trackingTruthValid + process.tracksValidationFS + process.trackerSeedValidator)
# END MODIFICATIONS
