from typing import Any

from schemas.response import StandardResponse
from .status_constants import StatusCodes

def generate_response( 
        success : bool,
        responseCode : str,
        responseMessage : str,
        data : Any = None,
        error : Any = None
) -> StandardResponse :
    return StandardResponse(
        success=success,
        responseCode=responseCode,
        responseMessage=responseMessage,
        data=data,
        error=error
    )


def success_response(responseMessage : str, data : Any = None) -> StandardResponse:
    response =  generate_response(True,StatusCodes.SUCCESS_CODE, responseMessage, data=data)
    return response.model_dump(exclude_none=True)