import sqlalchemy as sa
from passgen.integrations.pass_storage.models.base import Base
from sqlalchemy.sql import func


class Password(Base):
    __tablename__ = "password"
    __mapper_args__ = {"eager_defaults": True}
    id = sa.Column(sa.INTEGER, primary_key=True)
    owner = sa.Column(sa.VARCHAR(25), nullable=False, index=True)  # tg id
    label = sa.Column(sa.VARCHAR(255), nullable=False, index=True)
    phrase = sa.Column(sa.VARCHAR(1024), unique=True,
                       nullable=False, index=True)

    password = sa.Column(sa.VARCHAR(255), nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, nullable=False,
                           server_default=func.now())
    updated_at = sa.Column(sa.TIMESTAMP, nullable=False,
                           server_default=func.now(),
                           onupdate=func.current_timestamp())
