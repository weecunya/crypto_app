import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings
from app.models import Base, Role, User, UserRole
from app.utils import hash_password

connect_args = {"check_same_thread": False}
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True, connect_args=connect_args)

AsyncSessionLocal = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    print('start')
    new_engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True, connect_args=connect_args)
    async with new_engine.begin() as conn:
        print('Connected')
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        roles = await session.execute(select(Role))
        roles = roles.scalars().all()
        if not roles:
            session.add(Role(name="admin"))
            session.add(Role(name="user"))
            await session.commit()
            role_id_res = await session.execute(select(Role.id).where(Role.name=='admin'))
            role_id = role_id_res.scalar_one()
        admin_res = await session.execute(select(User).where(User.email=='admin@example.com'))
        admin = admin_res.scalar_one_or_none()
        if not admin:
            session.add(User(email='admin@example.com',hashed_password=hash_password('admin123'),first_name='admin',last_name='admin',is_active=True))
            await session.commit()
            user_id_res = await session.execute(select(User.id).where(User.email=='admin@example.com'))
            user_id = user_id_res.scalar_one()
            session.add(UserRole(user_id=user_id, role_id=role_id))
            await session.commit()


if __name__ == '__main__':
    asyncio.run(init_db())