import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        return "{name}({attrs})".format(
            name=self.__class__.__name__,
            attrs=", ".join(
                f"{attr}={getattr(self, attr)}" for attr in self.__repr_attrs__
            ),
        )



class TimeStampMixin:
    created_at: Mapped[sa.DateTime] = mapped_column(
        sa.TIMESTAMP(), default=sa.func.now(), nullable=False
    )

    updated_at: Mapped[sa.DateTime] = mapped_column(
        sa.TIMESTAMP(), default=sa.func.now(), onupdate=sa.func.now(), nullable=False
    )


class User(Base, TimeStampMixin):
    __tablename__ = "users"
    __repr_attrs__ = ("id", "username", "email", "is_active", "is_superuser")

    id: Mapped[sa.Integer] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[sa.String] = mapped_column(sa.String, nullable=False)
    email: Mapped[sa.String] = mapped_column(sa.String, nullable=False)
    password: Mapped[sa.String] = mapped_column(sa.String, nullable=False)
    is_active: Mapped[sa.Boolean] = mapped_column(sa.Boolean, default=True)
    is_superuser: Mapped[sa.Boolean] = mapped_column(sa.Boolean, default=False)

    __repr_attrs__ = ["id", "username", "email", "is_active", "is_superuser"]
