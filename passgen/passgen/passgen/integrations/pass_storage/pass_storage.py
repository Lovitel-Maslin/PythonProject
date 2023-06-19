import passgen.integrations.pass_storage.models as models

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from typing import Optional, List

from passgen.core.entities import Password
from passgen.core.config import DatabaseConfig
from passgen.integrations.base import PasswordStorage


class DatabasePasswordStorage(PasswordStorage):
    def __init__(self, config: DatabaseConfig,
                 session: Optional[async_sessionmaker] = None):
        self._config = config
        self._sess = session
        if self._sess is None:
            url = self._config.url
            engine = create_async_engine(url, echo=True)
            self._sess = async_sessionmaker(engine, expire_on_commit=False)

    async def from_phrase(self, phrase: str) -> Optional[Password]:
        query = select(models.Password).where(
            models.Password.phrase == phrase)
        async with self._sess() as conn:
            password = (await conn.execute(query)).scalar()
            return password

    async def from_label(self, owner: str, label: str) -> Optional[Password]:
        query = select(models.Password).where(
            (models.Password.owner == owner) |
            models.Password.label == label)
        async with self._sess() as conn:
            password = (await conn.execute(query)).scalar()
            return password

    async def from_owner(self, owner: str) -> List[Password]:
        query = select(models.Password).where(
            models.Password.owner == owner)
        async with self._sess() as conn:
            password_list = (await conn.execute(query)).all()
            return password_list

    async def save_password(self, owner: str, label: str,
                            phrase: str, password: str) -> bool:
        already_exist = await self.label_exists_for_owner(label, owner)
        if (already_exist):
            return False
        pass_db_model = models.Password(
            owner=owner,
            label=label or "",
            phrase=phrase,
            password=password
        )
        async with self._sess() as conn:
            conn.add(pass_db_model)
            await conn.commit()
        return True

    async def set_label(self, new_label: str, label: Optional[str],
                        phrase: Optional[str]) -> bool:
        if not label and not phrase:
            return False
        query = select(models.Password)
        if label is not None:
            query = query.where(models.Password.label == label)
        elif phrase is not None:
            query = query.where(models.Password.phrase == phrase)

        async with self._sess() as conn:
            password = (await conn.execute(query)).scalar()
            if password is not None:
                password.label = new_label
                await conn.commit()
                return True
        return False

    async def label_exists_for_owner(self, label: str, owner: str) -> bool:
        query = select(models.Password).where(
            (models.Password.label == label) &
            (models.Password.owner == owner))
        async with self._sess() as conn:
            password = (await conn.execute(query)).scalar()
            return password is not None
        return True

    async def set_phrase(self, new_phrase: str, label: str, owner: str) -> bool:
        query = select(models.Password).where(
            (models.Password.label == label) &
            (models.Password.owner == owner))
        async with self._sess() as conn:
            password = (await conn.execute(query)).scalar()
            if password is not None:
                password.phrase = new_phrase
                await conn.commit()
                return True
        return False

    async def delete_password(self, label: str, owner: str) -> bool:
        query = select(models.Password).where(
            (models.Password.label == label) &
            (models.Password.owner == owner))
        async with self._sess() as conn:
            password = (await conn.execute(query)).scalar()
            if password is not None:
                await conn.delete(password)
                await conn.commit()
                return True
        return False
