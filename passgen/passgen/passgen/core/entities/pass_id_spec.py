from dataclasses import dataclass


@dataclass
class PassIdSpec:
    length: int = 8
