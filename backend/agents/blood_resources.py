
from fastapi import APIRouter, Query

router = APIRouter(prefix="/blood", tags=["Blood Resources"])

BLOOD_BANKS = [
    {
        "id": "bank-demo-1",
        "name": "Demo Blood Bank",
        "city": "Coimbatore",
        "address": "Demo address — update before deployment",
        "phone": None,
        "blood_groups": ["O+", "O-", "A+", "B+"],
        "availability": "Call to confirm",
        "verified": False,
    }
]

DONORS = []


@router.get("/banks")
def search_blood_banks(
    blood_group: str = Query(..., min_length=2, max_length=3),
    city: str = Query(..., min_length=2, max_length=80),
):
    group = blood_group.strip().upper()
    city_query = city.strip().casefold()

    valid_groups = {
        "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
    }
    if group not in valid_groups:
        return {"results": [], "message": "Invalid blood group"}

    results = [
        bank for bank in BLOOD_BANKS
        if group in bank["blood_groups"]
        and city_query in bank["city"].casefold()
    ]

    return {
        "count": len(results),
        "results": results,
        "notice": "Demo records only. Call to confirm availability.",
    }


@router.get("/donors")
def search_donors(
    blood_group: str = Query(..., min_length=2, max_length=3),
    city: str = Query(..., min_length=2, max_length=80),
):
    group = blood_group.strip().upper()
    city_query = city.strip().casefold()

    valid_groups = {
        "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
    }
    if group not in valid_groups:
        return {"results": [], "message": "Invalid blood group"}

    results = [
        {
            "id": donor["id"],
            "name": donor["name"],
            "city": donor["city"],
            "blood_group": donor["blood_group"],
            "contact_method": donor["contact_method"],
        }
        for donor in DONORS
        if donor["blood_group"] == group
        and city_query in donor["city"].casefold()
        and donor["consented"] is True
        and donor["active"] is True
    ]

    return {"count": len(results), "results": results}
