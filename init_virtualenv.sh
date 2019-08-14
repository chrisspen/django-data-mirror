#!/bin/bash
set -e
VENV=${2:-.env}
cd "$(dirname "$0")"
REL_DIR=./
[ -d $REL_DIR$VENV ] && rm -Rf $REL_DIR$VENV
python3.7 -m venv $REL_DIR$VENV
. $REL_DIR$VENV/bin/activate
pip install -r requirements.txt -r requirements-test.txt
