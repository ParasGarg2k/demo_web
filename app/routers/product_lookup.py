from fastapi import APIRouter, HTTPException, Query
from utils.inventory import InventoryAPI
from app.config import settings
import json

router = APIRouter()

# Load product database
with open(settings.INVENTORY_PATH, "r") as f:
    product_data = json.load(f)["products"]

# Initialize in-memory inventory API
inventory = InventoryAPI(product_data)

@router.get("/search")
def search_products(query: str = Query(..., min_length=2)):
    """
    Search products by name substring.
    """
    results = inventory.search_products(query)
    return {"query": query, "results": results}

@router.get("/info")
def get_product_info(product_id: str = Query(...)):
    """
    Get detailed product info by ID.
    """
    product = inventory.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/location")
def get_product_location(product_id: str = Query(...)):
    """
    Get shelf and aisle location for a product.
    """
    product = inventory.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "product_id": product_id,
        "name": product["name"],
        "aisle": product["aisle_id"],
        "shelf": product["shelf_id"]
    }
