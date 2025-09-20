from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Owner

from .owners_schemas import OwnerCreate, OwnerUpdate, OwnerUpdatePartial


async def get_owners(session: AsyncSession) -> list[Owner]:
    stmt = select(Owner).order_by(Owner.id)
    result: Result = await session.execute(stmt)
    owners = result.scalars().all()
    await session.close()
    return list(owners)


async def get_owner(session: AsyncSession, owner_id: int) -> Owner | None:
    return await session.get(Owner, owner_id)


async def create_owner(session: AsyncSession, owner_in: OwnerCreate) -> Owner:
    owner = Owner(**owner_in.model_dump())
    session.add(owner)
    await session.commit()
    await session.refresh(owner)
    await session.close()
    return owner


async def update_owner(
    session: AsyncSession,
    owner: Owner,
    owner_update: OwnerUpdate | OwnerUpdatePartial,
    partial: bool = False, # частично
) -> Owner:
    for name, value in owner_update.model_dump(exclude_unset=partial).items():
        setattr(owner, name, value)
    await session.commit()
    await session.close()
    return owner


async def delete_owner(
    session: AsyncSession,
    owner: Owner,
) -> None:
    await session.delete(owner)
    await session.commit()
    await session.close()
