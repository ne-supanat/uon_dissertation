from pydantic import BaseModel

from models.archetypes import Archetype


class OutlineResponse(BaseModel):
    think: str
    objective: list[str]
    input: list[str]
    output: list[str]


class ThinkResponse(BaseModel):
    think: str
    response: str


class ScriptResponse(BaseModel):
    script: str


class ThinkScriptResponse(BaseModel):
    think: str
    script: str


class ThemeCode(BaseModel):
    code: str
    quotes: list[str]


class ScopeElement(BaseModel):
    element: str
    description: str
    justification: str


class ScopeComponent(BaseModel):
    actors: list[ScopeElement]
    physical_components: list[ScopeElement]
    social_aspect: list[ScopeElement]
    psychological_aspect: list[ScopeElement]
    misc: list[ScopeElement]
    key_activities: list[ScopeElement]

    def get_component_keys():
        return ScopeInfo().keys

    def get_component_names():
        return ScopeInfo().names

    def get_component_name_from_key(key):
        return ScopeInfo().names[ScopeInfo().keys.index(key)]

    def get_explanation():
        return """-   Actors are agents which can be a person or groups or organisation inside the system
-   Physical components are objects or tools or systems that actors use
-   Social aspect is rules or norms about social behaviour
-   Psychological aspect is rules or norms about psychological behaviour
-   Misc are real world elements that do not fall in any component

-   Key activities are interactions between actors and actors or actors and system environment"""


class ScopeThemeCode(ScopeComponent):
    file: str | None
    actors: list[ThemeCode]
    physical_components: list[ThemeCode]
    social_aspect: list[ThemeCode]
    psychological_aspect: list[ThemeCode]
    misc: list[ThemeCode]
    key_activities: list[ThemeCode]


class Scenario(BaseModel):
    scenario: str
    actions: list[str]


class ScenarioList(BaseModel):
    scenarios: list[Scenario]


class ActionProbability(BaseModel):
    probs: list[float]


class Profile(BaseModel):
    file: str
    summary: str
    quotes: list[str]
    attributes: list[str]
    archetype: Archetype


class ScopeInfo:
    keys = [
        "actors",
        "physical_components",
        "social_aspect",
        "psychological_aspect",
        "misc",
        "key_activities",
    ]

    names = [
        "Actors",
        "Physical Components",
        "Social Aspect",
        "Psychological Aspect",
        "Misc",
        "Key Activities",
    ]
