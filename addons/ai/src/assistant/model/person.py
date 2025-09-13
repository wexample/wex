from __future__ import annotations


from pydantic import BaseModel, Field

from addons.ai.src.assistant.model.reliable_value import ReliableValue


class SocialInfo(BaseModel):
    relationship_status: ReliableValue | None = None
    social_circle_description: ReliableValue | None = None
    profession: ReliableValue | None = None
    income_level: ReliableValue | None = None


class FamilyInfo(BaseModel):
    marital_status: ReliableValue | None = None
    number_of_children: ReliableValue | None = None
    family_background: ReliableValue | None = None


class SexualInfo(BaseModel):
    sexual_orientation: ReliableValue | None = None
    sexual_preferences: ReliableValue | None = None


class GeneralObservations(BaseModel):
    physical_appearance: ReliableValue | None = None
    personality_traits: ReliableValue | None = None
    hobbies_and_interests: ReliableValue | None = None


class Person(BaseModel):
    first_name: ReliableValue
    last_name: ReliableValue
    age: ReliableValue
    email: ReliableValue | None = None
    social_info: SocialInfo | None = Field(default_factory=SocialInfo)
    family_info: FamilyInfo | None = Field(default_factory=FamilyInfo)
    sexual_info: SexualInfo | None = Field(default_factory=SexualInfo)
    general_observations: GeneralObservations | None = Field(
        default_factory=GeneralObservations
    )
