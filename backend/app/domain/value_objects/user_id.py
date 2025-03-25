import uuid
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class UserId:
    value: Union[uuid.UUID, str]

    def __post_init__(self):
        object.__setattr__(
            self,
            "value",
            self.value if isinstance(self.value, uuid.UUID) else uuid.UUID(self.value),
        )

    @classmethod
    def generate(cls) -> "UserId":
        return cls(uuid.uuid4())

    def __str__(self) -> str:
        return str(self.value)
