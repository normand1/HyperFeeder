const fs = require('fs');
const dotenv = require('dotenv');

const defaultValues = {
  EPISODE_PATH: '.',
  ANCHOR_EMAIL: '',
  ANCHOR_PASSWORD: '',
  UPLOAD_TIMEOUT: 60 * 5 * 1000,
  SAVE_AS_DRAFT: false,
  LOAD_THUMBNAIL: false,
  IS_EXPLICIT: false,
  URL_IN_DESCRIPTION: false,
  POSTPROCESSOR_ARGS: '',
  SET_PUBLISH_DATE: false,
  AUDIO_FILE_FORMAT: 'mp3',
  AUDIO_FILE_TEMPLATE: 'episode.%(ext)s',
  THUMBNAIL_FILE_FORMAT: 'jpg',
  THUMBNAIL_FILE_TEMPLATE: 'thumbnail.%(ext)s',
  PUPETEER_HEADLESS: true,
};

const dotEnvVariables = parseDotEnvVariables();

function parseDotEnvVariables() {
  try {
    const envBuf = fs.readFileSync('../secrets/.env.auth');
    return dotenv.parse(envBuf);
  } catch (err) {
    return {};
  }
}

function getEnvironmentVariable(environmentVariableName) {
  return (
    process.env[environmentVariableName] ||
    dotEnvVariables[environmentVariableName] ||
    defaultValues[environmentVariableName]
  );
}

function getDotEnvironmentVariable(environmentVariableName) {
  return dotEnvVariables[environmentVariableName] || defaultValues[environmentVariableName];
}

function getTemplatedFileName(fileTemplate, fileFormat) {
  return fileTemplate.replace('%(ext)s', fileFormat);
}

function getBoolean(value) {
  if (typeof value === 'string') {
    return value.toLowerCase() !== 'false';
  }
  return !!value;
}

module.exports = {
  EPISODE_PATH: `${getEnvironmentVariable('EPISODE_PATH')}/episode.json`,
  ANCHOR_EMAIL: getEnvironmentVariable('ANCHOR_EMAIL'),
  ANCHOR_PASSWORD: getEnvironmentVariable('ANCHOR_PASSWORD'),
  UPLOAD_TIMEOUT: getEnvironmentVariable('UPLOAD_TIMEOUT'),
  SAVE_AS_DRAFT: getBoolean(getEnvironmentVariable('SAVE_AS_DRAFT')),
  LOAD_THUMBNAIL: getBoolean(getEnvironmentVariable('LOAD_THUMBNAIL')),
  IS_EXPLICIT: getBoolean(getEnvironmentVariable('IS_EXPLICIT')),
  URL_IN_DESCRIPTION: getBoolean(getEnvironmentVariable('URL_IN_DESCRIPTION')),
  POSTPROCESSOR_ARGS: getEnvironmentVariable('POSTPROCESSOR_ARGS'),
  SET_PUBLISH_DATE: getBoolean(getEnvironmentVariable('SET_PUBLISH_DATE')),
  AUDIO_FILE_FORMAT: getDotEnvironmentVariable('AUDIO_FILE_FORMAT'),
  AUDIO_FILE_TEMPLATE: getDotEnvironmentVariable('AUDIO_FILE_TEMPLATE'),
  THUMBNAIL_FILE_FORMAT: getDotEnvironmentVariable('THUMBNAIL_FILE_FORMAT'),
  THUMBNAIL_FILE_TEMPLATE: getDotEnvironmentVariable('THUMBNAIL_FILE_TEMPLATE'),
  AUDIO_FILE: getTemplatedFileName(
    getDotEnvironmentVariable('AUDIO_FILE_TEMPLATE'),
    getDotEnvironmentVariable('AUDIO_FILE_FORMAT')
  ),
  THUMBNAIL_FILE: getTemplatedFileName(
    getDotEnvironmentVariable('THUMBNAIL_FILE_TEMPLATE'),
    getDotEnvironmentVariable('THUMBNAIL_FILE_FORMAT')
  ),
  PUPETEER_HEADLESS: getBoolean(getDotEnvironmentVariable('PUPETEER_HEADLESS')),
};