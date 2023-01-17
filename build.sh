#!/bin/bash
pip install --upgrade pip
pip install -r requirements.txt
python ./arduino_web/manage.py collectstatic --no-input