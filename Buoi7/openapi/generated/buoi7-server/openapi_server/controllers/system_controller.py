import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.health_response import HealthResponse  # noqa: E501
from openapi_server.models.index_response import IndexResponse  # noqa: E501
from openapi_server import util


def get_health():  # noqa: E501
    """Health check

     # noqa: E501


    :rtype: Union[HealthResponse, Tuple[HealthResponse, int], Tuple[HealthResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_index():  # noqa: E501
    """Get API index

     # noqa: E501


    :rtype: Union[IndexResponse, Tuple[IndexResponse, int], Tuple[IndexResponse, int, Dict[str, str]]
    """
    return 'do some magic!'
