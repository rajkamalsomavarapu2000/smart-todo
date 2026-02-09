from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    notes: str
    tags: str
    created_at: str
    due_at: Optional[str]
    done: int
    done_at: Optional[str]
