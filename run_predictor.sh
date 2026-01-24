#!/bin/bash
set -e

export PATH=/usr/local/bin:/usr/bin:/bin

echo "Running predictor inside container at: $(date)" >> /app/predictor.log

/usr/local/bin/python /app/trainer_predictor.py >> /app/predictor.log 2>&1
