#! /bin/bash    
source /home/admin/miniconda3/etc/profile.d/conda.sh && \
conda activate risk_access && \
cd /home/admin/risk_access && \
python fullprocess.py && \
python apicalls.py
#python /home/admin/risk_access/fullprocess.py
