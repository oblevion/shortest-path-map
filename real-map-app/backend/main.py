from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import osmnx as ox
import networkx as nx

PLACE_NAME = "Delhi, India"  # whole Delhi[web:196][web:204]

# ---------- load real road graph ----------

print(f"Loading graph for {PLACE_NAME} ...")
# Download drivable street network for Delhi[web:41][web:201]
G = ox.graph_from_place(PLACE_NAME, network_type="drive")

# Keep only largest connected component to avoid unreachable pairs[web:41][web:107]
G = ox.truncate.largest_component(G, strongly=False)

# Add edge lengths in meters for routing[web:41]
G = ox.distance.add_edge_lengths(G)

app = FastAPI()

# Allow frontend on another port to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # relax for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "place": PLACE_NAME}

def shortest_path_coords(
    orig_lat: float, orig_lon: float,
    dest_lat: float, dest_lon: float,
) -> Dict[str, Any]:

    orig_node = ox.distance.nearest_nodes(G, X=orig_lon, Y=orig_lat)
    dest_node = ox.distance.nearest_nodes(G, X=dest_lon, Y=dest_lat)

    try:
        # ✅ EXPLICIT DIJKSTRA
        route_nodes: List[int] = nx.dijkstra_path(
            G,
            orig_node,
            dest_node,
            weight="length"
        )
    except nx.NetworkXNoPath:
        return {"coords": [], "length_m": 0.0}

    if not route_nodes:
        return {"coords": [], "length_m": 0.0}

    coords = [
        (G.nodes[n]["y"], G.nodes[n]["x"])
        for n in route_nodes
    ]

    # ✅ CORRECT distance calculation
    total_length = nx.dijkstra_path_length(
        G,
        orig_node,
        dest_node,
        weight="length"
    )

    return {
        "coords": coords,
        "length_m": round(total_length, 2),
    }

@app.get("/route")
def route(
    orig_lat: float,
    orig_lon: float,
    dest_lat: float,
    dest_lon: float,
):
    """
    GET /route?orig_lat=...&orig_lon=...&dest_lat=...&dest_lon=...
    """
    result = shortest_path_coords(orig_lat, orig_lon, dest_lat, dest_lon)
    if not result["coords"]:
        raise HTTPException(
            status_code=404,
            detail="No route found between these points",
        )
    return result
