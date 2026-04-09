import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.member_detail_envelope import MemberDetailEnvelope  # noqa: E501
from openapi_server.models.member_list_envelope import MemberListEnvelope  # noqa: E501
from openapi_server import util


def get_member_detail(member_id):  # noqa: E501
    """Get member detail

     # noqa: E501

    :param member_id: 
    :type member_id: str

    :rtype: Union[MemberDetailEnvelope, Tuple[MemberDetailEnvelope, int], Tuple[MemberDetailEnvelope, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_members():  # noqa: E501
    """List all members

     # noqa: E501


    :rtype: Union[MemberListEnvelope, Tuple[MemberListEnvelope, int], Tuple[MemberListEnvelope, int, Dict[str, str]]
    """
    return 'do some magic!'
