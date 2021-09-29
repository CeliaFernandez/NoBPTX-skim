# NoBPTX-skim

## How to install

Run the following set of commands:
```
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
mkdir Cosmic-Analysis
cd Cosmic-Analysis
git clone git@github.com:CeliaFernandez/NoBPTX-skim.git
scram b -j 8
```

## Run the skim
Always with NoBPTX datasets (running on dedicated Cosmics datasets won't work since pp reco collections are not available there):
```
cmsRun test/reduceCosmics_cfg.py
```
