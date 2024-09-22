# -*- coding: utf-8 -*-
"""Custom error reporting functions."""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status
from typing import Union
from pydantic import ValidationError

from challenge.exceptions import BaseError
from challenge.core.log_manager import LogManager
from challenge.constants import DATA_INVALID, CONNECTIO_ISSUE


def make_response_based_in_exception(
    detail_for_client: str = "An internal error has occurred.",
    logger: LogManager = None,
    exception_raised: Union[Exception, BaseError] = None,
    return_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """
    Raise HTTP exception and log Exception raised if specified.

    Designed to centralize HTTP error raising in general.

    Args:
        detail_for_client (str, optional): High-level problem description to return.
        logger (LogManager, optional): Object used to log reports if required.
        exception_raised (BaseError, optional): Detailed cause of the problem, just
            for internal logs.
        return_code (int, optional): HTTP code to return in raise. 500 by default.

    Raises:
        HTTPException: With a specified return code and detail.
    """
    if logger:
        if exception_raised:
            exc_log_str = f"{type(exception_raised).__name__}: "
            if isinstance(exception_raised, BaseError):
                exc_log_str += exception_raised.message
                return_code = status.HTTP_306_RESERVED
            else:
                exc_log_str += exception_raised.args[0]
                logger.error(exc_log_str)
        logger.warning(
            f"Raising HTTP Exception ({return_code}) - Detail: '{detail_for_client}'"
        )
    return JSONResponse(
        status_code=return_code,
        content={"detail": detail_for_client},
    )

def unexpected_error_handler(request: Request, exc: Union[Exception, BaseError]):
    """Use HTTP Exception raiser to report Unexpected error."""
    if isinstance(exc, BaseError):
        error_msg = exc.message
    else:
        error_msg = "Unexpected internal error."
    return make_response_based_in_exception(
        detail_for_client=error_msg,
        logger=request.app.logger,
        exception_raised=exc)

def expected_error_handler(request: Request, exc: BaseError):
    """Use BaseError raiser to report operational messages"""
    logger = request.app.logger
    logger.error(f"Exception triggerd {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_303_SEE_OTHER,
        content={"detail": exc.message})

def data_type_error_request(request: Request, exc: ValidationError):
    """Use RequestValidationError raiser to report Invalid data type"""
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content=DATA_INVALID)

def connection_refused_error(request: Request, exc:ConnectionRefusedError):
    """Use ConnectionRefusedError raiser to report connection issues with the database"""
    return JSONResponse(
        status_code=status.HTTP_428_PRECONDITION_REQUIRED,
        content=CONNECTIO_ISSUE)
