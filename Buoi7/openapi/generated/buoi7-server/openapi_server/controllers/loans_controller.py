import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.loan_create_request import LoanCreateRequest  # noqa: E501
from openapi_server.models.loan_detail_envelope import LoanDetailEnvelope  # noqa: E501
from openapi_server.models.loan_list_envelope import LoanListEnvelope  # noqa: E501
from openapi_server.models.loan_write_envelope import LoanWriteEnvelope  # noqa: E501
from openapi_server import util


def create_loan(member_id, body):  # noqa: E501
    """Create a loan for a member

     # noqa: E501

    :param member_id: 
    :type member_id: str
    :param loan_create_request: 
    :type loan_create_request: dict | bytes

    :rtype: Union[LoanWriteEnvelope, Tuple[LoanWriteEnvelope, int], Tuple[LoanWriteEnvelope, int, Dict[str, str]]
    """
    loan_create_request = body
    if connexion.request.is_json:
        loan_create_request = LoanCreateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_loan_detail(loan_id):  # noqa: E501
    """Get loan detail

     # noqa: E501

    :param loan_id: 
    :type loan_id: str

    :rtype: Union[LoanDetailEnvelope, Tuple[LoanDetailEnvelope, int], Tuple[LoanDetailEnvelope, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_member_loans(member_id):  # noqa: E501
    """List loans of one member

     # noqa: E501

    :param member_id: 
    :type member_id: str

    :rtype: Union[LoanListEnvelope, Tuple[LoanListEnvelope, int], Tuple[LoanListEnvelope, int, Dict[str, str]]
    """
    return 'do some magic!'


def return_loan(loan_id):  # noqa: E501
    """Return a borrowed book

     # noqa: E501

    :param loan_id: 
    :type loan_id: str

    :rtype: Union[LoanWriteEnvelope, Tuple[LoanWriteEnvelope, int], Tuple[LoanWriteEnvelope, int, Dict[str, str]]
    """
    return 'do some magic!'
