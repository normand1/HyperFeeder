import os
import sys
from datetime import datetime
import importlib.util
import json
import subprocess
import argparse
from podcastTextGenerator import PodcastTextGenerator
from generatePodcastChapterFile import GeneratePodcastChapterFile


def load_env():
    env_files = [".config.env", "./secrets/.auth.env"]
    for env_file in env_files:
        if os.path.isfile(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value
        else:
            raise FileNotFoundError(f"{env_file} file not found. Some environment variables may not be set correctly.")


def import_module(module_path):
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_command(command):
    result = subprocess.run(command, shell=True, check=True)
    if result.returncode != 0:
        print(f"Error occurred during: {command}")
        sys.exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Podcast generation and upload script")
    parser.add_argument("-f", "--folder", help="Folder name for the podcast", default=None)
    parser.add_argument("-u", "--upload-only", action="store_true", help="Perform upload only")
    parser.add_argument("--initial-query", nargs="+", help="Override INITIAL_QUERY env var with a comma separated list of these values")
    return parser.parse_args()


def main():
    load_env()

    args = parse_arguments()

    if args.initial_query and len(args.initial_query) > 0:
        os.environ["INITIAL_QUERY"] = ",".join(args.initial_query)

    upload_only = args.upload_only
    print(f"UPLOAD_ONLY: {upload_only}")

    if upload_only:
        run_command(f"podcastMetaInfoScripts/generateUploadJsonBody.sh output/{args.folder.strip()}")
        upload(f"output/{args.folder.strip()}")
        return

    if args.folder:
        folder = f"output/{args.folder.strip()}"
        folder_clean = args.folder.strip()
    else:
        podcast_name = os.environ.get("PODCAST_NAME", "").replace(" ", "-").replace('"', "")
        timestamp = datetime.now().strftime("%b%d-%Y-%I%p")
        folder = f"output/{podcast_name}-{timestamp}"
        folder_clean = f"{podcast_name}-{timestamp}"

    os.makedirs(folder, exist_ok=True)

    app = PodcastTextGenerator()
    segmentText = app.run(folder_clean)
    if segmentText:
        return segmentText

    tts_script = os.environ.get("TTS_SCRIPT", "ttsLocalScript.sh")
    run_command(f"audioScripts/{tts_script} {folder}")
    run_command(f"audioScripts/generateIntroWithMusic.sh ./{folder}")
    run_command(f"audioScripts/combineAudioFiles.sh ./{folder}")

    chapter_gen = GeneratePodcastChapterFile()
    chapter_gen.main(folder)
    run_command(f"podcastMetaInfoScripts/generatePodcastDescriptionText.sh ./{folder}")
    run_command(f"podcastMetaInfoScripts/generateUploadJsonBody.sh output/{folder}")

    print("All operations completed successfully.")


def upload(folder):
    print("Upload only mode")
    with open(f"{folder}/uploadJsonBody.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        print(f"config: {config}")
        subprocess.run("npm --prefix podcastUploader install", shell=True, check=True)
        subprocess.run(
            f"npm --prefix podcastUploader run upload -- '{json.dumps(config)}'",
            shell=True,
            check=True,
        )


if __name__ == "__main__":
    result = main()
    if result:
        if isinstance(result, str):
            sys.stdout.write(result)
        elif isinstance(result, bytes):
            sys.stdout.buffer.write(result)
        sys.exit(0)
