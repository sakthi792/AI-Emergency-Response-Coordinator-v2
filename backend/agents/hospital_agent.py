from database.hospitals import HOSPITALS


def hospital_agent(emergency: str, city: str = "Unknown"):

    emergency = emergency.lower()

    department = "Emergency"

    if any(word in emergency for word in ["accident", "trauma", "bleeding", "injury"]):
        department = "Trauma Care"

    elif any(word in emergency for word in ["burn", "fire"]):
        department = "Burn Care"

    elif any(word in emergency for word in ["heart", "chest", "cardiac"]):
        department = "Cardiology"

    selected = None

    for hospital in HOSPITALS:
        if (
            hospital["city"].lower() == city.lower()
            and hospital["department"].lower() == department.lower()
        ):
            selected = hospital
            break

    if selected is None:
        for hospital in HOSPITALS:
            if hospital["department"].lower() == department.lower():
                selected = hospital
                break

    if selected is None:
        selected = HOSPITALS[0]

    return {
        "hospital_name": selected["name"],
        "city": selected["city"],
        "department": selected["department"],
        "phone": selected["phone"],
        "reason": f"Recommended for {department} in {selected['city']}",
        "priority": "High"
    }