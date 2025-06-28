from fastapi import APIRouter, Query
from utils.inventory import InventoryAPI
from app.config import settings
import json
import random

router = APIRouter()

# Load products
with open(settings.INVENTORY_PATH, "r") as f:
    product_data = json.load(f)["products"]

# Initialize inventory
inventory = InventoryAPI(product_data)


@router.get("/random")
def recommend_random(
    count: int = Query(default=5, le=settings.MAX_RECOMMENDATIONS)
):
    """
    Recommend random products (fallback or for cold start).
    """
    all_products = inventory.list_all_products()
    return random.sample(all_products, min(count, len(all_products)))


@router.get("/by_category")
def recommend_by_category(
    category: str = Query(..., description="Product category (e.g., Dairy, Snacks)")
):
    """
    Recommend products from the same category.
    """
    products = inventory.list_all_products()
    results = [p for p in products if p["category"].lower() == category.lower()]

    return {
        "category": category,
        "results": results[:settings.MAX_RECOMMENDATIONS]
    }


@router.get("/similar")
def recommend_similar(product_id: str):
    """
    Recommend similar items by diet tag/category.
    """
    target = inventory.get_product(product_id)
    if not target:
        return {"error": "Product not found"}

    all_products = inventory.list_all_products()
    recommendations = []

    for p in all_products:
        if p["product_id"] == product_id:
            continue
        # Recommend if category matches or shares diet tags
        same_category = p["category"] == target["category"]
        shared_tags = bool(set(p.get("diet_tags", [])) & set(target.get("diet_tags", [])))
        if same_category or shared_tags:
            recommendations.append(p)

    return {
        "based_on": target["name"],
        "recommendations": recommendations[:settings.MAX_RECOMMENDATIONS]
    }
