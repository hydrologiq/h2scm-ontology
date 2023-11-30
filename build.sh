#!/bin/bash

set -e

echo "generating ontology"

rm -rf dist

pip3 install -r requirements.txt
python3 main.py

echo "generated ontology"
