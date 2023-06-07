#!/bin/zsh

create_env_file() {
    echo "OPENAI_API_KEY=$1" > .env
}

main() {
    # Check if .env file already exists
    if [[ -f .env ]]; then
        echo ".env file already exists."
        exit 0
    fi

    # Prompt user for OpenAI API key
    read "api_key?Enter your OpenAI API Key: "

    # Create .env file with the API key
    create_env_file "$api_key"
    echo ".env file created successfully."
}

main
