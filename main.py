# -*- coding: utf-8 -*-
"""Main application"""

import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from typing import AsyncIterator
from contextlib import asynccontextmanager

from challenge import constants
from challenge.api import api_leads, api_enroll, api_root
from challenge.core.log_manager import LogManager
from challenge.utils.error_management import (
    unexpected_error_handler,
    data_type_error_request,
    connection_refused_error
)

#Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manages the lifecycle of the FastAPI application.

    This function handles the startup and shutdown events for the application:
    - **Startup**: Initializes the logger, logs application version and startup message.
    - **Shutdown**: Logs a shutdown message when the application is closing.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This is an asynchronous iterator that yields control to FastAPI and waits for the application to finish running.
    """

    # StartUp events
    log_manager = LogManager()
    app.logger = log_manager.logger()
    app.logger.info(f"Unit version: {constants.VERSION}")
    app.logger.info(f"Starting unit execution.")
    try:
        yield
    finally:
    # ShutDown event
        app.logger.info("Shutting down.")

# Initialize App object
app = FastAPI(lifespan=lifespan)

# App metadata
app.title = constants.TITLE
app.description = constants.DESCRIPTION
app.version = constants.VERSION
app.contact = constants.CONTACT

# Include all APIs routers
app.include_router(api_root.router, tags=["root"])
app.include_router(api_leads.router, prefix="/leads", tags=["leads"])
app.include_router(api_enroll.router, prefix="/enroll", tags=["enroll"])

# Response exceptions Handlers
app.add_exception_handler(OSError, connection_refused_error)
app.add_exception_handler(RequestValidationError, data_type_error_request)
app.add_exception_handler(Exception, unexpected_error_handler)

def run_dev_server():
    """Run the server for development purposes."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_dev_server()
