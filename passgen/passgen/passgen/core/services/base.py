from abc import ABC
from typing import List, Optional
from passgen.core.entities import Password, PasswordSpec, PassIdSpec


class PasswordService(ABC):

    def generate_phrase(self, spec: PassIdSpec) -> str:
        raise NotImplementedError()

    async def from_phrase(self, phrase: str) -> Optional[Password]:
        raise NotImplementedError()

    async def from_label(self, owner: str, label: str) -> Optional[Password]:
        raise NotImplementedError()

    async def from_owner(self, owner: str) -> List[Password]:
        raise NotImplementedError()

    async def set_label(self, new_label: str, label: Optional[str],
                        phrase: Optional[str]) -> None:
        raise NotImplementedError()


class PasswordGeneratorService(ABC):
    def generate(self, spec: PasswordSpec) -> str:
        raise NotImplementedError()


class PassIdGeneratorService(ABC):
    def generate(self, spec: PassIdSpec) -> str:
        raise NotImplementedError()
