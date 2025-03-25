import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise ValueError("Email cannot be empty")

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    def __str__(self) -> str:
        return self.value
