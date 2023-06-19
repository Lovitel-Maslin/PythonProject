from dataclasses import dataclass


@dataclass
class PasswordSpec:
    use_digits: bool = True
    use_ascii: bool = True
    use_special: bool = True
    length: int = 8
