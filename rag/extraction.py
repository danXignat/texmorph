from llama_index.llms.groq import Groq
from llama_index.core.prompts import RichPromptTemplate
from llama_index.core import Settings

import os
import dotenv
import json

from typing import Type
from models.elements import NormalisedNode

from models.types import ElementType

PROMPT = RichPromptTemplate(r"""
Convert the following {{ block_type }} LaTeX block of code to a JSON object that can be parsed by Python's json.loads() function.

IMPORTANT REQUIREMENTS:
1. The output MUST be a valid JSON object that can be parsed with Python's json.loads()
2. All LaTeX commands with backslashes must be properly escaped for JSON
3. For each backslash in LaTeX, use FOUR backslashes (\\\\) in the JSON output
4. Do not include any explanation, markdown formatting, or additional text
5. Return ONLY the JSON object, nothing else
6. Evrything should be in a single line, no newlines or extra spaces should be included.

Pydantic model schema:
{{ schema }}

LATEX:
{{ latex }}

Example of proper escaping:
LaTeX: \alpha
JSON: {"formula": "\\\\alpha"}

RETURN ONLY VALID JSON DATA WITH NO SURROUNDING TEXT:
""")

class RAGExtractor:
    def __init__(self, llm_model: str = "gemma2-9b-it", embed_model: str = None, temperature: float=0):
        dotenv.load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        assert api_key is not None, "GROQ_API_KEY environment variable not set."

        Settings.llm = Groq(model=llm_model, api_key=api_key, temperature=temperature)

        self.llm_model = llm_model
        self.embed_model = embed_model

    def extract(self, block_type: ElementType, latex: str, cls: Type[NormalisedNode]) -> NormalisedNode:
        prompt = PROMPT.format(block_type=block_type, schema=cls.model_json_schema(), latex=latex)

        print(f"INFO - {self.llm_model} call")
        response = str(Settings.llm.complete(prompt))
        print(f"INFO - {self.llm_model} call done")

        try:
            json_data = self._jsonfy(response)
        except Exception as e:
            raise Exception(f"Failed to parse JSON response: {e}\n {latex}")

        return cls(**json_data)

    def _jsonfy(self, data: str) -> dict:
        left = data.index("{")
        right = data.rindex("}")

        j = data[left:right+1]

        with open("eror.json", "w") as f:
            f.write(j)

        parsed_json = json.loads(j)

        return parsed_json

