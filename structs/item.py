from dataclasses import dataclass
from typing import List


@dataclass()
class Item:
    item_id: int
    name: str
    source: str
    description: str
    tags: List[str]
