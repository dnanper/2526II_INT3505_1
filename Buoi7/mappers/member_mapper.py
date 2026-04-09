from Buoi7.entities import MemberEntity
from Buoi7.schemas.member import (
    MemberCreateRequestSchema,
    MemberDetailResponseSchema,
    MemberListItemSchema,
    MemberSummarySchema,
)


def member_request_to_entity(
    schema: MemberCreateRequestSchema,
    member_id: str,
) -> MemberEntity:
    return MemberEntity(id=member_id, name=schema.name, email=schema.email)


def member_entity_to_document(entity: MemberEntity) -> dict:
    return {"_id": entity.id, "name": entity.name, "email": entity.email}


def member_document_to_entity(document: dict) -> MemberEntity:
    return MemberEntity(
        id=document["_id"],
        name=document["name"],
        email=document["email"],
    )


def member_entity_to_summary(entity: MemberEntity) -> MemberSummarySchema:
    return MemberSummarySchema(id=entity.id, name=entity.name, email=entity.email)


def member_entity_to_list_item(
    entity: MemberEntity,
    *,
    active_loans: int,
) -> MemberListItemSchema:
    return MemberListItemSchema(
        id=entity.id,
        name=entity.name,
        email=entity.email,
        active_loans=active_loans,
    )


def member_entity_to_detail_response(
    entity: MemberEntity,
    *,
    active_loans: int,
) -> MemberDetailResponseSchema:
    return MemberDetailResponseSchema(
        id=entity.id,
        name=entity.name,
        email=entity.email,
        active_loans=active_loans,
    )
