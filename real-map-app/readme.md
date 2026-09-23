

```markdown
<div align="center">

# Delhi / NCR Route Optimizer

A lightweight web application for calculating and visualizing the shortest driving route on a real-world road graph using OpenStreetMap data.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OSMnx](https://img.shields.io/badge/Routing-OSMnx-blue?style=flat-square)](https://osmnx.readthedocs.io/)
[![NetworkX](https://img.shields.io/badge/Graph-NetworkX-orange?style=flat-square)](https://networkx.org/)
[![Leaflet](https://img.shields.io/badge/Frontend-Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![OpenStreetMap](https://img.shields.io/badge/Data-OpenStreetMap-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white)](https://www.openstreetmap.org/)

</div>

---

## Overview

This project implements an interactive routing engine for the **Delhi / NCR** region. It models real-world road topology sourced from OpenStreetMap, processes routing queries asynchronously via a FastAPI backend, and renders optimal paths on a Leaflet-powered interface.

---

## Key Features

* **Real-World Topology:** Constructs a drivable street network graph directly from OpenStreetMap data for Delhi and the National Capital Region (NCR).
* **Interactive Coordinate Selection:** Allows users to define arbitrary origin and destination waypoints directly via map clicks.
* **Shortest Path Computation:** Calculates the optimal driving path over the network graph using graph traversal algorithms via NetworkX.
* **Visual Route Rendering:** Plots the generated route dynamically as a highlighted polyline on the interactive map canvas.
* **Live Route Telemetry:** Displays total driving distance in kilometers in a dedicated interface information panel.

---

## Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Routing Engine** | [OSMnx](https://osmnx.readthedocs.io/) | Retrieves, models, and analyzes street networks from OpenStreetMap |
| **Graph Processing** | [NetworkX](https://networkx.org/) | Computes shortest paths across topological road graphs |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/) | Exposes asynchronous REST endpoints for routing queries |
| **Frontend Map UI** | [Leaflet.js](https://leafletjs.com/) | Provides the interactive map canvas, marker events, and polyline rendering |
| **Map Data** | [OpenStreetMap](https://www.openstreetmap.org/) | Geospatial vector data providing road network attributes |

---

## Workflow

1. **Graph Construction:** The backend downloads and caches the drivable road network graph for Delhi / NCR using OSMnx.
2. **Point Selection:** The user clicks origin and destination locations on the Leaflet map, transmitting GPS coordinates to the API.
3. **Node Snapping & Routing:** The backend matches coordinates to the nearest network nodes and traverses the graph with NetworkX to find the shortest path.
4. **Payload Delivery:** The API returns the polyline coordinates and the total calculated distance in kilometers.
5. **Map Visualization:** Leaflet renders the path and updates the telemetry panel.

---

## Project structure

```

shortest-route-ncr/
backend/
main.py
requirements.txt
frontend/
index.html

```

---

## Backend setup (FastAPI + OSMnx)

### 1. Install dependencies

```

cd backend
python -m pip install -r requirements.txt

```

`requirements.txt`:

```

fastapi
uvicorn
osmnx
networkx
shapely

```

### 2. Configure and run backend

`main.py` (summary):

- Builds a **driving graph** for a bounding box around Delhi / NCR:

```

bbox = (NORTH, SOUTH, EAST, WEST)
G = ox.graph_from_bbox(bbox=bbox, network_type="drive")  \# OSMnx 2.x API[^5][^6]
G = ox.utils_graph.get_largest_component(G, strongly=False)[^7]
G = ox.add_edge_lengths(G)[^8]

```

- Exposes:

- `GET /health` – quick status check  
- `GET /route?orig_lat=...&orig_lon=...&dest_lat=...&dest_lon=...` – shortest path as coordinates + length (meters)[web:38]

Start the API:

```

cd backend
python -m uvicorn main:app --reload

```

Check:

```

http://127.0.0.1:8000/health

```

You should see JSON with `status: "ok"`.

---

## Frontend setup (Leaflet)

### 1. Serve the static file

```

cd frontend
python -m http.server 5500

```

Open:

```

http://127.0.0.1:5500/index.html

```

### 2. What the frontend does

- Loads Leaflet and OpenStreetMap tiles[web:13][web:29]  
- Centers the map over Delhi / NCR at an appropriate zoom  
- On first click: sets **origin**  
- On second click: sets **destination** and calls:

```

GET /route?orig_lat=<lat1>\&orig_lon=<lon1>\&dest_lat=<lat2>\&dest_lon=<lon2>

```

- Draws the returned route as a blue polyline and fits the map to it  
- Shows total route length in kilometers in the status box

---

## Usage

1. Start backend: `python -m uvicorn main:app --reload` (from `backend/`).  
2. Start frontend server: `python -m http.server 5500` (from `frontend/`).  
3. Open `http://127.0.0.1:5500/index.html`.  
4. Click once on a road to set **origin**.  
5. Click again on another road (can be far away within the NCR bounding box) to set **destination**.  
6. The shortest driving route appears in blue and the distance is shown.

---

## Notes / Limitations
  
- If you click outside the bounding box or on isolated areas, the API returns **404 – No route found between these points**.  
- This demo uses static OpenStreetMap data only: no live traffic or advanced constraints beyond what OSM encodes.[web:41]
```


