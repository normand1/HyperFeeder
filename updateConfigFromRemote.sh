#!/usr/bin/env zsh

if [ -z "$1" ]
  then
    echo "No repository URL supplied"
    exit 1
fi

# Get the provided repository URL
repo_url="$1"

# Transform it into the raw URL format
raw_url=${repo_url/github.com/raw.githubusercontent.com}
raw_url="${raw_url}/master"

# Get current date/time
current_time=$(date +%s)

echo "Updating configuration from ${raw_url}"

curl -o ".env" "${raw_url}/.env?${current_time}"
curl -o "podcastTextGenerationApp/podcastDataSourcePlugins/.env.datasource" "${raw_url}/.env.datasource?${current_time}"
curl -o "podcastTextGenerationApp/podcastIntroPlugins/.env.intro" "${raw_url}/.env.intro?${current_time}"
curl -o "podcastTextGenerationApp/podcastOutroWriterPlugins/.env.outro" "${raw_url}/.env.outro?${current_time}"
curl -o "podcastTextGenerationApp/podcastProducerPlugins/.env.producer" "${raw_url}/.env.producer?${current_time}"
curl -o "podcastTextGenerationApp/podcastSummaryPlugins/.env.summary" "${raw_url}/.env.summary?${current_time}"
curl -o "podcastTextGenerationApp/podcastSegmentWriterPlugins/.env.writer" "${raw_url}/.env.writer?${current_time}"
