from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from sharedPluginServices.llm_utils import initialize_llm_model
from utilities.env_utils import get_env_var
import json
import os
import hashlib


class LLMChainManager:
    def __init__(
        self,
        system_prompt=None,
        user_prompt=None,
        system_prompt_env_var=None,
        user_prompt_file_env_var=None,
        max_tokens=8096,
    ):
        # Setup cache directory and file
        self.cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        # Create a unique cache file based on the prompts to avoid conflicts
        cache_key = hashlib.md5((str(system_prompt) + str(user_prompt) + str(system_prompt_env_var) + str(user_prompt_file_env_var)).encode()).hexdigest()
        self.cache_file = os.path.join(self.cache_dir, f"llm_cache_{cache_key}.json")

        # Load existing cache or create new one
        self._load_cache()

        # Handle prompts
        self.system_prompt = system_prompt or get_env_var(system_prompt_env_var)
        if user_prompt_file_env_var:
            with open(get_env_var(user_prompt_file_env_var), "r", encoding="utf-8") as file:
                self.user_prompt = file.read()
        else:
            self.user_prompt = user_prompt

        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", self.user_prompt),
            ]
        )
        self.parser = StrOutputParser()

        # Initialize the model using the utility function
        model = initialize_llm_model(max_tokens=max_tokens)

        # Create the chain
        self.chain = self.prompt_template | model | self.parser

    def _load_cache(self):
        """Load the cache from file or create new if doesn't exist"""
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._cache = {}

    def _save_cache(self):
        """Save the current cache to file"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, ensure_ascii=False, indent=2)

    def _get_cache_key(self, kwargs):
        """
        Create a cache key from kwargs dictionary.
        Convert to JSON string to make it hashable.
        """
        return json.dumps(kwargs, sort_keys=True)

    def invoke_chain(self, **kwargs):
        """
        Invoke the LLM chain with the given keyword arguments.
        Returns cached result if the same kwargs were used before.
        """
        cache_key = self._get_cache_key(kwargs)

        if cache_key in self._cache:
            return self._cache[cache_key]

        result = self.chain.invoke(kwargs)
        self._cache[cache_key] = result
        self._save_cache()
        return result
