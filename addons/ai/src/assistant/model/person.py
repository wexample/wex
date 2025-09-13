from __future__ import annotations

from pydantic import BaseModel, Field

from addons.ai.src.assistant.model.reliable_value import ReliableValue


class SocialInfo(BaseModel):
    income_level: ReliableValue | None = None
    profession: ReliableValue | None = None
    relationship_status: ReliableValue | None = None
    social_circle_description: ReliableValue | None = None


class FamilyInfo(BaseModel):
    family_background: ReliableValue | None = None
    marital_status: ReliableValue | None = None
    number_of_children: ReliableValue | None = None


class SexualInfo(BaseModel):
    sexual_orientation: ReliableValue | None = None
    sexual_preferences: ReliableValue | None = None


class GeneralObservations(BaseModel):
    hobbies_and_interests: ReliableValue | None = None
    personality_traits: ReliableValue | None = None
    physical_appearance: ReliableValue | None = None


class Person(BaseModel):
    age: ReliableValue
    email: ReliableValue | None = None
    family_info: FamilyInfo | None = Field(default_factory=FamilyInfo)
    first_name: ReliableValue
    general_observations: GeneralObservations | None = Field(
        default_factory=GeneralObservations
    )
    last_name: ReliableValue
    sexual_info: SexualInfo | None = Field(default_factory=SexualInfo)
    social_info: SocialInfo | None = Field(default_factory=SocialInfo)
