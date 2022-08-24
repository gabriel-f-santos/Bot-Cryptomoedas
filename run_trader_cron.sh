#!/bin/bash
. /home/gabriel/.bashrc

PATH=$(dirname "$0")

cd /home/gabriel/Documents/Projetos/robos/robo-cripto/robo_medias_gabriel/ &&
source venv/bin/activate &&
python ./src/trader.py