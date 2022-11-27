#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install docker
apt-get install docker-compose
pip install -r requirements.txt
docker pull mysql

