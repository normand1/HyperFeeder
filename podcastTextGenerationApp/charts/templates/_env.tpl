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

{{- if .Values.NEWSLETTER_DATA_SOURCE_RSS_PLUGINS }}
  {{- range .Values.NEWSLETTER_DATA_SOURCE_RSS_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.TAVILY_DATA_SOURCE_PLUGINS }}
  {{- range .Values.TAVILY_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

{{- if .Values.WARPCAST_SEARCH_DATA_SOURCE_PLUGINS }}
  {{- range .Values.WARPCAST_SEARCH_DATA_SOURCE_PLUGINS }}
    {{- $plugins = append $plugins . }}
  {{- end }}
{{- end }}

PODCAST_DATA_SOURCE_PLUGINS="{{ join "," $plugins }}"

PODCAST_INTRO_PLUGINS={{ .Values.PODCAST_INTRO_PLUGINS }}
PODCAST_SCRAPER_PLUGINS={{ .Values.PODCAST_SCRAPER_PLUGINS }}
PODCAST_SEGMENT_WRITER_PLUGINS={{ .Values.PODCAST_SEGMENT_WRITER_PLUGINS }}
PODCAST_OUTRO_PLUGINS={{ .Values.PODCAST_OUTRO_PLUGINS }}
PODCAST_PRODUCER_PLUGINS={{ .Values.PODCAST_PRODUCER_PLUGINS }}
STORY_WRITER_SYSTEM_PROMPT_SUMMARY={{- .Values.STORY_WRITER_SYSTEM_PROMPT_SUMMARY | quote }}
STORY_WRITER_USER_PROMPT_SUMMARY={{- .Values.STORY_WRITER_USER_PROMPT_SUMMARY | quote }}
OUTRO_WRITER_SYSTEM_PROMPT={{- .Values.OUTRO_WRITER_SYSTEM_PROMPT | quote }}
OUTRO_WRITER_USER_PROMPT={{- .Values.OUTRO_WRITER_USER_PROMPT | quote }}
INTRO_WRITER_SYSTEM_PROMPT={{- .Values.INTRO_WRITER_SYSTEM_PROMPT | quote }}
INTRO_WRITER_USER_PROMPT={{- .Values.INTRO_WRITER_USER_PROMPT | quote }}

{{- if .Values.INITIAL_QUERY }}
  INITIAL_QUERY={{ join "," .Values.INITIAL_QUERY | quote }}
{{- end }}

{{- if .Values.PODCAST_RESEARCHER_PLUGINS }}
PODCAST_RESEARCHER_PLUGINS={{ join "," .Values.PODCAST_RESEARCHER_PLUGINS }}
{{- end }}

{{- $pluginsStr := join "," $plugins }}

{{- if (contains "redditDataSourcePlugin" $pluginsStr) }}
SUBREDDIT={{ .Values.SUBREDDIT }}
{{- end }}

{{- if (contains "podcastFeedDataSourcePlugin" $pluginsStr) }}
PODCAST_FEEDS={{ .Values.PODCAST_FEEDS }}
NUMBER_OF_ITEMS_TO_FETCH={{ .Values.NUMBER_OF_ITEMS_TO_FETCH }}
{{- end }}

{{- if (contains "sqliteTokenDataSourcePlugin" $pluginsStr) }}
TOKEN_STORIES_DB_PATH={{ .Values.TOKEN_STORIES_DB_PATH }}
TOKEN_STORIES_COUNT_LIMIT={{ .Values.TOKEN_STORIES_COUNT_LIMIT }}
{{- end }}

{{- if (contains "newsletterRSSFeedDataSourcePlugin" $pluginsStr) }}
NEWSLETTER_RSS_FEEDS={{ .Values.NEWSLETTER_RSS_FEEDS }}
NEWSLETTER_RSS_NUMBER_OF_ITEMS_TO_FETCH={{ .Values.NEWSLETTER_RSS_NUMBER_OF_ITEMS_TO_FETCH }}
{{- end }}

{{- if (contains "hackerNewsDataSourcePlugin" $pluginsStr) }}
NUMBER_OF_POSTS_TO_FETCH={{ .Values.NUMBER_OF_POSTS_TO_FETCH }}
{{- end }}

{{- if (contains "warpcastSearchPlugin" $pluginsStr) }}
WARPCAST_SEARCH_NUMBER_OF_POSTS_TO_FETCH={{ .Values.WARPCAST_SEARCH_NUMBER_OF_POSTS_TO_FETCH }}
{{- end }}

{{- if (contains "redditDataSourcePlugin" $pluginsStr) }}
NUMBER_OF_SUBREDDIT_POSTS_TO_FETCH={{ .Values.NUMBER_OF_SUBREDDIT_POSTS_TO_FETCH }}
{{- end }}

SHOULD_PAUSE_AND_VALIDATE_QUERIES_BEFORE_STARTING={{ .Values.SHOULD_PAUSE_AND_VALIDATE_QUERIES_BEFORE_STARTING }}

{{- if .Values.PODCAST_NAME }}
PODCAST_NAME={{ .Values.PODCAST_NAME | quote }}
{{- end }}
{{- if .Values.PODCAST_TYPE }}
PODCAST_TYPE={{ .Values.PODCAST_TYPE | quote }}
{{- end }}
{{- if .Values.PODCAST_DESCRIPTION }}
PODCAST_DESCRIPTION={{ .Values.PODCAST_DESCRIPTION | quote }}
{{- end }}

LLM_MODEL_PROVIDER={{ .Values.LLM_MODEL_PROVIDER }}
LLM_MODEL_VERSION_NAME={{ .Values.LLM_MODEL_VERSION_NAME }}
MAX_TOKENS_SUMMARY={{ .Values.MAX_TOKENS_SUMMARY }}
TEMPERATURE_SUMMARY={{ .Values.TEMPERATURE_SUMMARY }}

TTS_SCRIPT={{ .Values.TTS_SCRIPT }}
{{- end }}
