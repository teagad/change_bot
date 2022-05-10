#!/bin/bash
virtualenv test
export BOT_TOKEN="write your token"
                
source test/bin/activate
pip install -r requirements.txt
python3 main.py