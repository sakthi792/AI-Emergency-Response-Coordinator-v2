
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/alerts",
    tags=["Earthquake Alerts"],
)

USGS_FEED_URL = (
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/"
    "summary/all_day.geojson"
)


@router.get("/earthquakes")
async def get_earthquakes(
    min_magnitude: float = Query(default=4.5, ge=0, le=10)
):
    checked_at = datetime.now(timezone.utc).isoformat()

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(USGS_FEED_URL)
            response.raise_for_status()
            data = response.json()

        features = data.get("features", [])
        events = []

        for feature in features:
            props = feature.get("properties") or {}
            geometry = feature.get("geometry") or {}
            coords = geometry.get("coordinates") or []

            magnitude = props.get("mag")

            if magnitude is None or magnitude < min_magnitude:
                continue

            events.append({
                "id": feature.get("id"),
                "magnitude": magnitude,
                "place": props.get("place") or "Location unavailable",
                "time": props.get("time"),
                "depth_km": coords[2] if len(coords) > 2 else None,
                "event_url": props.get("url"),
                "source": "USGS",
            })

        events.sort(
            key=lambda event: event["time"] or 0,
            reverse=True,
        )

        return {
            "status": "source_available",
            "source": USGS_FEED_URL,
            "checked_at": checked_at,
            "min_magnitude": min_magnitude,
            "count": len(events),
            "earthquakes": events,
        }

    except (httpx.HTTPError, ValueError):
        return {
            "status": "unverified",
            "message": "Unable to retrieve current earthquake data.",
            "source": USGS_FEED_URL,
            "checked_at": checked_at,
            "count": 0,
            "earthquakes": [],
        }
