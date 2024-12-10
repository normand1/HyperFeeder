import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


def initialize_llm_model(max_tokens=8096, temperature_env_var="TEMPERATURE_SUMMARY"):
    """
    Initialize and return an LLM model based on environment configuration.

    Args:
        model_version_env_var (str): Environment variable name for model version
        max_tokens (int): Maximum tokens for the model response
        temperature_env_var (str): Environment variable name for temperature setting

    Returns:
        Model instance (ChatOpenAI or ChatAnthropic)

    Raises:
        ValueError: If model_type is not 'openai' or 'anthropic'
    """
    model_type = os.getenv("LLM_MODEL_PROVIDER")
    model_version = os.getenv("LLM_MODEL_VERSION_NAME")

    temperature = float(os.getenv(temperature_env_var))

    if model_type == "openai":
        return ChatOpenAI(model=model_version, max_tokens=max_tokens, temperature=temperature)
    elif model_type == "anthropic":
        return ChatAnthropic(model=model_version, max_tokens=max_tokens, temperature=temperature)
    else:
        raise ValueError("Invalid model_type. Choose 'openai' or 'anthropic'.")
