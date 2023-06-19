from typing import List, Optional
from passgen.core.entities import Password
from passgen.core.services.base import PasswordService
from passgen.integrations import PasswordStorage


class PasswordServiceImpl(PasswordService):
    def __init__(self, storage: PasswordStorage):
        self._storage = storage

    async def from_phrase(self, phrase: str) -> Optional[Password]:
        return await self._storage.from_phrase(phrase)

    async def from_label(self, owner: str, label: str) -> Optional[Password]:
        return await self._storage.from_label(owner, label)

    async def from_owner(self, owner: str) -> List[Password]:
        return await self._storage.from_owner(owner)

    async def save_password(self, owner: str, label: str,
                            phrase: str, password: str) -> bool:
        return await self._storage.save_password(owner, label, phrase,
                                                 password)

    async def set_label(self, new_label: str, label: Optional[str],
                        phrase: Optional[str]) -> bool:
        return await self._storage.set_label(new_label, label, phrase)

    async def set_phrase(self, new_phrase: str, label: str, owner: str) -> bool:
        return await self._storage.set_phrase(new_phrase, label, owner)

    async def delete_password(self, label: str, owner: str) -> bool:
        return await self._storage.delete_password(label, owner)
