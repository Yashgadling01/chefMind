from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI,HTTPException
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB when the API starts
    client = MongoClient(
        "mongodb://localhost:27017",
        serverSelectionTimeoutMS=5000
    )

    client.admin.command("ping")

    app.state.mongodb_client = client
    app.state.db = client["chefmind"]

    yield

    # Close the connection when the API shuts down
    client.close()


app = FastAPI(
    title="ChefMind API",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "message": "ChefMind is alive! 🍳🤖"
    }


@app.get("/ingredients")
def get_ingredients(category: str | None = None):
    collection = app.state.db["ingredients"]

    if category:
        query = {"category": category}
    else:
        query={}    

    ingredients = collection.find(
        query,
        {"_id": 0}
    )

    return list(ingredients)

@app.post("/ingredients", status_code=201)
def create_ingredient(ingredient: IngredientCreate):
    collection = app.state.db["ingredients"]

    ingredient_data = ingredient.model_dump()

    try:
        result = collection.insert_one(ingredient_data)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="An ingredient with this name already exists"
        )

    ingredient_data["id"] = str(result.inserted_id)

    return {
        "message": "Ingredient created successfully",
        "ingredient": ingredient_data
    }

@app.get("/ingredients/{ingredient_name}")
def get_ingredient(ingredient_name: str):
    collection = app.state.db["ingredients"]

    ingredient = collection.find_one(
        {"name": ingredient_name},
        {"_id": 0}
    )

    if ingredient is None:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )

    return ingredient
