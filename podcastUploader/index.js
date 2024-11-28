const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

function readEnvFile() {
    try {
        const envPath = path.resolve(__dirname, '../.config.env');
        const envContents = fs.readFileSync(envPath, 'utf8');
        console.log('Contents of ../.config.env:');
        console.log(envContents);
    } catch (error) {
        console.error('Error reading .config.env file:', error.message);
    }
}

readEnvFile();

require('dotenv').config({ path: '../.config.env' });
const { compareDates } = require('./dateutils');
const { isEmpty } = require('./stringUtils');


function addUrlToDescription(youtubeVideoInfo) {
  return process.env.URL_IN_DESCRIPTION
    ? `${youtubeVideoInfo.description}\n${youtubeVideoInfo.url}`
    : youtubeVideoInfo.description;
}

async function setPublishDate(page, date) {
  console.log('-- Setting publish date');
  if (!date || !date.day || !date.monthAsFullWord || !date.year) {
    console.log('-- Warning: Invalid date object. Using current date.');
    date = getCurrentDate();
  }
  await clickSelector(page, 'input[type="radio"][id="publish-date-schedule"]');
  await page.waitForSelector('#date-input', { visible: true });
  await clickSelector(page, '#date-input');

  await selectCorrectYearAndMonthInDatePicker();
  await selectCorrectDayInDatePicker();

  async function selectCorrectYearAndMonthInDatePicker() {
    const dateForComparison = `${date.monthAsFullWord} ${date.year}`;
    const currentDateCaptionElementSelector =
      'div[class*="CalendarMonth"][data-visible="true"] div[class*="CalendarMonth_caption"] > strong';
    let currentDate = await getTextContentFromSelector(page, currentDateCaptionElementSelector);
    const navigationButtonSelector =
      compareDates(dateForComparison, currentDate) === -1
        ? 'div[class*="DayPickerNavigation_leftButton__horizontalDefault"]'
        : 'div[class*="DayPickerNavigation_rightButton__horizontalDefault"]';

    while (currentDate !== dateForComparison) {
      await clickSelector(page, navigationButtonSelector);
      currentDate = await getTextContentFromSelector(page, currentDateCaptionElementSelector);
    }
  }

  async function selectCorrectDayInDatePicker() {
    const dayWithoutLeadingZero = parseInt(date.day, 10);
    const dayXpath = `//div[contains(@class, "CalendarMonth") and @data-visible="true"]//td[contains(text(), "${dayWithoutLeadingZero}")]`;
    await clickXpath(page, dayXpath);
  }
}

