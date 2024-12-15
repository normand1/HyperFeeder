import hashlib
import json
import os

from langchain_core.prompts import ChatPromptTemplate
from sharedPluginServices.llm_utils import initialize_llm_model


class LLMChainManager:
    def __init__(
        self,
        system_prompt=None,
        user_prompt=None,
        max_tokens=8096,
        structured_output_model=None,
    ):
        self.cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        cache_key = hashlib.md5((str(system_prompt) + str(user_prompt)).encode()).hexdigest()
        self.cache_file = os.path.join(self.cache_dir, f"llm_cache_{cache_key}.json")
        self._load_cache()

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", user_prompt),
            ]
        )

        model = initialize_llm_model(max_tokens=max_tokens)

        if structured_output_model:
            structured_llm = model.with_structured_output(structured_output_model)
            self.chain = self.prompt_template | structured_llm
            self.return_structured = True
        else:
            self.chain = self.prompt_template | model
            self.return_structured = False

    def _load_cache(self):
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._cache = {}

    def _save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, ensure_ascii=False, indent=2)

    def _get_cache_key(self, kwargs):
        return json.dumps(kwargs, sort_keys=True)

    def invoke_chain(self, **kwargs):
        cache_key = self._get_cache_key(kwargs)
        if cache_key in self._cache:
            return self._cache[cache_key]

        result = self.chain.invoke(kwargs)
        if self.return_structured:
            out = result.dict()
        else:
            # For non-structured responses, result is likely an AIMessage. Use its content.
            out = result.content

        self._cache[cache_key] = out
        self._save_cache()
        return out
