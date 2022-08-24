#!/bin/bash

chmod +x run_trader_cron.sh &&
virtualenv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
python setup.py &&
deactivate