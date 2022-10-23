#!/bin/bash

# ensure the base OS has Python==3.9.13+ at this point onwards

echo "Initializing virtual environment"
python3 -m venv ./venv --clear

# because `source venv/bin/activate` may not work inside Docker container
work_dir=`pwd`
VIRTUAL_ENV="$work_dir/venv"
PATH="$VIRTUAL_ENV/bin:$PATH"

echo "Installing pip and pip-tools"
python3 -m pip install --upgrade pip==22.0.4 --require-virtualenv

pip3 install pip-tools==6.8.0 --require-virtualenv

echo "Installing dependencies"
pip-sync requirements.txt --pip-args '--no-cache-dir --require-virtualenv'

echo "Production environment built !"
