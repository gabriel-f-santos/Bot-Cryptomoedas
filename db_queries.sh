#!/bin/bash
. /home/gabriel/.bashrc

PATH=$(dirname "$0")

cd $PATH &&
source venv/bin/activate &&
python db_queries.py