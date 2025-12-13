#!/bin/bash
echo "Running predictor inside container at: $(date)"
python3 /app/trainer_predictor.py >> /app/predictor.log 2>&1