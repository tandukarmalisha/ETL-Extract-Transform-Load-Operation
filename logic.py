import re
import logging
from typing import Tuple, Optional, Any, List

def format_name(name_val: Any) -> Optional[str]:
    """Trims, applies initial capital, and limits to 250 characters."""
    name_str: str = str(name_val).strip()
    if not name_str or name_str.lower() == 'nan':
        return None
    
    capitalized: str = " ".join([word.capitalize() for word in name_str.split()])
    return capitalized[:250]

def clean_mobile(mobile_val: Any) -> str:
    """Extracts last 10 digits and sanitizes input to avoid len() errors."""
    digits: str = re.sub(r'\D', '', str(mobile_val))
    if len(digits) < 10:
        raise ValueError(f"Mobile number too short: {digits}")
    return digits[-10:]

def split_email_data(email_val: Any) -> Tuple[str, str]:
    """Splits email into username and domain."""
    email_clean: str = str(email_val).strip().lower()
    if "@" in email_clean:
        parts: List[str] = email_clean.split("@")
        return parts[0], parts[-1]
    return email_clean, "none"