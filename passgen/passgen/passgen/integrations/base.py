from abc import ABC
from typing import Optional, List
from passgen.core.entities import Password


class PasswordStorage(ABC):

    async def from_phrase(self, phrase: str) -> Optional[Password]:
        raise NotImplementedError()

    async def from_label(self, owner: str, label: str) -> Optional[Password]:
        raise NotImplementedError()

    async def from_owner(self, owner: str) -> List[Password]:
        raise NotImplementedError()

    async def save_password(self, owner: str, label: str,
                            phrase: str, password: str) -> bool:
        raise NotImplementedError()

    async def set_label(self, new_label: str, label: Optional[str],
                        phrase: Optional[str]) -> bool:
        raise NotImplementedError()

    async def label_exists_for_owner(self, label: str, owner: str) -> bool:
        raise NotImplementedError()

    async def set_phrase(self, new_phrase: str, label: str, owner: str) -> bool:
        raise NotImplementedError()

    async def delete_password(self, label: str, owner: str) -> bool:
        raise NotImplementedError()
