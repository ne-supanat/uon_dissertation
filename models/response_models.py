from pydantic import BaseModel

from models.archetypes import Archetype


class ThinkResponse(BaseModel):
    think: str
    response: str


class ScriptResponse(BaseModel):
    script: str


class ThinkScriptResponse(BaseModel):
    think: str
    script: str


class Code(BaseModel):
    code: str
    quotes: list[str]


class CodeJustification(BaseModel):
    code: str
    justification: str


class KeyComponents(BaseModel):
    file: str | None
    actors: list[Code]
    archetypes: list[Code]
    physical_components: list[Code]
    social_aspect: list[Code]
    psychological_aspect: list[Code]
    misc: list[Code]
    key_activities: list[Code]

    def get_component_names():
        return [
            "Actors",
            "Archetypes",
            "Physical Components",
            "Social Aspect",
            "Psychological Aspect",
            "Misc",
            "Key Activities",
        ]

    def get_component_keys():
        return [
            "actors",
            "archetypes",
            "physical_components",
            "social_aspect",
            "psychological_aspect",
            "misc",
            "key_activities",
        ]

    def get_explanation():
        return """-   Actors are agents which can be a person or groups or organisation inside the system
-   Archetypes are categories of Actors defines what they are allowed or expected to do
-   Physical components are objects or tools or systems that actors use
-   Social aspect is rules or norms about social behaviour
-   Psychological aspect is rules or norms about psychological behaviour
-   Misc are real world elements that do not fall in any component

-   Key activities are interactions between actors and actors or actors and system environment"""


class Profile(BaseModel):
    file: str
    summary: str
    quotes: list[str]
    attributes: list[str]
    archetype: Archetype
