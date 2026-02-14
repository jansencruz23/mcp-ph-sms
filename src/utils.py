import re


def normalize_phone(phone: str) -> str:
    """
    Normalizes phone number to +63 format.
    Accepts: 0917..., +63917..., 63917...
    """
    clean = re.sub(r"[^\d+]", "", phone)

    if clean.startswith("09") and len(clean) == 11:
        return "+63" + clean[1:]

    if clean.startswith("639") and len(clean) == 12:
        return "+" + clean

    if clean.startswith("+639") and len(clean) == 13:
        return clean

    if clean.startswith("9") and len(clean) == 10:
        return "+63" + clean

    return clean
