#!/bin/zsh

cd podcastTextGenerationApp/charts
helmfile template > output.yaml
grep -A 1000 "config.env:" output.yaml | sed 's/^ *//' | sed '1d' > ../../.config.env
cd ../../

# Source the updated environment variables
source .config.env

echo "Plugins configured! 🚀🚀🚀"
