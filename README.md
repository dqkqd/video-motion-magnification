# video motion magnification
Python source code to amplificate motion on a video, this code is written based on [pbMoMa: Phase Based video MOtion MAgnification](https://github.com/jvgemert/pbMoMa) and [Steerable pyramid and STSIM metrics](https://github.com/andreydung/Steerable-filter)
### Requirements:
  - python 3.6
  - numpy
  - scipy
  - opencv
### Run Command:
    
    python3 main.py "video-name" "amplification_factor" "low_frequency" "high_frequency"

### Example:
    python3 main.py videos/plants.avi 40 0.2 0.4
    
