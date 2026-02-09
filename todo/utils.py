from datetime import datetime, timezone
from typing import List

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def join_tags(tags: List[str]) -> str:
    return ",".join(t.strip() for t in tags if t.strip())
