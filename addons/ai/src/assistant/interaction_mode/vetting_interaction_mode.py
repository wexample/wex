from typing import Optional, TypeVar

from langchain_core.pydantic_v1 import BaseModel

from addons.ai.src.assistant.interaction_mode.formated_data_interaction_mode import FormatedDataInteractionMode
from addons.ai.src.assistant.model.person import Person
from addons.ai.src.assistant.utils.user_prompt_section import UserPromptSection


class VettingInteractionMode(FormatedDataInteractionMode):

    def get_initial_prompt(self, prompt_section: UserPromptSection) -> Optional[str]:
        return (
            "You are a world-class detective tasked with analyzing "
            "conversations and transcriptions of suspected individuals. "
            "Your job is to populate the dataset with information derived from the given text content. "
            "Incorporate a broad range of suppositions. "
            "Employ your expertise to make impressive deductions "
            "by analyzing the language used and applying smart logical interpretations. "
            "This is a first analysis from a non trusted source, so most of information are unreliable"
        )

    def get_pydantic_model(self) -> TypeVar("T", bound=BaseModel):
        return Person
