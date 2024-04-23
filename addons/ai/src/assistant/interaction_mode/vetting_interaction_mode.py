from typing import Optional, TypeVar

from langchain_core.pydantic_v1 import BaseModel, Extra
from addons.ai.src.assistant.interaction_mode.formated_data_interaction_mode import FormatedDataInteractionMode
from addons.ai.src.assistant.model.person import Person
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class VettingInteractionMode(FormatedDataInteractionMode):

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return "Fill up the dataset based on given text content"

    def get_pydantic_model(self) -> TypeVar("T", bound=BaseModel):
        return Person
