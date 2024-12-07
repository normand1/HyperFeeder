{{- define "mypodcast.envVars" -}}
#! This is the configuration file for the podcast generator

{{- $plugins := list -}}

{{- if .Values.ARTICLES_DATA_SOURCE_PLUGINS }}
  {{- range .Values.ARTICLES_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.ARXIV_DATA_SOURCE_PLUGINS }}
  {{- range .Values.ARXIV_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.HACKER_NEWS_DATA_SOURCE_PLUGINS }}
  {{- range .Values.HACKER_NEWS_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.NEWSLETTER_RSS_DATA_SOURCE_PLUGINS }}
  {{- range .Values.NEWSLETTER_RSS_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.PODCAST_DATA_SOURCE_PLUGINS }}
  {{- range .Values.PODCAST_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.SQLITE_DATA_SOURCE_PLUGINS }}
  {{- range .Values.SQLITE_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.REDDIT_DATA_SOURCE_PLUGINS }}
  {{- range .Values.REDDIT_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

PODCAST_DATA_SOURCE_PLUGINS="{{ join "," $plugins }}"

PODCAST_INTRO_PLUGINS={{ .Values.PODCAST_INTRO_PLUGINS }}
PODCAST_SCRAPER_PLUGINS={{ .Values.PODCAST_SCRAPER_PLUGINS }}
PODCAST_SEGMENT_WRITER_PLUGINS={{ .Values.PODCAST_SEGMENT_WRITER_PLUGINS }}
PODCAST_OUTRO_PLUGINS={{ .Values.PODCAST_OUTRO_PLUGINS }}
PODCAST_PRODUCER_PLUGINS={{ .Values.PODCAST_PRODUCER_PLUGINS }}

{{- $pluginsStr := join "," $plugins }}

{{- if (contains "redditAPIPlugin" $pluginsStr) }}
SUBREDDIT={{ .Values.SUBREDDIT }}
{{- end }}

{{- if (contains "articlesRSSFeedPlugin" $pluginsStr) }}
ARTICLES_RSS_FEEDS={{ .Values.ARTICLES_RSS_FEEDS }}
NUMBER_OF_ITEMS_TO_FETCH={{ .Values.NUMBER_OF_ITEMS_TO_FETCH }}
{{- end }}

{{- if (contains "podcastFeedPlugin" $pluginsStr) }}
PODCAST_FEEDS={{ .Values.PODCAST_FEEDS }}
NUMBER_OF_ITEMS_TO_FETCH={{ .Values.NUMBER_OF_ITEMS_TO_FETCH }}
{{- end }}

{{- if (contains "sqliteTokenPlugin" $pluginsStr) }}
TOKEN_STORIES_DB_PATH={{ .Values.TOKEN_STORIES_DB_PATH }}
TOKEN_STORIES_COUNT_LIMIT={{ .Values.TOKEN_STORIES_COUNT_LIMIT }}
{{- end }}

{{- if (contains "newsletterRSSFeedPlugin" $pluginsStr) }}
ARTICLES_RSS_FEEDS={{ .Values.ARTICLES_RSS_FEEDS }}
NUMBER_OF_ITEMS_TO_FETCH={{ .Values.NUMBER_OF_ITEMS_TO_FETCH }}
{{- end }}

{{- if (contains "hackerNewsAPIPlugin" $pluginsStr) }}
NUMBER_OF_POSTS_TO_FETCH={{ .Values.NUMBER_OF_POSTS_TO_FETCH }}
{{- end }}

{{- if (contains "arxivApiPlugin" $pluginsStr) }}
ARXIV_SEARCH_QUERY={{ .Values.ARXIV_SEARCH_QUERY }}
{{- end }}

SHOULD_PAUSE_AND_VALIDATE_STORIES_BEFORE_SCRAPING={{ .Values.SHOULD_PAUSE_AND_VALIDATE_STORIES_BEFORE_SCRAPING }}

PODCAST_NAME="{{ .Values.PODCAST_NAME }}"
PODCAST_TYPE="{{ .Values.PODCAST_TYPE }}"
PODCAST_DESCRIPTION="{{ .Values.PODCAST_DESCRIPTION }}"

LLM_MODEL_PROVIDER={{ .Values.LLM_MODEL_PROVIDER }}
LLM_MODEL_VERSION_NAME={{ .Values.LLM_MODEL_VERSION_NAME }}
OPENAI_MAX_TOKENS_SUMMARY={{ .Values.OPENAI_MAX_TOKENS_SUMMARY }}
OPENAI_TEMPERATURE_SUMMARY={{ .Values.OPENAI_TEMPERATURE_SUMMARY }}

TTS_SCRIPT={{ .Values.TTS_SCRIPT }}
{{- end }}
