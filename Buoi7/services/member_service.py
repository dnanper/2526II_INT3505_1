from Buoi7.database import loans_collection, members_collection
from Buoi7.exceptions import AppError
from Buoi7.mappers.member_mapper import (
    member_document_to_entity,
    member_entity_to_detail_response,
    member_entity_to_list_item,
)
from Buoi7.schemas.member import MemberDetailEnvelopeSchema, MemberListEnvelopeSchema


class MemberService:
    def list_members(self) -> MemberListEnvelopeSchema:
        documents = list(members_collection.find().sort("name", 1))

        data = []
        for document in documents:
            entity = member_document_to_entity(document)
            active_loans = loans_collection.count_documents(
                {"member_id": entity.id, "returned_date": None}
            )
            data.append(member_entity_to_list_item(entity, active_loans=active_loans))

        return MemberListEnvelopeSchema(data=data)

    def get_member_detail(self, member_id: str) -> MemberDetailEnvelopeSchema:
        document = members_collection.find_one({"_id": member_id})
        if not document:
            raise AppError("Member not found", 404)

        entity = member_document_to_entity(document)
        active_loans = loans_collection.count_documents(
            {"member_id": member_id, "returned_date": None}
        )
        return MemberDetailEnvelopeSchema(
            data=member_entity_to_detail_response(entity, active_loans=active_loans)
        )
