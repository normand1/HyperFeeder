#!/bin/zsh

cd podcastTextGenerationApp/charts

# Generate templates
echo "Generating templates..."
if helmfile template > output.yaml 2>/dev/tty; then
    # Extract environment variables for validation
    grep -A 1000 "config.env:" output.yaml | sed 's/^ *//' | sed '1d' > ../../.config.env
    cd ../../

    # Source the updated environment variables
    source .config.env
    echo "Plugins configured! 🚀🚀🚀"
else
    echo "Failed to generate templates. Please check for errors."
fi
