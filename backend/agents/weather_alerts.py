
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["Weather & Disaster Alerts"])

IMD_WARNING_URL = (
    "https://api.imd.gov.in/api/v1/districtwarning"
)

INCOIS_URL = (
    "https://tsunami.incois.gov.in/TEWS/searlywarnings.jsp"
)


@router.get("/weather")
async def get_weather_alerts():
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(IMD_WARNING_URL)
            response.raise_for_status()
            data = response.json()

        if not isinstance(data, list):
            return {
                "status": "unverified",
                "message": "Unexpected response from IMD.",
                "source": IMD_WARNING_URL,
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "alerts": [],
            }

        return {
            "status": "source_available",
            "source": IMD_WARNING_URL,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "alerts": data,
        }

    except Exception:
        return {
            "status": "unverified",
            "message": "Unable to verify current weather alerts.",
            "source": IMD_WARNING_URL,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "alerts": [],
        }


@router.get("/tsunami")
def get_tsunami_source():

    return {
        "status": "official_source_link",
        "message": (
            "Check the official INCOIS page for current tsunami "
            "warnings and advisories."
        ),
        "source": INCOIS_URL,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
