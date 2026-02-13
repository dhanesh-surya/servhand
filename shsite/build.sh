#!/bin/bash

# Install system dependencies for pillow and other packages
apt-get update
apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz0b \
    libfribidi0

# Clean up apt cache
apt-get clean
rm -rf /var/lib/apt/lists/*
