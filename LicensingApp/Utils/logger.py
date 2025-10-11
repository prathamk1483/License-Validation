import requests

FORM_ID = "1FAIpQLSejaTLaogLDdX-haMqWeD8YrnRYj223Kk2Bz1_djRPH1xaM3w"
ENTRY_IDS = {
    "level": "entry.400725868",
    "event": "entry.200624023",
    "source": "entry.1759631711",
    "macAddress": "entry.1062631497",
    "success": "entry.46034889",
    "details": "entry.1120702727",
}

FORM_URL = f"https://docs.google.com/forms/d/e/{FORM_ID}/formResponse"

def log(level="", event="", source="", macAddress="", success=None, details=None):
    """
    Submits a log to your Google Form.
    """
    payload = {
        ENTRY_IDS["level"]: level,
        ENTRY_IDS["event"]: event,
        ENTRY_IDS["details"]: details,
        ENTRY_IDS["source"]: source,
        ENTRY_IDS["macAddress"]: macAddress or "",
        ENTRY_IDS["success"]: str(success).lower() if success is not None else "",
    }

    try:
        response = requests.post(FORM_URL, data=payload, timeout=5)
        if response.status_code in [200, 0]:
            print(f"✅ Logged: {event}")
        else:
            print(f"⚠️ Failed to log: HTTP {response.status_code}")
    except Exception as e:
        print(f"⚠️ Exception while logging: {e}")
