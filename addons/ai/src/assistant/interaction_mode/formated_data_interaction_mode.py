import os
from typing import Optional, Any, TypeVar

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.pydantic_v1 import BaseModel, Extra

from addons.ai.src.assistant.interaction_mode.abstract_vector_store_interaction_mode import AbstractInteractionMode
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection

FORMATED_DATA_FORMAT_COMMA_SEPARATED = 'comma-separated'
FORMATED_DATA_FORMAT_JSON = 'json'
FORMATED_DATA_FORMAT_XML = 'xml'
FORMATED_DATA_FORMAT_YAML = 'yaml'
FORMATED_DATA_FORMATS = [
    FORMATED_DATA_FORMAT_COMMA_SEPARATED,
    FORMATED_DATA_FORMAT_JSON,
    FORMATED_DATA_FORMAT_XML,
    FORMATED_DATA_FORMAT_YAML
]


class FormatedDataInteractionMode(AbstractInteractionMode):
    @staticmethod
    def name() -> str:
        return "formated_data"

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return (f"You generate structured data in {(' '.join(prompt_section.options)).upper()} format, "
                f"with any other text before or after. "
                "No introduction. No conclusion. No markdown code block.")

    def get_output_parser(self, prompt_section: UserPromptSection) -> Optional[BaseOutputParser]:
        if FORMATED_DATA_FORMAT_COMMA_SEPARATED in prompt_section.options:
            from langchain_core.output_parsers import CommaSeparatedListOutputParser
            return CommaSeparatedListOutputParser()
        elif FORMATED_DATA_FORMAT_JSON in prompt_section.options:
            from langchain_core.output_parsers import JsonOutputParser
            return JsonOutputParser()
        elif FORMATED_DATA_FORMAT_XML in prompt_section.options:
            from langchain.output_parsers import XMLOutputParser
            return XMLOutputParser()
        elif FORMATED_DATA_FORMAT_YAML in prompt_section.options:
            from langchain.output_parsers import YamlOutputParser
            return YamlOutputParser(pydantic_object=self.get_pydantic_model())

    def get_pydantic_model(self) -> TypeVar("T", bound=BaseModel):
        class AnyFieldObjectContainer(BaseModel):
            class Config:
                extra = Extra.allow

        return AnyFieldObjectContainer

    def chain_response_to_string(
        self,
        prompt_section: UserPromptSection,
        chain_response: Any
    ) -> str:

        if FORMATED_DATA_FORMAT_YAML in prompt_section.options:
            import yaml
            return os.linesep + yaml.dump(chain_response.dict())
        elif FORMATED_DATA_FORMAT_XML in prompt_section.options:
            import dicttoxml
            return os.linesep + dicttoxml.dicttoxml(chain_response).decode()

        return str(chain_response)
