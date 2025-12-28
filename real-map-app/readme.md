<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# give me in md downloadable format

You can make the README directly downloadable by saving the Markdown content into a file named `README.md`. Below is the **exact file content**; copy–paste it into `README.md` in your project root, and it will be a normal downloadable Markdown file in any Git client or file browser. The text itself is standard Markdown.

```markdown
# Real Map Shortest Path (Delhi / NCR)

This project is a minimal web app that finds the **shortest driving route on a real map** using OpenStreetMap data. It uses:

- OSMnx + NetworkX for routing on a real road graph[web:41]  
- FastAPI as the backend API[web:25]  
- Leaflet as the interactive frontend map UI[web:29]

---

## Features

- Real road network for **Delhi / NCR region** loaded from OpenStreetMap[web:41][web:204]  
- Shortest path between two arbitrary points (click origin and destination on the map)[web:38]  
- Returns and displays:
  - The route as a blue polyline on the map  
  - Total distance in kilometers in the info box

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

