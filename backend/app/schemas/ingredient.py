
from enum import Enum
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class IngredientCategory(str, Enum):
    vegetable = "vegetable"
    fruit = "fruit"
    protein = "protein"
    grain = "grain"
    legume = "legume"
    dairy = "dairy"
    spice = "spice"
    herb = "herb"
    oil = "oil"
    sauce = "sauce"
    condiment = "condiment"
    sweetener = "sweetener"
    nut = "nut"
    seed = "seed"
    fungus = "fungus"
    seafood = "seafood"


class CookingMethod(str, Enum):
    boil = "boil"
    steam = "steam"
    roast = "roast"
    bake = "bake"
    grill = "grill"
    fry = "fry"
    deep_fry = "deep_fry"
    shallow_fry = "shallow_fry"
    pan_fry = "pan_fry"
    saute = "saute"
    stir_fry = "stir_fry"
    sear = "sear"
    braise = "braise"
    pressure_cook = "pressure_cook"
    air_fry = "air_fry"
    caramelize = "caramelize"


Score = Annotated[float, Field(ge=0, le=10)]


class IngredientCreate(BaseModel):

    model_config = ConfigDict(use_enum_values=True)

    name: Annotated[str, Field(min_length=1, max_length=100)]
    category: IngredientCategory
    description: Annotated[str, Field(min_length=1)]
    cooking_methods: list[CookingMethod] = Field(min_length=1)
    taste_profile: dict[str, Score]
    texture_profile: dict[str, Score]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Ingredient name cannot be empty or contain only spaces"
            )

        return value.title()


class IngredientResponse(BaseModel):

    model_config = ConfigDict(use_enum_values=True)

    id: str
    name: str
    category: IngredientCategory
    description: str
    cooking_methods: list[CookingMethod]
    taste_profile: dict[str, Score]
    texture_profile: dict[str, Score]


class IngredientCreatedResponse(BaseModel):

    message: str
    ingredient: IngredientResponse