async function postEpisode(youtubeVideoInfo) {
  let browser;
  let page;

  console.log(youtubeVideoInfo);
  const { audioFilePath, podcastTitle, podcastDescription, descriptionFilePath } = JSON.parse(youtubeVideoInfo);

  try {
    console.log('Launching puppeteer');
    browser = await puppeteer.launch({ args: [], headless: false });

    page = await openNewPage('https://podcasters.spotify.com/pod/dashboard/episode/wizard');

    console.log('Setting language to English');
    await setLanguageToEnglish();

    console.log('Trying to log in');
    await login();

    console.log('Opening new episode wizard');
    await waitForNewEpisodeWizard();

    console.log('Uploading audio file');
    await uploadEpisode(audioFilePath);

    console.log('Filling required podcast details');
    await fillRequiredDetails(podcastTitle, podcastDescription, descriptionFilePath);

    console.log('Filling optional podcast details');
    // await fillOptionalDetails();

    console.log('Skipping Interact step');
    await skipInteractStep();

    console.log('Save draft or publish');
    await saveDraftOrScheduleOrPublish();

    /*
    This is a workaround solution of the problem where the podcast
    is sometimes saved as draft with title "Untitled" and no other metadata.
    We navigate to the spotify/anchorfm dashboard immediately after podcast is
    published/scheduled.
     */
    await goToDashboard();

    console.log('Yay');
  } catch (err) {
    if (page !== undefined) {
      console.log('Screenshot base64:');
      const screenshotBase64 = await page.screenshot({ encoding: 'base64' });
      console.log(`data:image/png;base64,${screenshotBase64}`);
    }
    throw new Error(`Unable to post episode to anchorfm: ${err}`);
  } finally {
    if (browser !== undefined) {
      await browser.close();
    }
  }

  async function openNewPage(url) {
    const newPage = await browser.newPage();
    await newPage.goto(url);
    await newPage.setViewport({ width: 1600, height: 789 });
    return newPage;
  }

  async function setLanguageToEnglish() {
    await clickSelector(page, 'button[aria-label="Change language"]');
    await clickSelector(page, '[data-testid="language-option-en"]');
  }

  async function login() {
    if (process.env.ANCHOR_LOGIN) {
      await anchorLogin();
    } else {
      await spotifyLogin();
    }
  }

  async function anchorLogin() {
    console.log('-- Accessing Spotify for Podcasters login page');
    await clickXpath(page, '//button[contains(text(), "Continue")]');

    console.log('-- Logging in');
    /* The reason for the wait is because
    anchorfm can take a little longer to load the form for logging in
    and because pupeteer treats the page as loaded(or navigated to)
    even when the form is not showed
    */
    await page.waitForSelector('#email');
    await page.type('#email', process.env.ANCHOR_EMAIL);
    await page.type('#password', process.env.ANCHOR_PASSWORD);
    await clickSelector(page, 'button[type=submit]');
    await page.waitForNavigation();
    console.log('-- Logged in');
  }

  async function spotifyLogin() {
    console.log('-- Accessing new Spotify login page for podcasts');
    await clickXpath(page, '//span[contains(text(), "Continue with Spotify")]/parent::button');
    console.log('-- Logging in');
    
    await page.waitForSelector('#login-username');
    await page.type('#login-username', process.env.SPOTIFY_EMAIL);
    await page.type('#login-password', process.env.SPOTIFY_PASSWORD);
    await sleepSeconds(1);
    await clickSelector(page, 'button[id="login-button"]');
    console.log('login-button');
    // await clickSelector(page, 'button[data-testid="auth-accept"]');
    console.log('auth-accept');
    await page.waitForNavigation();
    console.log('-- In the app');
  }
  
  async function waitForNewEpisodeWizard() {
    await sleepSeconds(1);
    console.log('-- Waiting for episode wizard to open');
    await page.waitForXPath('//span[contains(text(),"Select a file")]');
  }

  async function uploadEpisode(audioFilePath) {
    console.log(audioFilePath);
    console.log('-- Uploading audio file');
    await page.waitForSelector('input[type=file]');
    const inputFile = await page.$('input[type=file]');

    // Attempt to upload the file with retries
    const maxRetries = 3;
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      await inputFile.uploadFile(audioFilePath);
      
      // Check if the upload has started
      try {
        await page.waitForXPath('//span[contains(text(),"Uploading")]', { timeout: 5000 });
        console.log('-- Upload started successfully');
        break;
      } catch (error) {
        if (attempt === maxRetries) {
          throw new Error('Failed to start file upload after multiple attempts');
        }
        console.log(`-- Upload didn't start, retrying (attempt ${attempt}/${maxRetries})`);
      }
    }

    console.log('-- Waiting for upload to finish');
    await page.waitForXPath('//span[contains(text(),"Preview ready!")]');
    console.log('-- Audio file is uploaded');
  }

  async function fillRequiredDetails(podcastTitle, podcastDescription, descriptionFilePath) {
    console.log('-- Adding title');
    const titleInputSelector = '#title-input';
    await page.waitForSelector(titleInputSelector, { visible: true });
    await sleepSeconds(2);
    await page.type(titleInputSelector, podcastTitle);

    console.log('-- Setting switches');

    if (process.env.SET_PUBLISH_DATE) {
        if (youtubeVideoInfo && youtubeVideoInfo.uploadDate) {
            const dateDisplay = `${youtubeVideoInfo.uploadDate.day} ${youtubeVideoInfo.uploadDate.monthAsFullWord}, ${youtubeVideoInfo.uploadDate.year}`;
            console.log('-- Schedule publishing for date: ', dateDisplay);
            await setPublishDate(page, youtubeVideoInfo.uploadDate);
        } else {
            console.log('-- Warning: Upload date is not available. Using current date.');
            await setPublishDate(page, getCurrentDate());
        }
    } else {
        console.log('-- No schedule, should publish immediately');
        await clickSelector(page, 'input[type="radio"][id="publish-date-now"]');
    }

    console.log('-- Selecting content type (explicit or no explicit)');
    const selectorForExplicitContentLabel = process.env.IS_EXPLICIT
        ? 'input[type="radio"][id="explicit-content"]'
        : 'input[type="radio"][id="no-explicit-content"]';
    await clickSelector(page, selectorForExplicitContentLabel, { visible: true });

    console.log('-- Selecting content sponsorship (sponsored or not sponsored)');
    const selectorForSponsoredContent = process.env.IS_SPONSORED
        ? 'input[type="radio"][id="sponsored-content"]'
        : 'input[type="radio"][id="no-sponsored-content"]';
    await clickSelector(page, selectorForSponsoredContent, { visible: true });

    console.log('-- Adding description');
    const textboxInputSelector = 'div[role="textbox"]';
    await page.waitForSelector(textboxInputSelector, { visible: true });

    let description;
    try {
        description = fs.readFileSync(descriptionFilePath, 'utf8');
    } catch (error) {
        console.error(`Error reading description file: ${error.message}`);
        description = podcastDescription;
    }

    // Copy the description to the clipboard
    await page.evaluate((text) => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }, description);

    console.log('-- Description copied to clipboard. Pausing for manual input.');

    // Pause execution and allow manual intervention
    await page.evaluate(() => {
        // Pause execution for manual intervention
        debugger;
    });

    console.log('-- Manual intervention completed, waiting for description to be entered');

    // Wait until the description is entered correctly
    let enteredDescription = '';
    while (true) {
        await sleepSeconds(2); // Wait for a short interval before checking again
        enteredDescription = await page.evaluate((selector) => {
            const element = document.querySelector(selector);
            return element ? element.innerText : '';
        }, textboxInputSelector);
        
        if (enteredDescription.trim() === description.trim()) {
            break;
        }
    }

    console.log('-- Description entered correctly, continuing script');
}

