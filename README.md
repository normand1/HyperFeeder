# HyperFeeder - Autonomous Podcast Generator

This application generates dynamic podcasts based on the latest news. The app fetches relevant content, generates an intro, summarizes stories, and even writes podcast descriptions and chapters.

Currently, the only source available for building dynamic podcasts from is the HackerNews API. The plan is to expand this tool to ingest many different configurable sources for building podcast content from as well as new sources for augmenting the source content. See the Issues tab for the planned and in-progress roadmap. Also, feel free to open new issues for feature requests or pull requests for new features you'd like to contribute back.

## Prerequisites

- You will need Python version 3.9.5 or newer. If your Python version is older, you can use `pyenv` to manage multiple versions of Python on your system. Here's how to do it:

    - If you don't have `pyenv` installed, you can install it following the instructions on the [pyenv GitHub](https://github.com/pyenv/pyenv#installation).

    - After `pyenv` is installed, you can install Python 3.9.5 with the following commands:
        
        ```bash
        pyenv install 3.9.5
        pyenv global 3.9.5
        ```
    - Now, check your Python version:
        
        ```bash
        python --version
        ```
      You should see `Python 3.9.5` as the output.

- To access some features, you will need an OpenAI API key. Here's how to get one:

- [Create an account on OpenAI.](https://platform.openai.com/signup/)
- After signing up and logging in, navigate to the API section.
- Here, you'll find your API key. Make sure to keep this key secure and do not share it with anyone.

## Installation 

Clone this repository using git:

```bash
git clone <repo_url>
cd <repo_directory>
```

Run the setup script:

```bash
./setup_script.sh
```

## Dependencies

After setting up, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Folder Structure

Here's a brief overview of the main folders and files in this project:

- `generatePodcast.sh`: Runs all scripts in the correct sequence to build a podcast
- `podcastTextGenerationApp/`: The main Python application.
- `podcastMetaInfoScripts/`: Scripts to manage podcast metadata (chapters and description).
- `audioScripts/`: Scripts to manage audio files.
- `audioScripts/podcast_intro_music.mp3`: Default intro music

## Running the Application

To generate a new podcast you can run the generatePodcast script by running `./generatePodcast.sh`.

If the podcast generation process fails at some point you can re-run any of the failed script directly.
Running `generatePodcast.sh` just runs these scripts in the correct sequence.

If you want to run / debug / modify the python app for podcast text generation you can follow these instructions:

To run the application, navigate to the `podcastTextGenerationApp` directory and run `app.py`:

```bash
cd podcastTextGenerationApp
python app.py
```

## Easy Podcast Modification Points
### Background Music
- You can easily change the intro background music by replacing the file `podcast_intro_music.mp3` with your own music. This file was generated with [Google's experimental Music LM](https://aitestkitchen.withgoogle.com/experiments/music-lm).

### Introduction
- Modify the intro by modifying the prompt for the intro here: `podcastTextGenerationApp/podcastIntroWriter.py`

### New Story Presentation
- Modify the way that the news story segments are presented by modifying the prompt here: `podcastTextGenerationApp/storySegmentWriter.py`

## Contributing

Contributions, issues and feature requests are welcome! Feel free to check [issues page](<repo_issues_url>). If you'd like to contribute new features, open a pull request.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

If you have any questions, feel free to reach out to me at `<david.norman.w@gmail.com>`.

Enjoy your new podcast!
