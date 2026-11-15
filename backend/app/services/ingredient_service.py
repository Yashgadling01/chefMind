
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException

from backend.app.repositories.ingredient_repository import (
    IngredientRepository
)


class IngredientService:

    def __init__(self, repository: IngredientRepository):
        self.repository = repository

    def get_all(self, category=None):

        ingredients = self.repository.get_all(category)

        for ingredient in ingredients:
            ingredient["id"] = str(ingredient.pop("_id"))

        return ingredients

    def get_by_name(self, name):

        ingredient = self.repository.get_by_name(name)

        if ingredient is None:
            raise HTTPException(
                status_code=404,
                detail="Ingredient not found"
            )

        ingredient["id"] = str(ingredient.pop("_id"))

        return ingredient

    def create(self, data):

        try:
            ingredient_id = self.repository.create(data)

        except DuplicateKeyError:
            raise HTTPException(
                status_code=409,
                detail="An ingredient with this name already exists"
            )

        data["id"] = ingredient_id

        return {
            "message": "Ingredient created successfully",
            "ingredient": data
        }

    def update(self, name, data):

        existing = self.repository.get_by_name(name)

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Ingredient not found"
            )

        try:
            self.repository.update(existing["_id"], data)

        except DuplicateKeyError:
            raise HTTPException(
                status_code=409,
                detail="An ingredient with this name already exists"
            )

        data["id"] = str(existing["_id"])

        return {
            "message": "Ingredient updated successfully",
            "ingredient": data
        }

    def delete(self, name):

        result = self.repository.delete(name)

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Ingredient not found"
            )

        return {
            "message": f"{name} deleted successfully"
        }