function sleepSeconds(seconds) {
    return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

  async function skipInteractStep() {
    console.log('-- Going to Interact step so we can skip it');
    await clickXpath(page, '//span[text()="Next"]/parent::button');
    console.log('-- Waiting before clicking next again to skip Interact step');
    await sleepSeconds(1);
    console.log('-- Going to final step by skipping Interact step');
    await clickXpath(page, '//span[text()="Next"]/parent::button');
  }

  async function saveDraftOrScheduleOrPublish() {
    if (process.env.SAVE_AS_DRAFT) {
      console.log('-- Saving draft');
      await clickSelector(page, 'header > button > span');
      await page.waitForNavigation();
      await clickXpath(page, '//span[text()="Save draft"]/parent::button');
    } else if (process.env.SET_PUBLISH_DATE) {
      console.log('-- Scheduling');
      await clickXpath(page, '//span[text()="Schedule"]/parent::button');
    } else {
      console.log('-- Publishing');
      await clickXpath(page, '//span[text()="Publish"]/parent::button');
    }
    await clickXpath(page, '//span[text()="Publish"]/parent::button');
    await sleepSeconds(3);
  }

  async function goToDashboard() {
    await page.goto('https://podcasters.spotify.com/pod/dashboard/episodes');
    await sleepSeconds(3);
  }
}

async function sleepSeconds(seconds) {
  await new Promise((r) => {
    setTimeout(r, seconds * 1000);
  });
}

async function clickSelector(page, selector, options = {}) {
  await page.waitForSelector(selector, options);
  const elementHandle = await page.$(selector);
  await clickDom(page, elementHandle);
}

async function clickXpath(page, xpath, options = {}) {
  await page.waitForXPath(xpath, options);
  const [elementHandle] = await page.$x(xpath);
  await clickDom(page, elementHandle);
}

async function clickDom(page, domElementHandle) {
  await page.evaluate((element) => element.click(), domElementHandle);
}

async function getTextContentFromSelector(page, selector, options = {}) {
  await page.waitForSelector(selector, options);
  const elementHandle = await page.$(selector);
  return getTextContentFromDom(page, elementHandle);
}

async function getTextContentFromDom(page, domElementHandle) {
  return page.evaluate((element) => element.textContent, domElementHandle);
}

function getCurrentDate() {
  const now = new Date();
  return {
    day: now.getDate().toString(),
    monthAsFullWord: now.toLocaleString('default', { month: 'long' }),
    year: now.getFullYear().toString()
  };
}

module.exports = {
  postEpisode,
};