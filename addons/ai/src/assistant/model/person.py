from typing import Optional

from pydantic import BaseModel, Field

from addons.ai.src.assistant.model.reliable_value import ReliableValue


class SocialInfo(BaseModel):
    relationship_status: Optional[ReliableValue] = None
    social_circle_description: Optional[ReliableValue] = None
    profession: Optional[ReliableValue] = None
    income_level: Optional[ReliableValue] = None


class FamilyInfo(BaseModel):
    marital_status: Optional[ReliableValue] = None
    number_of_children: Optional[ReliableValue] = None
    family_background: Optional[ReliableValue] = None


class SexualInfo(BaseModel):
    sexual_orientation: Optional[ReliableValue] = None
    sexual_preferences: Optional[ReliableValue] = None


class GeneralObservations(BaseModel):
    physical_appearance: Optional[ReliableValue] = None
    personality_traits: Optional[ReliableValue] = None
    hobbies_and_interests: Optional[ReliableValue] = None


class Person(BaseModel):
    first_name: ReliableValue
    last_name: ReliableValue
    age: ReliableValue
    email: Optional[ReliableValue] = None
    social_info: Optional[SocialInfo] = Field(default_factory=SocialInfo)
    family_info: Optional[FamilyInfo] = Field(default_factory=FamilyInfo)
    sexual_info: Optional[SexualInfo] = Field(default_factory=SexualInfo)
    general_observations: Optional[GeneralObservations] = Field(default_factory=GeneralObservations)
