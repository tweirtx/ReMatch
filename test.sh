#!/usr/bin/env bash
sudo -u postgres psql -f purge.sql
source /home/travis/PycharmProjects/ReMatch/venv/bin/activate
python3 -m ReMatch iWDSy2FoPwU youtube 2019njbri frc Sii5fcmevN8 youtube
