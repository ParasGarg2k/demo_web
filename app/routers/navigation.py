from fastapi import APIRouter, HTTPException, Query
from utils.nav import Graph, astar  # Adjust import if needed
from app.config import settings

import json

router = APIRouter()

# Load store map JSON (with aisles and shelves)
with open(settings.STORE_MAP_PATH, "r") as f:
    store_map = json.load(f)

graph = Graph()
positions = {}

# Build nodes from aisles and shelves
for aisle in store_map.get("aisles", []):
    node_id = aisle["id"]
    positions[node_id] = (aisle["coordinates"]["x"], aisle["coordinates"]["y"])
    graph.add_node(node_id)

for shelf in store_map.get("shelves", []):
    node_id = shelf["id"]
    positions[node_id] = (shelf["coordinates"]["x"], shelf["coordinates"]["y"])
    graph.add_node(node_id)

# Build edges - you need to define adjacency here
# For example, connect shelves to their aisles, aisles to nearby aisles, etc.

# Connect shelves to their aisles (cost=1)
for shelf in store_map.get("shelves", []):
    graph.add_edge(shelf["id"], shelf["aisle_id"], cost=1)
    graph.add_edge(shelf["aisle_id"], shelf["id"], cost=1)

# Connect aisles linearly or via some logic (example: connect aisles in sequence)
aisle_ids = [aisle["id"] for aisle in store_map.get("aisles", [])]
for i in range(len(aisle_ids) - 1):
    from_id = aisle_ids[i]
    to_id = aisle_ids[i+1]
    # Calculate cost as Euclidean distance or set as 1
    x1, y1 = positions[from_id]
    x2, y2 = positions[to_id]
    cost = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    graph.add_edge(from_id, to_id, cost=cost)
    graph.add_edge(to_id, from_id, cost=cost)


@router.get("/path")
def get_navigation_path(
    start: str = Query(..., description="Start location (e.g., entrance, A1)"),
    end: str = Query(..., description="Destination location (e.g., A4, checkout)")
):
    if start not in positions or end not in positions:
        raise HTTPException(status_code=404, detail="Invalid start or end location")

    path, cost = astar(graph, start, end, positions)

    if path is None:
        raise HTTPException(status_code=400, detail="No path found between locations")

    return {
        "start": start,
        "end": end,
        "path": path,
        "total_cost": cost
    }
