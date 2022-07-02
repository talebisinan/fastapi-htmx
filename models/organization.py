from tortoise.models import Model
from tortoise import fields


class Organization(Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
    session_key = fields.TextField()

    def __str__(self):
        return "organizations"


async def create_organization(title: str, session_key: str):
    organization = await Organization.create(title=title, session_key=session_key)
    return organization


async def get_organization(item_id: int):
    return await Organization.get(id=item_id)


async def update_organization(item_id: int, title: str):
    organization = await get_organization(item_id)
    organization.title = title
    await organization.save()
    return organization


async def get_organizations(session_key: str, skip: int = 0, limit: int = 100):
    return await (
        Organization.filter(session_key=session_key).offset(skip).limit(limit).all()
    )


async def get_organizations_count(session_key: str) -> int:
    return await Organization.filter(session_key=session_key).count()


async def delete_organization(item_id: int):
    organization = await get_organization(item_id)
    await organization.delete()
