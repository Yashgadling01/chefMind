
from fastapi import APIRouter, Request

from backend.app.schemas.ingredient import (
    IngredientCategory,
    IngredientCreate,
    IngredientResponse,
    IngredientCreatedResponse
)
from backend.app.repositories.ingredient_repository import (
    IngredientRepository
)
from backend.app.services.ingredient_service import IngredientService


router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)


def get_service(request: Request):

    repository = IngredientRepository(
        request.app.state.db["ingredients"]
    )

    return IngredientService(repository)


@router.get("", response_model=list[IngredientResponse])
def get_ingredients(
    request: Request,
    category: IngredientCategory | None = None
):

    return get_service(request).get_all(category)


@router.post(
    "",
    status_code=201,
    response_model=IngredientCreatedResponse
)
def create_ingredient(
    ingredient: IngredientCreate,
    request: Request
):

    return get_service(request).create(
        ingredient.model_dump()
    )


@router.get("/{ingredient_name}", response_model=IngredientResponse)
def get_ingredient(
    ingredient_name: str,
    request: Request
):

    return get_service(request).get_by_name(ingredient_name)


@router.put(
    "/{ingredient_name}",
    response_model=IngredientCreatedResponse
)
def update_ingredient(
    ingredient_name: str,
    ingredient: IngredientCreate,
    request: Request
):

    return get_service(request).update(
        ingredient_name,
        ingredient.model_dump()
    )


@router.delete("/{ingredient_name}")
def delete_ingredient(
    ingredient_name: str,
    request: Request
):

    return get_service(request).delete(ingredient_name)
