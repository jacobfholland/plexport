#!/bin/bash

# Uninstall current plexport package
pip uninstall plexport -y

# Delete the dist folder
rm -rf dist
rm -rf build
rm -rf plexport.egg-info

# Repackage the plexport package
python3 setup.py sdist bdist_wheel

# Install the newly packaged plexport package
pip install dist/plexport-0.1.tar.gz
