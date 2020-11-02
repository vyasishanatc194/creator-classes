# -*- coding: utf-8 -*-

from rest_framework import status

# -----------------------------------------------------------------------------


def get_status(code):
    """Get the human readable SNAKE_CASE version of a status code."""
    for name, val in status.__dict__.items():
        if not callable(val) and code is val:
            return name.replace("HTTP_%s_" % code, "")
    return "UNKNOWN"


def modify_api_response(response):
    """
    Modify API response format.
    Example success:
    {
        "code": 200,
        "status": "OK",
        "data": {
            "username": "username"
        }
    }

    Example error:
    {
        "code": 404,
        "status": "NOT_FOUND",
        "errors": [
            {
                "title": "detail",
                "detail": "Not found."
            }
        ]
    }
    """
    # # If errors we got this from the exception handler which already modified the response
    # if status.is_client_error(response.status_code) or status.is_server_error(
    #     response.status_code
    # ):
    #     return response

    # Modify the response data
    modified_data = {}
    modified_data["code"] = response.status_code
    # modified_data["status"] = get_status(response.status_code)

    if response.data.get("errors"):
        modified_data["status"] = "FAIL"
        modified_data["message"] = response.data.get("errors")[0].get("detail")
        modified_data["data"] = []
        # modified_data["errors"] = response.data.get("errors")

    else:
        if response.data.get("status") is None:
            modified_data["status"] = "OK"
        else:
            modified_data["status"] = response.data.get("status")
        modified_data["message"] = response.data.get("message")
        modified_data["data"] = response.data.get("data")

    response.data = modified_data
    return response
