#!/bin/bash
set -e
cd /app/workspace/scripts
rm -rf /tmp/mineru
python download_mineru.py
cd /tmp/mineru/
python setup.py