#!/bin/bash
. /home/ubuntu/.bashrc

PATH=$(dirname "$0")

cd /home/ubuntu/NewtonBot &&
source venv/bin/activate &&
python ./src/trader.py
