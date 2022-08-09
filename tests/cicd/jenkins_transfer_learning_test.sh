#!/bin/bash

# set vars
# MODEL_NAME="TLK"
# DATA_PATH="/home/vmagent/app/AIDK/TransferLearningKit/datasets"

# init conda env
eval "$('/opt/intel/oneapi/intelpython/latest/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
# activate conda
conda activate pytorch-1.10.0
echo `pwd`
ls
# run main.py
cd /home/vmagent/app/AIDK/TransferLearningKit/src
python main.py

# run unittest
cd /home/vmagent/app/AIDK/TransferLearningKit/test
# pytest -v test_transferrable_model.py # pytest for single test file
pytest -v test_basic_finetunner.py
python run_testting.py
