import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book_create_request import BookCreateRequest  # noqa: E501
from openapi_server.models.book_create_response import BookCreateResponse  # noqa: E501
from openapi_server.models.book_detail_envelope import BookDetailEnvelope  # noqa: E501
from openapi_server.models.book_list_envelope import BookListEnvelope  # noqa: E501
from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server import util


def create_book(body):  # noqa: E501
    """Create a new book

     # noqa: E501

    :param book_create_request: 
    :type book_create_request: dict | bytes

    :rtype: Union[BookCreateResponse, Tuple[BookCreateResponse, int], Tuple[BookCreateResponse, int, Dict[str, str]]
    """
    book_create_request = body
    if connexion.request.is_json:
        book_create_request = BookCreateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_book_detail(book_id):  # noqa: E501
    """Get book detail

     # noqa: E501

    :param book_id: 
    :type book_id: str

    :rtype: Union[BookDetailEnvelope, Tuple[BookDetailEnvelope, int], Tuple[BookDetailEnvelope, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_books():  # noqa: E501
    """List all books

     # noqa: E501


    :rtype: Union[BookListEnvelope, Tuple[BookListEnvelope, int], Tuple[BookListEnvelope, int, Dict[str, str]]
    """
    return 'do some magic!'
