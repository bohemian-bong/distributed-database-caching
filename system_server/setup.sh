#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install Python 3 and pip
echo "Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip

# Install Flask
echo "Installing Flask..."
pip3 install Flask

# Install PyMongo
echo "Installing PyMongo..."
pip3 install pymongo

# Verify installations
echo "Verifying installations..."
python3 -m flask --version
python3 -c "import pymongo; print(pymongo.__version__)"

echo "Installation complete!"
