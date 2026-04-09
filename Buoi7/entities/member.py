from dataclasses import dataclass


@dataclass(slots=True)
class MemberEntity:
    id: str
    name: str
    email: str
