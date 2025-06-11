class StatusCodes:
    # Success
    SUCCESS_CODE = "SU0000"

    # Error
    ERROR_CODE = "ERR0000"
    FILE_NOT_FOUND_CODE = "ERR0001"
    NO_RESULTS_FOUND_CODE = "ERR0002"

class StatusMessages:
    # Success
    SUCCESS_MSG = "Success"


    # Error
    INTERNAL_ERROR = "Internal server error"
    USER_ID_CLIENT_ID_REQUIRED = "UserId/ClientId is required"
    FILE_NOT_FOUND = "File not found"
    NO_PAYLOAD = "Data not found"
    FAILED_TO_UPLOAD = "Failed to upload"
    NO_RESULTS_FOUND = "No results found"
    INVALID_PAYLOAD = "Invalid payload"