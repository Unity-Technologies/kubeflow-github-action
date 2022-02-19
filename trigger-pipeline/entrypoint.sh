#!/bin/bash

echo "${INPUT_ENCODED_GOOGLE_APPLICATION_CREDENTIALS}" | base64 -d > /tmp/gcloud-sa.json
python  /main.py
