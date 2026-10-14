
from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017",
    serverSelectionTimeoutMS=5000
)

try:
    # Check the database connection
    client.admin.command("ping")
    print("ChefMind connected to MongoDB successfully!")

    # Select the ChefMind database
    db = client["chefmind"]

    # Select the ingredients collection
    ingredients_collection = db["ingredients"]

    # Retrieve all ingredients
    ingredients = ingredients_collection.find(
        {},
        {
            "_id": 0,
            "name": 1,
            "category": 1
        }
    )

    # Display each ingredient
    print("\nIngredients stored in ChefMind:")

    for ingredient in ingredients:
        print(
            f"Name: {ingredient['name']} | "
            f"Category: {ingredient['category']}"
        )

finally:
    client.close()
